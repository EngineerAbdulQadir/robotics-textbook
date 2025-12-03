"""Quick test script to verify services are working."""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_qdrant():
    """Test Qdrant connection and collection."""
    from qdrant_client import AsyncQdrantClient
    
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")
    collection = os.getenv("QDRANT_COLLECTION_NAME", "textbook_content")
    
    print(f"Testing Qdrant connection...")
    print(f"URL: {url}")
    print(f"Collection: {collection}")
    
    try:
        client = AsyncQdrantClient(url=url, api_key=api_key)
        
        # Get collection info
        info = await client.get_collection(collection)
        print(f"✅ Qdrant connected!")
        print(f"   Points count: {info.points_count}")
        
        if info.points_count == 0:
            print("⚠️  WARNING: Collection is empty! You need to index your textbook content.")
        else:
            print(f"   ✅ Collection has data!")
        
        return True
    except Exception as e:
        print(f"❌ Qdrant error: {e}")
        return False


async def test_openai():
    """Test OpenAI connection."""
    from openai import AsyncOpenAI
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    print(f"\nTesting OpenAI connection...")
    print(f"API Key: {api_key[:20]}...")
    
    try:
        client = AsyncOpenAI(api_key=api_key)
        
        # Simple embedding test
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input="test"
        )
        print(f"✅ OpenAI connected!")
        print(f"   Embedding dimension: {len(response.data[0].embedding)}")
        return True
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return False


async def main():
    print("=" * 50)
    print("RAG Chatbot Service Test")
    print("=" * 50)
    
    qdrant_ok = await test_qdrant()
    openai_ok = await test_openai()
    
    print("\n" + "=" * 50)
    if qdrant_ok and openai_ok:
        print("✅ All services OK!")
    else:
        print("❌ Some services failed. Check the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
