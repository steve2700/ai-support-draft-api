# AI-Powered FAQ Generator API

A modern, scalable FastAPI backend application that leverages OpenAI's GPT models to generate helpful FAQ answers automatically. This project demonstrates full integration of AI with a robust backend and database, perfect for startups and businesses seeking to automate customer support content.

---

## Features

- ✅ **AI-generated FAQ answers** using OpenAI GPT-4o-mini (chat completions)  
- ✅ Create, read, search, and paginate FAQs stored in a PostgreSQL database  
- ✅ Built with FastAPI for blazing fast performance and automatic Swagger UI docs  
- ✅ SQLAlchemy ORM for database interactions with PostgreSQL (can use Supabase)  
- ✅ Environment variables support with `.env` for secure API keys and configs  
- ✅ Automatic saving of AI-generated FAQs to minimize repeated token usage  
- ✅ Input validation and error handling for robust API experience  

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11+  
- **AI Integration:** OpenAI Python SDK (latest)  
- **Database:** PostgreSQL (via SQLAlchemy ORM)  
- **Deployment Ready:** Docker, CI/CD (optional to add)  
- **Others:** Pydantic, dotenv for config management  

---

## Getting Started

### Prerequisites

- Python 3.11+  
- PostgreSQL database or Supabase instance  
- OpenAI API key ([sign up for free](https://platform.openai.com/signup))  

### Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/ai-faq-generator.git
   cd ai-faq-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=your_postgresql_connection_string_here
   ```

5. Initialize the database:
   ```bash
   python -m app.db.init_db
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Open http://127.0.0.1:8000/docs to access the Swagger UI and test the API.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/faqs/` | Create a new FAQ manually |
| GET | `/api/faqs/` | Get list of FAQs with pagination & search |
| POST | `/api/faqs/generate` | Generate an answer via AI & save to DB |

### Example Request for AI-generated FAQ

```bash
curl -X POST "http://127.0.0.1:8000/api/faqs/generate" \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I reset my password?"}'
```

### Response

```json
{
  "id": 1,
  "question": "How do I reset my password?",
  "answer": "To reset your password, follow these steps: ..."
}
```

---

## Contributing

Feel free to open issues or submit pull requests to improve this project.

---

## License

MIT License © Stewie

---

## Contact
nyaruwatastewart27@gmail.com

Built with ❤️ using FastAPI & OpenAI API
