# ResearchMind

An AI-powered research assistant that combines advanced language models with web search capabilities to deliver comprehensive research insights.

## Overview

ResearchMind leverages cutting-edge technologies to perform intelligent research tasks:
- **Groq LLM**: Fast, efficient language model for processing and analysis
- **Tavily Search**: Real-time web search for current information
- **LangChain**: Orchestration framework for AI workflows
- **FastAPI**: High-performance backend API
- **Streamlit**: Intuitive web interface for interactions

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Streamlit
- **AI/ML**: LangChain, Groq, Tavily, Pydantic
- **Testing**: Pytest, Pytest-asyncio
- **Code Quality**: Black, Ruff

## Project Structure

```
ResearchMind/
├── backend/                  # FastAPI backend application
│   ├── api/                 # API routes and endpoints
│   ├── models/              # Pydantic data models and schemas
│   ├── services/            # Business logic and external integrations
│   ├── utils/               # Utility functions and logging
│   ├── main.py              # Application entry point
│   └── config.py            # Configuration management
├── frontend/                # Streamlit frontend application
│   ├── pages/               # Page components
│   ├── components/          # Reusable UI components
│   └── app.py               # Main Streamlit app
├── tests/                   # Test suite
│   ├── test_api.py          # API endpoint tests
│   └── test_services.py     # Service layer tests
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore configuration
└── README.md               # This file
```

## Installation

### Prerequisites

- Python 3.9+
- pip or conda
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/silyones/ResearchMind.git
   cd ResearchMind
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configurations
   ```

5. **Run the application**

   **Backend:**
   ```bash
   cd backend
   python main.py
   # OR
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

   **Frontend (in another terminal):**
   ```bash
   cd frontend
   streamlit run app.py
   ```

## Configuration

Environment variables are managed through `.env` file. Copy `.env.example` to `.env` and configure:

- `GROQ_API_KEY`: Your Groq API key
- `TAVILY_API_KEY`: Your Tavily API key
- `LLM_MODEL`: Language model to use
- `TEMPERATURE`: Model temperature setting
- `MAX_TOKENS`: Maximum tokens for responses

## API Documentation

Once the backend is running, access interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:

```bash
pytest tests/ -v
pytest tests/ -v --cov=backend
```

## Development

### Code Style

Format code with Black:
```bash
black backend/ frontend/ tests/
```

Lint with Ruff:
```bash
ruff check backend/ frontend/ tests/
```

### Adding Dependencies

Add new dependencies to `requirements.txt` and install:
```bash
pip install package_name
pip freeze > requirements.txt
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run code quality checks
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Streamlit, and LangChain**
