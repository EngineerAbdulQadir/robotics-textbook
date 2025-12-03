# RAG Chatbot Backend

FastAPI-based backend for the Physical AI Textbook RAG (Retrieval-Augmented Generation) chatbot.

## Overview

This service provides:
- Natural language Q&A using Gemini LLM and Qdrant vector search
- Text selection-based contextual questions
- Conversation history and session management
- RAG pipeline with hallucination prevention

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (Neon Serverless)
- Qdrant Cloud
- Google Gemini API key

### Local Development Setup

1. **Clone and setup**:
```bash
git clone <repo>
cd chatbot-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API keys and database URLs
```

3. **Run with Docker Compose**:
```bash
docker-compose up -d
```

4. **Run migrations**:
```bash
cd chatbot-backend
alembic upgrade head
```

5. **Start development server**:
```bash
uvicorn src.main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
chatbot-backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # SQLAlchemy models (Message, Conversation, etc.)
│   ├── services/            # Business logic (RAG, Qdrant, Gemini, etc.)
│   ├── api/                 # REST API endpoints (/chat/query, /chat/selection, etc.)
│   └── utils/               # Utilities (chunking, embeddings, errors, logging)
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data and mocks
├── migrations/              # Alembic database migrations
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── Dockerfile               # Container image
├── docker-compose.yml       # Local development services
└── README.md               # This file
```

## API Endpoints

### Chat Endpoints

- **POST /api/v1/chat/query** - Send question about textbook content
  ```bash
  curl -X POST http://localhost:8000/api/v1/chat/query \
    -H "Content-Type: application/json" \
    -d '{"question": "How do ROS 2 nodes communicate?", "session_id": "session-123"}'
  ```

- **POST /api/v1/chat/selection** - Ask question about selected text
  ```bash
  curl -X POST http://localhost:8000/api/v1/chat/selection \
    -H "Content-Type: application/json" \
    -d '{"selected_text": "ROS 2 nodes...", "question": "Explain this more?", "session_id": "session-123", "chapter": "Module 1"}'
  ```

- **GET /api/v1/chat/history** - Retrieve conversation history
  ```bash
  curl http://localhost:8000/api/v1/chat/history?session_id=session-123
  ```

### Health Check

- **GET /api/v1/health** - Service health status

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run integration tests (requires services running)
pytest tests/integration/ -v --with-external-services
```

## Database Management

### Create Migration

```bash
alembic revision --autogenerate -m "Description of changes"
```

### Run Migrations

```bash
alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1
```

## Configuration

### Environment Variables

```
NEON_DATABASE_URL=postgresql://...
QDRANT_URL=https://...
QDRANT_API_KEY=...
GEMINI_API_KEY=...
SESSION_EXPIRY_DAYS=30
LOG_LEVEL=INFO
```

See `.env.example` for full list.

## Development Guidelines

### Code Style

- Use Black for formatting: `black src/ tests/`
- Lint with Ruff: `ruff check src/ tests/`
- Type hints required for function signatures

### Adding New Endpoints

1. Create model in `src/models/`
2. Create service logic in `src/services/`
3. Add endpoint in `src/api/routes.py`
4. Write tests in `tests/unit/` and `tests/integration/`
5. Update API documentation

### RAG Pipeline

The RAG (Retrieval-Augmented Generation) pipeline:
1. Embed user question
2. Search Qdrant for similar content chunks
3. Pass question + retrieved context to Gemini LLM
4. Extract citations from retrieved chunks
5. Store conversation in PostgreSQL
6. Return response with citations

## Deployment

### Docker

```bash
docker build -t chatbot-backend:latest .
docker run -p 8000:8000 \
  -e NEON_DATABASE_URL=postgresql://... \
  -e QDRANT_URL=https://... \
  -e QDRANT_API_KEY=... \
  -e GEMINI_API_KEY=... \
  chatbot-backend:latest
```

### Production Checklist

- [ ] Environment variables set in production
- [ ] Database connection pooling configured
- [ ] API rate limiting enabled
- [ ] Error logging and monitoring configured
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Health check endpoint monitored
- [ ] CORS origins configured correctly
- [ ] Secrets not exposed in code/logs

## Monitoring

Service health check endpoint:
```bash
curl http://localhost:8000/api/v1/health
```

Logs are structured JSON for easy parsing:
```bash
tail -f logs/chatbot.log | jq
```

## Troubleshooting

### Database Connection Error
- Verify `NEON_DATABASE_URL` is correct
- Check network connectivity to Neon
- Ensure connection pooling limits not exceeded

### Qdrant Connection Error
- Verify `QDRANT_URL` and `QDRANT_API_KEY`
- Ensure collection exists in Qdrant
- Check network connectivity

### Gemini API Error
- Verify `GEMINI_API_KEY` is valid
- Check API quota and rate limits
- Verify request format matches API specification

## Contributing

1. Create feature branch: `git checkout -b feature-name`
2. Make changes and add tests
3. Run tests: `pytest tests/ -v`
4. Commit: `git commit -m "description"`
5. Push and create pull request

## License

MIT

## Support

For issues and questions, open an issue in the GitHub repository.

---

**Status**: Phase 1 Setup Complete
**Next**: Phase 2 - Foundational Infrastructure
**Documentation**: See `/docs/DEVELOPMENT.md` for detailed development guide
