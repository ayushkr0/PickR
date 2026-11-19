from pinecone import Pinecone, ServerlessSpec

from app.core.config import settings

_client: Pinecone | None = None
_index = None

EMBEDDING_MODEL = "multilingual-e5-large"
EMBEDDING_DIMENSION = 1024


def get_pinecone_client() -> Pinecone:
    global _client
    if _client is None:
        if not settings.pinecone_api_key:
            raise RuntimeError("PINECONE_API_KEY is not configured")
        _client = Pinecone(api_key=settings.pinecone_api_key)
    return _client


def get_or_create_index():
    global _index
    if _index is not None:
        return _index

    pc = get_pinecone_client()
    index_name = settings.pinecone_index_name

    existing = [i.name for i in pc.list_indexes()]
    if index_name not in existing:
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.pinecone_cloud,
                region=settings.pinecone_region,
            ),
        )

    _index = pc.Index(index_name)
    return _index


def embed_texts(texts: list[str], batch_size: int = 90) -> list[list[float]]:
    pc = get_pinecone_client()
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        result = pc.inference.embed(
            model=EMBEDDING_MODEL,
            inputs=batch,
            parameters={"input_type": "passage"},
        )
        all_embeddings.extend(item.values for item in result.data)
    return all_embeddings


def embed_query(text: str) -> list[float]:
    pc = get_pinecone_client()
    result = pc.inference.embed(
        model=EMBEDDING_MODEL,
        inputs=[text],
        parameters={"input_type": "query"},
    )
    return result.data[0].values


def upsert_products(products: list[dict], batch_size: int = 50) -> int:
    """Upsert products into Pinecone.

    Each product dict needs: id, name, category, brand, price, and optionally
    summary, specs, pros, cons for richer searchable text.
    """
    index = get_or_create_index()

    searchable_texts = []
    for p in products:
        parts = [p["name"], p.get("brand", ""), p.get("category", "")]
        if p.get("summary"):
            parts.append(p["summary"])
        if p.get("specs"):
            specs = p["specs"]
            if isinstance(specs, dict):
                parts.extend(f"{k}: {v}" for k, v in specs.items())
        if p.get("pros"):
            parts.extend(p["pros"] if isinstance(p["pros"], list) else [])
        searchable_texts.append(" ".join(str(x) for x in parts if x))

    embeddings = embed_texts(searchable_texts)

    vectors = []
    for p, emb in zip(products, embeddings):
        vectors.append({
            "id": str(p["id"]),
            "values": emb,
            "metadata": {
                "product_id": str(p["id"]),
                "category": p["category"],
                "price": float(p["price"]),
                "brand": p.get("brand", ""),
            },
        })

    upserted = 0
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i : i + batch_size]
        index.upsert(vectors=batch)
        upserted += len(batch)

    return upserted


def search_products(
    query: str,
    category: str | None = None,
    max_budget: float | None = None,
    top_k: int = 5,
) -> list[str]:
    """Search Pinecone for products matching the query.

    Returns a list of product_id strings.
    """
    index = get_or_create_index()
    query_embedding = embed_query(query)

    metadata_filter: dict = {}
    if category:
        metadata_filter["category"] = {"$eq": category}
    if max_budget is not None:
        metadata_filter["price"] = {"$lte": max_budget}

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=metadata_filter if metadata_filter else None,
    )

    return [match.metadata["product_id"] for match in results.matches]
