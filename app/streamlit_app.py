import streamlit as st
from src.data_loader import load_data
from src.preprocessing import preprocess
from src.pandas_agent import create_pandas_agent
from src.sql_agent import create_sql_agent
from src.router import route_query
from src.tools import run_forecast, run_anomaly

#PAGE CONFIG 
st.set_page_config(page_title="Solar AI Analyst", layout="wide")

# CUSTOM CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        .stTextInput > div > div > input {
            padding: 12px;
            border-radius: 10px;
        }

        .main {
            max-width: 900px;
            margin: auto;
        }

        .stPlotlyChart, .stLineChart, .stBarChart {
            margin-top: 20px;
            margin-bottom: 20px;
        }

        h1, h2, h3 {
            margin-top: 1rem;
            margin-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)


#  LOAD DATA
df = preprocess(load_data())


#LANGCHAIN SETTINGS
from langchain.globals import set_verbose, set_debug
set_verbose(False)
set_debug(False)


# CACHE AGENTS 
@st.cache_resource
def load_agents():
    pandas_agent = create_pandas_agent(df)
    sql_agent = create_sql_agent()
    return pandas_agent, sql_agent

pandas_agent, sql_agent = load_agents()


# SIDEBAR #
st.sidebar.title("⚡ Solar AI System")

option = st.sidebar.radio(
    "Select Mode",
    ["💬 Chat with Data", "📊 Dashboard"]
)


#CHAT MODE #
if option == "💬 Chat with Data":

    st.title("💬 AI Solar Data Analyst")

    # ✅ Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ✅ Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✅ Chat input (replaces text_input + button)
    query = st.chat_input("Ask your question...")

    if query:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                try:
                    route = route_query(query)

                    if route == "sql":
                        response = sql_agent.invoke({"input": query})
                        output = response.get("output", str(response))

                    elif route == "forecast":
                        output = run_forecast(df)

                    elif route == "anomaly":
                        output = run_anomaly(df)

                    else:
                        try:
                            # ✅ FIX: remove .run()
                            output = pandas_agent(query, st.session_state.messages)
                        except:
                            output = "Try a simpler question."

                    st.markdown(output)

                    # ✅ Save assistant response
                    st.session_state.messages.append(
                        {"role": "assistant", "content": str(output)}
                    )

                except Exception as e:
                    st.error("⚠️ Something went wrong. Try again.")
                    print("DEBUG:", e)

#  DASHBOARD MODE
elif option == "📊 Dashboard":

    st.title("📊 Solar Dashboard")

    # Power Generation
    st.subheader("⚡ Power Generation Over Time")
    st.line_chart(df.set_index('DATE_TIME')['AC_POWER'])

    #Irradiation vs Power
    st.subheader("🌤️ Irradiation vs Power")
    st.scatter_chart(df[['IRRADIATION', 'AC_POWER']])

    # Temperature 
    st.subheader("🌡️ Temperature Trends")
    st.line_chart(
        df.set_index('DATE_TIME')[['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE']]
    )

    # Optional Metrics 
    st.subheader("📈 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Power", round(df["AC_POWER"].mean(), 2))
    col2.metric("Max Power", round(df["AC_POWER"].max(), 2))
    col3.metric("Avg Irradiation", round(df["IRRADIATION"].mean(), 2))