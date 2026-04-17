# AI Career Agent - Intelligent Job Search Platform

A full-stack AI-powered SaaS that helps job seekers find matching jobs, generate cover letters, and prepare for interviews.

## Features
- Resume upload and skill extraction
- Job scraping from multiple sources
- ML-powered job matching and ranking
- AI cover letter generation
- Interview simulation with feedback
- Career gap analysis

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and add your OpenAI API key
3. Run `docker-compose -f docker/docker-compose.yml up --build`
4. Access the app at http://localhost:8501

## Architecture
Microservices architecture with FastAPI, PostgreSQL, Redis, FAISS vector search, and LangChain agents.

## Services
- User Service (auth, resume management)
- ML Service (embeddings, matching, ranking)
- LLM Agent Service (cover letters, interviews)
- Scraper Service (job collection)
- Analytics Service (feedback tracking)

## Tech Stack
- Backend: FastAPI, SQLAlchemy, Pydantic
- ML: Sentence-Transformers, FAISS, XGBoost
- LLM: OpenAI GPT, LangChain
- Database: PostgreSQL, Redis
- Frontend: Streamlit
- Deployment: Docker, Nginx