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
│   │   ├── fetch_news.py               # API endpoints
│   │   ├── relevance_score.py
│   │   └── verification.py
│   │
│   ├── graph/
│   │   ├── builder.py              # Builds LangGraph
│   │   ├── state.py                # NewsState
│   │   ├── nodes.py                # Utility nodes
│   │
│   ├── agents/
│   │   ├── 
│   │   ├── 
│   │   └── 
│   │
│   ├── memory/
│   │   ├── load_memory.py          # Load LTM
│   │   ├── update_memory.py        # Update LTM
│   │   ├── repository.py           # Memory interface
│   │   ├── sqlite_repository.py
│   │   └── memory_models.py
│   │
│   ├── llms/
│   │   ├── llms.py             # LLM factory
│   │
│   ├── prompts/
│   │   ├── prompts.py
│   │
│   ├── schemas/
│   │   ├── schemas.py
│   │
│   ├── utils/
│   │   ├── deduplicate.py
│   │   ├── filter_relevant_news.py
│   │   ├── filter_relevant_verified_news.py
│   │   ├── formatter.py
│   │   └── re_ranking.py
│   │
│   ├── config/
│   │   ├── 
│   │   └── 
│   │
│   └── database/
│       ├── 
│       └── 
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