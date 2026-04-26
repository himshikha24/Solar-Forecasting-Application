
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

os.environ['API_KEY'] = os.getenv("OPENAI_API_KEY")


def create_sql_agent():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "Database", "solar.db")

    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    prompt = PromptTemplate.from_template("""
You are an agent designed to interact with a SQL database.

You have access to the following tools:
{tools}

Use the following format:

Question: the input question
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: input to the action
Observation: result of the action
Thought: I now know the final answer
Final Answer: the answer

Question: {input}
{agent_scratchpad}
""")

    agent = create_react_agent(
        llm=llm,
        tools=toolkit.get_tools(),
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
        verbose=False
    )

    return agent_executor
