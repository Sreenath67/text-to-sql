#  Text-to-SQL with Streamlit & LangChain

This project is a **Text-to-SQL web application** built with **Streamlit** and **LangChain**, powered by **Google Generative AI (Gemini)**.  
It allows users to ask natural language questions about their data, automatically **generates SQL queries**, and also **executes those queries** on the connected database to return results.

Live Demo: [https://textto-sql.streamlit.app/](https://textto-sql.streamlit.app/)

---

## Features
- Convert natural language questions into SQL queries.
- Execute the generated SQL queries directly on the database.
- View both the generated SQL and the query results.
- Simple Streamlit-based UI for easy interaction.
- Powered by **LangChain** and **Google Generative AI (Gemini)**.

---

## 🛠️ Tech Stack
- **Frontend/UI:** [Streamlit](https://streamlit.io)
- **LLM & Orchestration:** [LangChain](https://www.langchain.com/)
- **LLM Provider:** Google Generative AI (Gemini)
- **Database:** SQLite (example, can be replaced with your own DB)
- **Deployment:** Streamlit Cloud (Free hosting)

---

## 📂 Project Structure
.
├── sql.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── .streamlit/
│ └── secrets.toml # Environment variables (API key, DB config)
└── README.md # Project documentation

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sreenath67/text-to-sql.git
   cd text-to-sql
   
Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


Install dependencies
pip install -r requirements.txt
Set up environment variables


Create a .streamlit/secrets.toml file:
GOOGLE_API_KEY = "your_google_api_key_here"
Get your API key from: Google AI Studio

▶️ Running Locally:
streamlit run sql.py
🌐 Deployment:
This project is deployed for free using Streamlit Cloud.

Steps to deploy:

Push your code to GitHub.

Go to Streamlit Cloud and create a new app.

Connect your repo and select sql.py as the entry point.

Add your GOOGLE_API_KEY in the Streamlit Secrets Manager under .streamlit/secrets.toml.

📊 Example
Question:
👉 "What are the different tables in the database?"

Generated SQL:

SELECT name FROM sqlite_master WHERE type='table';


Executed Result:
[('users',), ('orders',), ('products',)]



