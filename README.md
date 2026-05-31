# Personal Investment Portfolio API 📈

A robust, production-ready RESTful API for tracking and managing personal investments (Mutual Funds, Stocks, Fixed Deposits, etc.). Built with FastAPI and SQLite.

## Features
* **Full CRUD Operations:** Create, Read, Update, and Delete investments.
* **Data Validation:** Strict input validation using Pydantic (e.g., preventing negative investment amounts).
* **Database Management:** Persistent SQLite database via SQLAlchemy ORM.
* **File Export:** Download your entire portfolio as a cleanly formatted `.csv` file.
* **Security:** `DELETE` operations are protected by API Key authentication.
* **Reliability:** Built-in application logging and a suite of unit tests.

## Tech Stack
* **Framework:** FastAPI
* **Database:** SQLite & SQLAlchemy
* **Server:** Uvicorn
* **Testing:** Pytest & HTTPX
* **Environment Management:** Python-dotenv

## Local Setup & Installation

**1. Clone the repository**
\`\`\`bash
git clone https://github.com/shreedev96/portfolio-api.git
cd portfolio-api
\`\`\`

**2. Create and activate a virtual environment**
* Windows: `python -m venv venv` then `venv\Scripts\activate`
* Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`

**3. Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**4. Set up Environment Variables**
Create a `.env` file in the root directory and add your secure API key:
\`\`\`text
SECRET_API_KEY=your_secret_key_here
\`\`\`

## Running the Application
Start the local server using Uvicorn:
\`\`\`bash
uvicorn main:app --reload
\`\`\`
* **Interactive API Docs (Swagger UI):** Navigate to `http://127.0.0.1:8000/docs` to interact with the API.

##  Running Tests
To run the automated test suite, ensure your virtual environment is active and run:
\`\`\`bash
pytest
\`\`\`