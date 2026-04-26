import streamlit as st
from src.data_loader import load_data
from src.preprocessing import preprocess
from src.pandas_agent import create_pandas_agent
from src.sql_agent import create_sql_agent
from src.router import route_query
from src.tools import run_forecast, run_anomaly, check_asset_health, get_weather
from src.weather_api import get_weather_forecast
from src.anomaly import detect_underperforming_assets

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
    ["💬 Chat with Data", "📊 Dashboard", "⛅ Scenario Simulator"]
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

                    elif route == "weather":
                        output = get_weather()

                    elif route == "health":
                        output = check_asset_health(df)

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

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Avg Power", round(df["AC_POWER"].mean(), 2))
    col2.metric("Max Power", round(df["AC_POWER"].max(), 2))
    col3.metric("Avg Irrad.", round(df["IRRADIATION"].mean(), 2))
    
    weather_data = get_weather_forecast()
    if weather_data and len(weather_data) > 0:
        tomorrow = weather_data[1] if len(weather_data) > 1 else weather_data[0]
        col4.metric("Tmrw High", f"{tomorrow['Max Temp (°C)']}°C")
        col5.metric("Tmrw Rain", f"{tomorrow['Precipitation (mm)']}mm")
        
    # Asset Health Indicator
    health_df = detect_underperforming_assets(df)
    if not health_df.empty:
        issues = health_df[health_df['Status'] != 'Healthy']
        if not issues.empty:
            st.warning(f"⚠️ {len(issues)} inverters flagged for potential maintenance or damage. Ask the Chatbot for details.")
        else:
            st.success("✅ All inverters are operating normally.")

# SCENARIO SIMULATOR MODE
elif option == "⛅ Scenario Simulator":

    st.title("⛅ Weather Scenario & Asset Monitoring")
    st.markdown("Simulate different weather conditions for upcoming days to assess forecasting implications and monitor generation capabilities.")
    
    st.sidebar.subheader("Scenario Parameters")
    days_ahead = st.sidebar.selectbox("Forecast Period", [1, 7], format_func=lambda x: "Tomorrow" if x==1 else "Next 7 Days")
    
    irr_adj = st.sidebar.slider("Irradiation Adjustment (%)", min_value=-100.0, max_value=100.0, value=0.0, step=5.0, help="Simulate heavy cloud cover (-%) or peak clear skies (+%)")
    amb_temp_adj = st.sidebar.slider("Ambient Temp Adjustment (°C)", -15.0, 15.0, 0.0, 1.0)
    mod_temp_adj = st.sidebar.slider("Module Temp Adjustment (°C)", -15.0, 15.0, 0.0, 1.0)

    from src.tools import run_scenario_simulation
    
    with st.spinner("Generating scenario future data..."):
        scenario_df = run_scenario_simulation(df, days_ahead, irr_adj, amb_temp_adj, mod_temp_adj)
    
    st.subheader(f"Predicted Power Generation ({'Tomorrow' if days_ahead==1 else 'Next 7 Days'})")
    
    chart_data = scenario_df.set_index('DATE_TIME')[['PREDICTED_AC_POWER']]
    st.line_chart(chart_data)
    
    # Asset Monitoring Alerts
    st.subheader("🛠️ Asset Monitoring Alerts")
    
    # Baseline comparison (average historic power)
    avg_historic_power = df['AC_POWER'].mean()
    avg_predicted_power = scenario_df['PREDICTED_AC_POWER'].mean()
    
    threshold_drop = 0.20 # 20% drop threshold
    
    col1, col2 = st.columns(2)
    col1.metric("Historical Avg Power Base", f"{avg_historic_power:.2f} kW")
    
    diff_percent = (avg_predicted_power - avg_historic_power) / avg_historic_power * 100
    col2.metric("Scenario Avg Predicted Power", f"{avg_predicted_power:.2f} kW", f"{diff_percent:.1f}%")
    
    if avg_predicted_power < (avg_historic_power * (1 - threshold_drop)):
        st.error(f"⚠️ **Asset Warning Alert**: Protected Plant Output drops by over {threshold_drop*100}% compared to historical baseline. Consider engaging backup energy reserves or scheduling asset inspection to prevent yield loss under these condition states.")
    elif avg_predicted_power > (avg_historic_power * 1.2):
        st.success(f"✅ **Peak Generation Alert**: Predicted scenarios point to over-generation. Asset systems should be prepared for high load. Potential for battery storage charging.")
    else:
        st.info("✔️ **Nominal Status**: Forecasted output under this scenario is within standard operating thresholds.")

    st.markdown("### Synthesized Scenario Data Sample")
    st.dataframe(scenario_df[['DATE_TIME', 'IRRADIATION', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'PREDICTED_AC_POWER']].head(10))