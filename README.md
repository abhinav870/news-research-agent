1) PROJECT ARCHITECTURE:

                  FastAPI
                      │
                      ▼
             LangGraph Workflow
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Load LTM                Load STM
          │
          ▼
    Validate Request
          │
          ▼
     News Fetch Agent
          │
          ▼
 Normalize to NewsArticleCollection
          │
          ▼
 Relevance Filter Agent (LLM)
 (score + reason + reject/accept )
          │
          ▼
   Filter Irrelevant News
          │
          ▼
   Deduplicate (Utility)
          │
          ▼
  Verify News Agent
          │
          ▼
Rank Results (Utility)
          │
          ▼
   News Format Agent
          │
          ▼
 Update LTM (LLM + Repository)
          │
          ▼
      Save STM
          │
          ▼
          END


2) PROJECT FILES HEIRARCHY:

news-research-agent/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
├── main.py                         # Entry point (CLI testing)
│
├── app/
│   │
│   ├── api/
│   │   ├── app.py                  # FastAPI application
│   │   ├── routes.py               # API endpoints
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   ├── graph/
│   │   ├── builder.py              # Builds LangGraph
│   │   ├── state.py                # NewsState
│   │   ├── nodes.py                # Utility nodes
│   │   └── edges.py                # Conditional routing (if needed)
│   │
│   ├── agents/
│   │   ├── fetch_agent.py
│   │   ├── verify_agent.py
│   │   └── format_agent.py
│   │
│   ├── memory/
│   │   ├── load_memory.py          # Load LTM
│   │   ├── update_memory.py        # Update LTM
│   │   ├── repository.py           # Memory interface
│   │   ├── sqlite_repository.py
│   │   └── memory_models.py
│   │
│   ├── llms/
│   │   ├── provider.py             # LLM factory
│   │   ├── groq.py
│   │   └── huggingface.py
│   │
│   ├── prompts/
│   │   ├── fetch_prompt.py
│   │   ├── verification_prompt.py
│   │   ├── formatting_prompt.py
│   │   └── memory_prompt.py
│   │
│   ├── schemas/
│   │   ├── request_schema.py
│   │   ├── fetched_news.py
│   │   ├── verified_news.py
│   │   ├── formatted_news.py
│   │   ├── memory_schema.py
│   │   └── state_schema.py
│   │
│   ├── services/
│   │   ├── twitter_service.py
│   │   ├── verification_service.py
│   │   └── ranking_service.py
│   │
│   ├── utils/
│   │   ├── parser.py
│   │   ├── deduplicator.py
│   │   ├── logger.py
│   │   ├── constants.py
│   │   └── helpers.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── langsmith.py
│   │
│   └── database/
│       ├── news_memory.db
│       └── init_db.py
│
├── tests/
│   ├── test_fetch_agent.py
│   ├── test_verify_agent.py
│   ├── test_format_agent.py
│   ├── test_memory.py
│   └── test_api.py
│
└── notebooks/
    └── experiments.ipynb