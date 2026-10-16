from dataclasses import dataclass
from app.rag.retrieval_context import (
    RetrievalContext,
    SourceCitation,
)


@dataclass
class ContextItem:
    source_id: str
    document_id: str
    file_name: str | None
    category: str
    section: str | None
    page_number: int | None
    text: str
    score: float


def build_context_items(
    results: list[dict],
) -> list[ContextItem]:

    context_items = []

    for index, result in enumerate(
        results,
        start=1,
    ):
        source = result["_source"]

        metadata = source.get(
            "metadata",
            {},
        )

        item = ContextItem(
            source_id=f"S{index}",
            document_id=source[
                "document_id"
            ],
            file_name=metadata.get(
                "file_name"
            ),
            category=source.get(
                "category",
                "unknown",
            ),
            section=source.get(
                "section"
            ),
            page_number=source.get(
                "page_number"
            ),
            text=source["text"],
            score=result.get(
                "rerank_score",
                result.get(
                    "rrf_score",
                    0.0,
                ),
            ),
        )

        context_items.append(item)

    return context_items

def build_context_text(
    context_items: list[ContextItem],
) -> str:

    context_blocks = []

    for item in context_items:

        block = f"""
[{item.source_id}]

Document ID: {item.document_id}
File: {item.file_name}
Category: {item.category}
Section: {item.section}
Page: {item.page_number}

Content:
{item.text}
""".strip()

        context_blocks.append(block)

    return "\n\n".join(
        context_blocks
    )

def deduplicate_results(
    results: list[dict],
) -> list[dict]:

    seen = set()
    unique_results = []

    for result in results:
        source = result["_source"]

        key = (
            source["document_id"],
            source.get("chunk_index"),
        )

        if key in seen:
            continue

        seen.add(key)
        unique_results.append(result)

    return unique_results

def build_retrieval_context(
    results: list[dict],
) -> RetrievalContext:

    results = deduplicate_results(results)

    items = build_context_items(
        results
    )

    context_text = build_context_text(
        items
    )

    sources = [
        SourceCitation(
            source_id=item.source_id,
            document_id=item.document_id,
            file_name=item.file_name,
            category=item.category,
            section=item.section,
            page_number=item.page_number,
        )
        for item in items
    ]

    return RetrievalContext(
        context_text=context_text,
        sources=sources,
    )

