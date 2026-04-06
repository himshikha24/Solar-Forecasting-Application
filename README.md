# ⚡ Solar Forecasting GenAI Application

## 🚀 Features

### 💬 Chat with Data (GenAI Interface)
- Ask questions in natural language
- Supports multi-turn conversations (chat history)
- Context-aware responses
- Powered by OpenAI LLM

### 📊 Smart Data Analysis
- Pandas-based intelligent query execution
- Automatic conversion of user queries → Python code
- Handles filtering, aggregation, trends, and insights

### 🗄️ SQL Agent Integration
- Query structured database using natural language
- SQLite database integration
- Supports analytical queries across datasets

### 📈 Dashboard Visualization
- Power generation trends
- Irradiation vs power analysis
- Temperature insights
- Key performance metrics

### 🔮 Forecasting Module
- Predict future solar power generation
- Time-series based modeling

### 🚨 Anomaly Detection
- Detect abnormal patterns in solar data
- Useful for monitoring system failures

---

## 🛠️ Tech Stack

### 👨‍💻 Languages
- Python

### 📚 Libraries & Frameworks
- Streamlit (UI)
- Pandas (data processing)
- NumPy
- SQLAlchemy (database)
- SQLite (local database)
- OpenAI API (LLM)
- LangChain (for SQL agent)

### 🤖 AI/ML
- LLM-based query understanding
- Time-series forecasting
- Anomaly detection models

# ⚡ Solar Forecasting GenAI Application

An intelligent AI-powered analytics system for solar power data that enables users to interact with data using natural language queries, perform forecasting, anomaly detection, and visualize insights in real-time.

---

## 🚀 Features

### 💬 Chat with Data (GenAI Interface)
- Ask questions in natural language
- Supports multi-turn conversations (chat history)
- Context-aware responses
- Powered by OpenAI LLM

### 📊 Smart Data Analysis
- Pandas-based intelligent query execution
- Automatic conversion of user queries → Python code
- Handles filtering, aggregation, trends, and insights

### 🗄️ SQL Agent Integration
- Query structured database using natural language
- SQLite database integration
- Supports analytical queries across datasets

### 📈 Dashboard Visualization
- Power generation trends
- Irradiation vs power analysis
- Temperature insights
- Key performance metrics

### 🔮 Forecasting Module
- Predict future solar power generation
- Time-series based modeling

### 🚨 Anomaly Detection
- Detect abnormal patterns in solar data
- Useful for monitoring system failures

---

## 🛠️ Tech Stack

### 👨‍💻 Languages
- Python

### 📚 Libraries & Frameworks
- Streamlit (UI)
- Pandas (data processing)
- NumPy
- SQLAlchemy (database)
- SQLite (local database)
- OpenAI API (LLM)
- LangChain (for SQL agent)

### 🤖 AI/ML
- LLM-based query understanding
- Time-series forecasting
- Anomaly detection models

## ⚙️ How It Works

1. User enters a query in the chat interface
2. Query is routed using intelligent routing:
   - SQL queries → SQL Agent
   - Forecast queries → Forecast module
   - Anomaly queries → Anomaly module
   - Other queries → Pandas Agent

3. Pandas Agent:
   - Converts natural language → Python (Pandas) code
   - Executes safely on DataFrame
   - Returns result

4. SQL Agent:
   - Converts query → SQL
   - Executes on SQLite database

5. Results are displayed in:
   - Chat interface
   - Dashboard (for visualization)

---

## 🧠 Chat History & Memory

- Maintains session-based chat history
- Enables contextual follow-up questions
- Improves response accuracy

---

