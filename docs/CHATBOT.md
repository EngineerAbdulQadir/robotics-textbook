# 🤖 Chatbot Backend - Complete Setup Guide

## 📋 Overview

This RAG (Retrieval-Augmented Generation) chatbot backend uses:
- **FastAPI** - Modern Python web framework
- **PostgreSQL (Neon)** - Serverless database for conversations
- **Qdrant** - Vector database for semantic search
- **OpenAI/Gemini** - LLM for generating responses
- **SQLAlchemy** - ORM for database operations

---

## 🔑 Required Credentials

You need to obtain the following API keys and services:

### 1. **Neon PostgreSQL Database**
### 2. **Qdrant Vector Database**
### 3. **OpenAI API Key** (or Gemini API Key)

---

## 📝 Step-by-Step Setup

### Step 1: Get Neon PostgreSQL Database

**1.1 Create Neon Account**
- Go to: https://neon.tech/
- Click "Sign Up" (free tier available)
- Sign up with GitHub or email

**1.2 Create Database**
- Click "Create Project"
- Project name: `robotics-chatbot`
- Region: Choose closest to you
- PostgreSQL version: 15 (default)
- Click "Create Project"

**1.3 Get Connection String**
- After creation, you'll see "Connection Details"
- Copy the connection string that looks like:
  ```
  postgresql://username:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
  ```
- **Save this!** You'll need it for `.env` file

---

### Step 2: Get Qdrant Vector Database

**2.1 Create Qdrant Cloud Account**
- Go to: https://cloud.qdrant.io/
- Click "Get Started"
- Sign up with GitHub or email

**2.2 Create Cluster**
- Click "Create Cluster"
- Cluster name: `robotics-textbook`
- Cloud provider: Choose one (GCP recommended)
- Region: Choose closest to you
- Plan: Free tier (1GB)
- Click "Create"

**2.3 Get API Credentials**
- After creation, click on your cluster
- Go to "API Keys" tab
- Click "Create API Key"
- Copy the API key (looks like: `qdrant_xxx...`)
- Copy the cluster URL (looks like: `https://xxxx-xxxx.us-east4-0.gcp.cloud.qdrant.io:6333`)
- **Save both!**

**2.4 Create Collection**
- Go to "Collections" tab
- Click "Create Collection"
- Collection name: `textbook_content`
- Vector size: `1536` (for OpenAI embeddings)
- Distance: `Cosine`
- Click "Create"

---

### Step 3: Get OpenAI API Key

**3.1 Create OpenAI Account**
- Go to: https://platform.openai.com/
- Click "Sign Up"
- Verify your email and phone

**3.2 Add Payment Method**
- Go to: https://platform.openai.com/account/billing
- Click "Add payment method"
- Add credit card (required for API access)
- Add $5-10 credit (should last months for development)

**3.3 Create API Key**
- Go to: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Name: `robotics-chatbot`
- Copy the key (starts with `sk-...`)
- **Save this immediately!** You won't see it again

---

### Step 4: Install Dependencies

**4.1 Navigate to Backend**
```bash
cd C:\Users\AQI\OneDrive\Desktop\HACKATHON\robotics-textbook\chatbot-backend
```

**4.2 Create Virtual Environment**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**4.3 Install Requirements**
```powershell
pip install -r requirements.txt
```

---

### Step 5: Configure Environment Variables

**5.1 Create `.env` File**
```powershell
# Copy the example file
copy .env.example .env
```

**5.2 Edit `.env` File**

Open `.env` in notepad or VS Code and fill in your credentials:

```env
# ============================================
# Database Configuration
# ============================================
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# ============================================
# Vector Database (Qdrant)
# ============================================
QDRANT_URL=https://xxxx-xxxx-xxxx-xxxx.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=textbook_content

# ============================================
# LLM Configuration (OpenAI)
# ============================================
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# ============================================
# Application Configuration
# ============================================
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# ============================================
# CORS Configuration
# ============================================
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000,https://YOUR_USERNAME.github.io

# ============================================
# Session Configuration
# ============================================
SESSION_EXPIRY_DAYS=30
MAX_CONVERSATION_HISTORY=50

# ============================================
# API Rate Limiting
# ============================================
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# ============================================
# Feature Flags
# ============================================
ENABLE_HALLUCINATION_CHECK=true
ENABLE_RATE_LIMIT_GRACEFUL_DEGRADATION=true
```

**Important:**
- Replace `NEON_DATABASE_URL` with your Neon connection string
- Replace `QDRANT_URL` with your Qdrant cluster URL
- Replace `QDRANT_API_KEY` with your Qdrant API key
- Replace `OPENAI_API_KEY` with your OpenAI API key
- Update `ALLOWED_ORIGINS` with your GitHub Pages URL

---

### Step 6: Initialize Database

**6.1 Run Migrations**
```powershell
alembic upgrade head
```

This creates all necessary database tables.

---

### Step 7: Index Textbook Content

**7.1 Run Indexing Script**
```powershell
python index_textbook.py
```

This will:
- Read all markdown files from `../book/docs/`
- Split content into chunks
- Generate embeddings using OpenAI
- Store in Qdrant vector database

**Expected output:**
```
Indexing textbook content...
Found 45 markdown files
Processing: intro.md
Processing: chapter1.md
...
Successfully indexed 450 chunks
Done!
```

---

### Step 8: Start the Backend

**8.1 Run Development Server**
```powershell
uvicorn src.main:app --reload --port 8000
```

**8.2 Verify It's Running**
Open browser: `http://localhost:8000/docs`

You should see the FastAPI interactive documentation.

---

## 🧪 Testing the Backend

### Test 1: Health Check

```powershell
curl http://localhost:8000/api/v1/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "qdrant": "connected"
}
```

### Test 2: Ask a Question

```powershell
curl -X POST http://localhost:8000/api/v1/chat/query `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is ROS 2?\", \"session_id\": \"test-123\"}'
```

**Expected response:**
```json
{
  "response": "ROS 2 is the Robot Operating System...",
  "sources": [
    {
      "chapter": "Introduction to ROS 2",
      "content": "...",
      "relevance_score": 0.89
    }
  ],
  "session_id": "test-123"
}
```

### Test 3: Get Conversation History

```powershell
curl http://localhost:8000/api/v1/chat/history?session_id=test-123
```

---

## 📁 Project Structure

```
chatbot-backend/
├── src/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment configuration
│   ├── db.py                   # Database connection
│   ├── models/                 # SQLAlchemy models
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/               # Business logic
│   │   ├── rag_service.py      # RAG pipeline
│   │   ├── qdrant_service.py   # Vector search
│   │   └── llm_service.py      # OpenAI integration
│   ├── api/                    # API endpoints
│   │   └── routes.py
│   └── utils/                  # Utilities
│       ├── chunking.py
│       └── embeddings.py
├── migrations/                 # Database migrations
├── tests/                      # Test files
├── .env                        # Your credentials (DO NOT COMMIT!)
├── .env.example                # Template
├── requirements.txt            # Python dependencies
├── index_textbook.py           # Indexing script
└── README.md
```

---

## 🔧 Configuration Details

### Database (Neon PostgreSQL)

**Purpose:** Store conversation history and messages

**Tables:**
- `conversations` - Chat sessions
- `messages` - Individual messages
- `users` - User data (optional)

**Connection pooling:**
- Pool size: 10 connections
- Max overflow: 20 connections

### Vector Database (Qdrant)

**Purpose:** Semantic search for relevant textbook content

**Collection:** `textbook_content`
- Vector size: 1536 (OpenAI embeddings)
- Distance metric: Cosine similarity
- Indexed fields: chapter, section, content

### LLM (OpenAI)

**Models:**
- **Chat:** `gpt-4` (or `gpt-3.5-turbo` for cheaper option)
- **Embeddings:** `text-embedding-3-small`

**Usage:**
- Embeddings: ~$0.02 per 1M tokens
- GPT-4: ~$0.03 per 1K tokens (input)
- GPT-3.5-Turbo: ~$0.001 per 1K tokens (cheaper alternative)

---

## 💰 Cost Estimates

### Development (Low Usage)
- **Neon:** Free tier (sufficient)
- **Qdrant:** Free tier (1GB, sufficient)
- **OpenAI:** ~$5-10/month

### Production (Moderate Usage)
- **Neon:** ~$10-20/month
- **Qdrant:** ~$25/month (Pro plan)
- **OpenAI:** ~$50-100/month

**Total:** ~$85-140/month for production

---

## 🛠️ Troubleshooting

### Issue: "OPENAI_API_KEY must be set"

**Solution:**
- Check `.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set
- Restart the server

### Issue: "Connection to Neon failed"

**Solution:**
- Verify `NEON_DATABASE_URL` is correct
- Check Neon dashboard - database should be "Active"
- Ensure `?sslmode=require` is at the end of URL

### Issue: "Qdrant connection failed"

**Solution:**
- Verify `QDRANT_URL` and `QDRANT_API_KEY`
- Check Qdrant dashboard - cluster should be "Running"
- Ensure collection `textbook_content` exists

### Issue: "No results found for query"

**Solution:**
- Run indexing script: `python index_textbook.py`
- Verify docs exist in `../book/docs/`
- Check Qdrant dashboard - collection should have points

### Issue: "Rate limit exceeded"

**Solution:**
- Check OpenAI usage: https://platform.openai.com/usage
- Add more credits if needed
- Use `gpt-3.5-turbo` instead of `gpt-4`

---

## 🚀 Alternative: Use Gemini Instead of OpenAI

If you prefer Google's Gemini (free tier available):

**1. Get Gemini API Key**
- Go to: https://makersuite.google.com/app/apikey
- Click "Create API Key"
- Copy the key

**2. Update `.env`**
```env
# Comment out OpenAI
# OPENAI_API_KEY=sk-...

# Add Gemini
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

**3. Update `src/config.py`**
Change the validator to check for Gemini instead of OpenAI.

---

## 📚 API Documentation

Once running, visit:
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Main Endpoints:

**1. POST /api/v1/chat/query**
- Ask questions about textbook
- Returns answer + citations

**2. POST /api/v1/chat/selection**
- Ask about selected text
- Context-aware responses

**3. GET /api/v1/chat/history**
- Get conversation history
- Filter by session_id

**4. GET /api/v1/health**
- Check service health
- Verify connections

---

## 🔐 Security Notes

### DO NOT:
- ❌ Commit `.env` file to Git
- ❌ Share API keys publicly
- ❌ Expose database credentials
- ❌ Use production keys in development

### DO:
- ✅ Use `.env` for local development
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Monitor API usage
- ✅ Enable rate limiting

---

## 📊 Monitoring

### Check Logs
```powershell
# View logs
tail -f logs/chatbot.log

# Or in PowerShell
Get-Content logs/chatbot.log -Wait
```

### Monitor API Usage

**OpenAI:**
- Dashboard: https://platform.openai.com/usage
- Set usage limits to avoid surprises

**Neon:**
- Dashboard: https://console.neon.tech/
- Monitor connection count and storage

**Qdrant:**
- Dashboard: https://cloud.qdrant.io/
- Check vector count and memory usage

---

## ✅ Setup Checklist

- [ ] Neon PostgreSQL database created
- [ ] Qdrant cluster created and collection set up
- [ ] OpenAI API key obtained and credits added
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with all credentials
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Textbook content indexed (`python index_textbook.py`)
- [ ] Backend server running (`uvicorn src.main:app --reload`)
- [ ] Health check passes (`curl http://localhost:8000/api/v1/health`)
- [ ] Test query successful

---

## 🎯 Next Steps

1. **Test thoroughly** - Try various questions
2. **Monitor costs** - Check OpenAI usage daily
3. **Optimize** - Tune chunk size and retrieval count
4. **Deploy** - Use Render, Railway, or Docker
5. **Connect frontend** - Update chat widget to use your backend

---

## 📞 Support

### Useful Links:
- **Neon Docs:** https://neon.tech/docs
- **Qdrant Docs:** https://qdrant.tech/documentation/
- **OpenAI Docs:** https://platform.openai.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/

### Common Commands:
```powershell
# Start backend
uvicorn src.main:app --reload --port 8000

# Run migrations
alembic upgrade head

# Index content
python index_textbook.py

# Run tests
pytest tests/ -v

# Check logs
Get-Content logs/chatbot.log -Wait
```

---

**Your chatbot backend is now ready to use!** 🎉

**Backend URL:** `http://localhost:8000`
**API Docs:** `http://localhost:8000/docs`
