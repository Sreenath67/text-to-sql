import os
import re
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)

schema_description = """
Database name: shop.db
Tables:
1. users(user_id INTEGER PRIMARY KEY, name TEXT, age INTEGER, phone_number TEXT)
2. products(product_id INTEGER PRIMARY KEY, product_name TEXT, price REAL)
3. orders(order_id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, order_date TEXT)

Relationships:
- orders.user_id → users.user_id
- orders.product_id → products.product_id
"""

sql_prompt = PromptTemplate(
    input_variables=["question", "schema"],
    template="""
You are a SQL expert. Write a valid SQLite query ONLY. 
Use the following database schema:

{schema}

Question: {question}

Return only the SQL query. Do not include explanations, comments, or markdown.
"""
)

# Build the chain
sql_chain = LLMChain(llm=llm, prompt=sql_prompt)

#  Streamlit UI 
st.set_page_config(page_title="Text to SQL with Gemini & LangChain ")
st.title("LangChain + Gemini SQL Chatbot")

question = st.text_input("Ask a question about your data:")

if st.button("Generate and Run SQL"):
    try:
        # Generate SQL 
        result = sql_chain.invoke({"question": question, "schema": schema_description})#dict
        generated_sql = result["text"]   # extract the actual SQL string

        # Clean SQL
        generated_sql = re.sub(r"```sql|```", "", generated_sql, flags=re.IGNORECASE).strip()
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

        # Show generated query
        st.subheader("Generated SQL:")
        st.code(generated_sql, language="sql")

        # Run query
        conn = sqlite3.connect("shop.db")
        cursor = conn.cursor()
        cursor.execute(generated_sql)
        rows = cursor.fetchall()
        conn.close()

        # Display results
        st.subheader("Query Results:")
        if rows:
            st.dataframe(rows)
        else:
            st.info("No results found.")

    except Exception as e:
        st.error(f"Error: {e}")
