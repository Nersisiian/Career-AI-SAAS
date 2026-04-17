# 🧠 AI Career Agent – Intelligent Job Search SaaS

[![CI Pipeline](https://github.com/Nersisiian/Career-AI-SAAS/actions/workflows/ci.yml/badge.svg)](https://github.com/Nersisiian/Career-AI-SAAS/actions/workflows/ci.yml)

**AI Career Agent** – это полнофункциональная SaaS-платформа, которая помогает соискателям автоматизировать поиск работы с помощью искусственного интеллекта. Сервис анализирует резюме, находит подходящие вакансии, генерирует персонализированные сопроводительные письма и симулирует собеседования.

---

## 🚀 Возможности

- 📄 **Загрузка и анализ резюме** – извлечение навыков, опыта, образования с помощью NLP.
- 🔍 **Поиск вакансий** – скрапинг с популярных досок объявлений (симулированный).
- 🎯 **ML‑ранжирование** – подбор вакансий на основе эмбеддингов и XGBoost с учётом фидбека.
- ✍️ **AI‑генерация сопроводительных писем** – индивидуально под каждую вакансию (OpenAI).
- 🎤 **Симуляция собеседований** – вопросы с оценкой ответов.
- 📊 **Анализ карьерных пробелов** – рекомендации по развитию.
- 🧠 **Самообучение** – улучшение рекомендаций на основе действий пользователя.

---

## 🏗️ Архитектура

Проект построен по микросервисной архитектуре:

| Сервис               | Порт  | Технологии                                |
|----------------------|-------|--------------------------------------------|
| `user-service`       | 8001  | FastAPI, PostgreSQL, Redis, JWT            |
| `ml-service`         | 8002  | FastAPI, Sentence‑Transformers, FAISS, XGBoost |
| `llm-agent`          | 8003  | FastAPI, LangChain, OpenAI, ChromaDB       |
| `scraper-service`    | 8004  | FastAPI, BeautifulSoup, APScheduler        |
| `analytics-service`  | 8005  | FastAPI, PostgreSQL                        |
| `frontend`           | 8501  | Streamlit                                  |
| `nginx`              | 80    | API Gateway / Reverse Proxy                |

Все сервисы упакованы в Docker и управляются через `docker-compose`.

---

## 📦 Требования

- **Docker** и **Docker Compose** (версия 2+)
- OpenAI API ключ (для LLM‑функций)
- 4+ ГБ свободной оперативной памяти

---

## ⚡ Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/Nersisiian/Career-AI-SAAS.git
cd Career-AI-SAAS
