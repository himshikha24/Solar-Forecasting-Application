import pandas as pd
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def create_pandas_agent(df):

    def run_query(query: str, chat_history=None):

        try:
            history_text = ""

            if chat_history:
                for msg in chat_history[-5:]:  # last 5 messages
                    history_text += f"{msg['role']}: {msg['content']}\n"

            prompt = f"""
You are a data analyst working with a pandas DataFrame called df.

Previous conversation:
{history_text}

Columns:
{list(df.columns)}

Convert the user question into pandas code.

Rules:
- Only use df
- Return ONLY python code
- No explanation

User Question:
{query}
"""

            response = llm.invoke(prompt)

            code = response.content.strip()
            code = code.replace("```python", "").replace("```", "").strip()

            local_vars = {"df": df}
            result = eval(code, {}, local_vars)

            return result

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    return run_query