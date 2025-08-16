import os
import re
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

db = SQLDatabase.from_uri("sqlite:///shop.db")  
sql_chain = create_sql_query_chain(llm, db)


st.set_page_config(page_title="Text to SQL with Gemini & LangChain")
st.title("LangChain + Gemini SQL Chatbot")

question = st.text_input("Ask a question about your data:")

if st.button("Generate and Run SQL"):
    try:
        # Step 1: Generate SQL from question
        result = sql_chain.invoke({"question": question})

        # Extract SQL from LangChain output
        if isinstance(result, dict) and "query" in result:
            generated_sql = result["query"]
        else:
            generated_sql = str(result)

        # Step 2: Clean the SQL
        # Remove markdown code fences ```sql ... ```
        generated_sql = re.sub(r"```sql|```", "", generated_sql, flags=re.IGNORECASE).strip()
        # Remove any accidental "Question:" or explanation text
        if "SELECT" in generated_sql.upper():
            generated_sql = generated_sql[generated_sql.upper().find("SELECT"):]
        elif "PRAGMA" in generated_sql.upper():
            generated_sql = generated_sql[generated_sql.upper().find("PRAGMA"):]
        elif "INSERT" in generated_sql.upper():
            generated_sql = generated_sql[generated_sql.upper().find("INSERT"):]
        elif "UPDATE" in generated_sql.upper():
            generated_sql = generated_sql[generated_sql.upper().find("UPDATE"):]
        elif "DELETE" in generated_sql.upper():
            generated_sql = generated_sql[generated_sql.upper().find("DELETE"):]

        st.subheader("Generated SQL:")
        st.code(generated_sql, language="sql")

        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute(generated_sql)
        rows = cursor.fetchall()
        conn.close()

        # Step 4: Display results
        st.subheader("Query Results:")
        if rows:
            st.dataframe(rows)
        else:
            st.info("No results found.")

    except Exception as e:
        st.error(f"Error: {e}")
