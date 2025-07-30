#!/usr/bin/env python3

"""
OpenAI-compatible wrapper for the RAG chat functionality.
This wrapper adapts the rag-components/chat.py to use only OpenAI API
and our template system, without modifying the read-only submodule.
"""

import os
import sys
from pathlib import Path
import click
from typing import List
import importlib.util

# Import our template system
from .prompts import get_rag_chat_context

# Add rag-components to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "rag-components"))

# Import from rag-components
import query_db
from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI


def check_rag_components_available():
    """Check if RAG components are available and installed."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    rag_components_path = repo_root / "rag-components"
    return (
        importlib.util.find_spec("chromadb") is not None
        and rag_components_path.exists()
    )


def setup_rag_path():
    """Add rag-components directory to the Python path."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    rag_path = str(repo_root / "rag-components")
    if rag_path not in sys.path:
        sys.path.append(rag_path)
    return rag_path


def get_rag_snippets(
    query,
    collection_name="vtk-examples",
    database_path="./db/codesage-codesage-large-v2",
    top_k=5,
):
    """Get code snippets from the RAG database."""
    setup_rag_path()
    try:
        import query_db

        client = query_db.initialize_db(database_path)
        results = query_db.query_db(query, collection_name, top_k, client)

        relevant_examples = []
        for item in results["code_metadata"]:
            if "original_id" in item:
                relevant_examples.append(item["original_id"])

        for item in results["text_metadata"]:
            if "code" in item:
                relevant_examples.append(item["code"])

        relevant_examples = list(set(relevant_examples))

        return {
            "code_snippets": results["code_documents"],
            "text_snippets": results["text_documents"],
            "code_metadata": results["code_metadata"],
            "references": relevant_examples,
        }
    except Exception as e:
        print(f"Error using RAG components: {e}")
        return None


class OpenAIRAGChat:
    """OpenAI-compatible wrapper for RAG chat functionality."""

    def __init__(
        self, model: str = "gpt-4o", database: str = "./db/codesage-codesage-large-v2"
    ):
        """Initialize the OpenAI RAG chat system.

        Args:
            model: OpenAI model to use
            database: Path to the RAG database
        """
        self.model = model
        self.database = database
        self.llm = None
        self.client = None
        self.history = [
            ChatMessage(role="system", content="You are a helpful VTK assistant")
        ]

        self._init_components()

    def _init_components(self):
        """Initialize LLM and database components."""
        try:
            # Only support OpenAI compatible models
            self.llm = OpenAI(model=self.model)
        except Exception as e:
            raise RuntimeError(f"Unsupported Model {self.model}: {e}")

        self.client = query_db.initialize_db(database_path=self.database)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

    def ask(
        self,
        query: str,
        collection_name: str = "python-examples",
        top_k: int = 15,
        streaming: bool = False,
    ):
        """Ask a question using RAG-enhanced chat.

        Args:
            query: User's question
            collection_name: RAG collection to search
            top_k: Number of examples to retrieve
            streaming: Whether to stream the response

        Returns:
            Dictionary with response and references
        """
        # Add user query to history
        self.history.append(ChatMessage(role="user", content=query))

        # Query the RAG database for relevant documents
        results = query_db.query_db(query, collection_name, top_k, self.client)
        relevant_examples = [
            item["original_id"] for item in results["code_metadata"]
        ] + [item["code"] for item in results["text_metadata"]]
        snippets = [item for item in results["code_documents"]]
        relevant_examples = list(set(relevant_examples))

        # Combine the retrieved documents into a single text
        retrieved_text = "\n\n## Next example:\n\n".join(snippets)

        # Use our template system instead of the hardcoded PROMPT
        content = get_rag_chat_context(retrieved_text, query.rstrip())

        # Add the enhanced context as a message
        self.history.append(ChatMessage(role="assistant", content=content.rstrip()))

        # Generate a response using the LLM
        if streaming:
            response = self.llm.stream_chat(self.history)
        else:
            response = self.llm.chat(self.history)

        return {"response": response, "references": relevant_examples}

    def generate_urls_from_references(self, references: List[str]) -> List[str]:
        """Generate URLs from reference paths.

        Args:
            references: List of reference file paths

        Returns:
            List of generated URLs
        """
        urls = []
        for ref in references:
            ref = Path(ref)
            # Transform vtk-examples.git/src/Python/PolyData/CurvaturesAdjustEdges.py
            # to https://examples.vtk.org/site/Python/PolyData/CurvaturesAdjustEdges
            try:
                url = "https://examples.vtk.org/site/{}".format(
                    (ref.relative_to(ref.parents[-3])).with_suffix("")
                )
                urls.append(url)
            except ValueError:
                # If we can't compute relative path, skip this reference
                continue
        return urls


@click.command()
@click.option(
    "--database", default="./db/codesage-codesage-large-v2", help="Path to the database"
)
@click.option(
    "--collection-name",
    default="python-examples",
    help="Name for the collection in the database",
)
@click.option(
    "--top-k",
    type=int,
    default=15,
    help="Retrieve the top k examples from the database",
)
@click.option("--model", default="gpt-4o", help="OpenAI model to use")
def main(database, collection_name, top_k, model):
    """Query database for code snippets using OpenAI API only."""

    # Initialize the chat system
    chat = OpenAIRAGChat(model, database)

    print("Welcome to VTK's OpenAI-powered assistant! What would you like to know?")
    print("Type 'exit' to quit")

    while True:
        user_input = input("User: ")
        if len(user_input) == 0:
            continue

        full_reply = ""
        if user_input.lower() == "exit":
            print("Bye!")
            break

        try:
            reply = chat.ask(user_input, collection_name, top_k, streaming=True)
            for item in reply["response"]:
                print(item.delta, end="")
                full_reply += item.delta

            print("\n Here are some relevant references:")
            for ref_url in chat.generate_urls_from_references(reply["references"]):
                print(ref_url)

            # Add reply to the chat history
            chat.history.append(
                ChatMessage(role="assistant", content=full_reply.rstrip())
            )

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
