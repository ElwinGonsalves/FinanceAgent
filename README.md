# 💸 Financial Intelligence Agent

A real-time financial dashboard powered by **AI (Groq/Llama 3)**, **Streamlit**, and **LangGraph**. 

This agent provides instant financial insights for any country, including live currency exchange rates, major stock market indices, and headquarters locations.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-blue?style=for-the-badge)

## ✨ Features

- **🧠 AI-Powered Analysis**: Uses Groq (Llama 3 70B) to interpret user requests and format data.
- **💱 Live Currency Rates**: Fetches real-time exchange rates via *ExchangeRate-API* (auto-converts from EUR base).
- **📈 Stock Market Data**: Provides key stock indices for major economies (Mock/Static data for reliability).
- **📍 Location Intelligence**: Generates Google Maps links for Stock Exchange HQs.
- **⚡ Fast & Free**: Designed to run optimally on free-tier APIs.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (UI/UX Pro Max styling)
- **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful agent workflow)
- **LLM**: [Groq](https://groq.com/) (Llama-3.3-70b-versatile)
- **Data**: [ExchangeRate-API](https://www.exchangerate-api.com/) & Custom Tools

## 🚀 Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd finance_agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    - Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    - Add your API keys to `.env`:
        - `GROQ_API_KEY`: Get from [Groq Console](https://console.groq.com/).
        - `EXCHANGERATE_API_KEY`: Get from [ExchangeRate-API](https://www.exchangerate-api.com/).

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## ☁️ Deployment

Want to run this online? Check out our [Deployment Guide](DEPLOY.md) for step-by-step instructions on deploying to **Streamlit Cloud**.

## 📂 Project Structure

```
finance_agent/
├── app.py              # Main Streamlit application
├── agent.py            # LangGraph agent definition & LLM setup
├── tools/              # Custom tool definitions
│   ├── currency.py     # Currency fetching logic (Live + Mock)
│   ├── stocks.py       # Stock market data
│   └── maps.py         # Location data
├── requirements.txt    # Python dependencies
├── .env                # API Keys (Git-ignored)
└── DEPLOY.md           # Deployment instructions
```

## 📝 License

This project is open-source and available under the MIT License.
