"""
Script to index textbook content into Qdrant vector database.
This creates the collection and indexes all markdown files from book/docs.
"""

import asyncio
import os
import glob
import hashlib
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
COLLECTION_NAME = "textbook_content"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536  # text-embedding-3-small dimension
CHUNK_SIZE = 500  # characters per chunk
CHUNK_OVERLAP = 100


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap
    return chunks


def extract_metadata(filepath: str, content: str) -> dict:
    """Extract metadata from file path and content."""
    path = Path(filepath)
    parts = path.parts
    
    # Extract chapter and section from path
    chapter = ""
    section = ""
    
    for part in parts:
        if part.startswith("ch") or part.startswith("module"):
            chapter = part
        elif part.endswith(".md"):
            section = part.replace(".md", "").replace("-", " ").title()
    
    # Extract title from content (first # heading)
    title = section
    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    return {
        "chapter": chapter,
        "section": section,
        "title": title,
        "filepath": filepath
    }


async def create_collection():
    """Create Qdrant collection if it doesn't exist."""
    from qdrant_client import AsyncQdrantClient
    from qdrant_client.models import Distance, VectorParams
    
    client = AsyncQdrantClient(
        url=QDRANT_URL, 
        api_key=QDRANT_API_KEY,
        timeout=120  # Increase timeout to 120 seconds
    )
    
    # Check if collection exists
    collections = await client.get_collections()
    collection_names = [c.name for c in collections.collections]
    
    if COLLECTION_NAME in collection_names:
        print(f"Collection '{COLLECTION_NAME}' already exists. Deleting and recreating...")
        await client.delete_collection(COLLECTION_NAME)
    
    # Create collection
    await client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSION,
            distance=Distance.COSINE
        )
    )
    print(f"✅ Created collection '{COLLECTION_NAME}'")
    
    return client


async def get_embedding(text: str) -> list[float]:
    """Get embedding from OpenAI."""
    from openai import AsyncOpenAI
    
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    response = await client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


async def index_documents():
    """Index all markdown files from book/docs."""
    from qdrant_client.models import PointStruct
    
    # Find all markdown files
    docs_path = Path(__file__).parent.parent / "book" / "docs"
    md_files = list(docs_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to index")
    
    # Create collection
    client = await create_collection()
    
    points = []
    point_id = 0
    
    for filepath in md_files:
        print(f"Processing: {filepath.name}")
        
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ⚠️ Error reading file: {e}")
            continue
        
        # Skip empty files
        if not content.strip():
            continue
        
        # Extract metadata
        metadata = extract_metadata(str(filepath), content)
        
        # Chunk the content
        chunks = chunk_text(content)
        print(f"  → {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks):
            # Generate embedding
            try:
                embedding = await get_embedding(chunk)
            except Exception as e:
                print(f"  ⚠️ Error getting embedding: {e}")
                continue
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk,
                    "chapter": metadata["chapter"],
                    "section": metadata["section"],
                    "title": metadata["title"],
                    "filepath": metadata["filepath"],
                    "chunk_index": i
                }
            )
            points.append(point)
            point_id += 1
        
        # Batch upload every 10 points (smaller batches to avoid timeout)
        if len(points) >= 10:
            try:
                await client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
                print(f"  ✅ Uploaded {len(points)} points")
                points = []
            except Exception as e:
                print(f"  ⚠️ Error uploading batch: {e}")
                # Try uploading one by one
                for point in points:
                    try:
                        await client.upsert(collection_name=COLLECTION_NAME, points=[point], wait=True)
                    except Exception as e2:
                        print(f"  ⚠️ Error uploading point: {e2}")
                points = []
    
    # Upload remaining points
    if points:
        try:
            await client.upsert(collection_name=COLLECTION_NAME, points=points, wait=True)
            print(f"✅ Uploaded final {len(points)} points")
        except Exception as e:
            print(f"⚠️ Error uploading final batch: {e}")
    
    # Verify
    info = await client.get_collection(COLLECTION_NAME)
    print(f"\n{'='*50}")
    print(f"✅ Indexing complete!")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Total points: {info.points_count}")
    print(f"{'='*50}")


async def main():
    print("=" * 50)
    print("Textbook Content Indexer")
    print("=" * 50)
    print(f"Qdrant URL: {QDRANT_URL}")
    print(f"Collection: {COLLECTION_NAME}")
    print()
    
    await index_documents()


if __name__ == "__main__":
    asyncio.run(main())
