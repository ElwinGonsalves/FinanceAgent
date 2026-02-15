import streamlit as st
import json
import os
from dotenv import load_dotenv

# Import Agent
try:
    from agent import initialize_agent
except ImportError:
    from finance_agent.agent import initialize_agent

# Load environment variables (Local)
load_dotenv(override=True)

# Load environment variables (Streamlit Cloud)
# Streamlit Cloud stores secrets in st.secrets, not always os.environ.
# We manually inject them to ensure tools usage of os.getenv works.
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if "EXCHANGERATE_API_KEY" in st.secrets:
    os.environ["EXCHANGERATE_API_KEY"] = st.secrets["EXCHANGERATE_API_KEY"]

# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Intelligence Agent",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (UI/UX Pro Max) ---
# Dark mode optimized, clean typography, card-like containers
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #1E293B; /* Slate 800 */
        border: 1px solid #334155; /* Slate 700 */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: #6366F1; /* Indigo 500 */
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC; /* Slate 50 */
    }
    
    /* Custom Card for Results */
    .result-card {
        background-color: #0F172A; /* Slate 900 */
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* JSON Block */
    .stJson {
        background-color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("💸 Financial Intelligence Agent")
st.markdown("### Real-time Market Insights & Currency Data powered by Groq Llama 3")
st.markdown("---")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠️ GROQ_API_KEY missing in .env")
        st.info("Please add your API key to continue.")
    else:
        st.success("API Key Detected ✅")

    st.markdown("### Target Country")
    target_country = st.text_input("Enter Country Name", value="India", placeholder="e.g., Japan, USA, UK")
    
    st.markdown("---")
    st.markdown("**Capabilities:**")
    st.markdown("- 💱 Exchange Rates (USD/INR/GBP/EUR)")
    st.markdown("- 📈 Stock Indices (Values & Changes)")
    st.markdown("- 📍 HQ Location Maps")
    
    run_btn = st.button("Generate Intelligence", type="primary", use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 🛠️ Debugging")
    if st.button("Test Currency Tool"):
        from tools.currency import get_exchange_rates
        try:
            res = get_exchange_rates(target_country)
            st.code(res, language="json")
        except Exception as e:
            st.error(f"Tool Error: {e}")
            
    if st.button("Check Secrets"):
        st.write("Checking environment variables...")
        groq_status = "✅ Found" if os.environ.get("GROQ_API_KEY") else "❌ Missing"
        er_status = "✅ Found" if os.environ.get("EXCHANGERATE_API_KEY") else "❌ Missing"
        
        st.write(f"GROQ_API_KEY: {groq_status}")
        st.write(f"EXCHANGERATE_API_KEY: {er_status}")
        
        # Check raw st.secrets for debugging cloud
        if "EXCHANGERATE_API_KEY" in st.secrets:
            st.write("Secret exists in st.secrets")
            # Show first 4 chars to verify it's not empty/wrong
            key_preview = st.secrets["EXCHANGERATE_API_KEY"][:4] + "..."
            st.code(f"Key Preview: {key_preview}")
        else:
            st.write("Secret NOT found in st.secrets")

# --- Main Logic ---

if run_btn and target_country:
    if not api_key:
        st.error("Please configure your Groq API Key first.")
        st.stop()

    agent_executor = initialize_agent()

    # Define the prompt based on user specs
    prompt_text = (
        f"Give me full financial intelligence for {target_country}. "
        "1. Official Currency Name & Code. "
        "2. Exchange rates for 1 unit of this currency to USD, INR, GBP, EUR. "
        "3. Major Stock Indices with current values. "
        "4. Google Maps link for the Stock Exchange HQ. "
        "Return the final answer as a structured JSON object with keys: "
        "'currency', 'exchange_rates', 'stock_indices', 'maps_link'."
    )

    # Define the system prompt
    system_prompt = (
        "You are an expert Financial Intelligence Agent. "
        "Your goal is to provide accurate financial data for a given country. "
        "You MUST use the provided tools to get exchange rates, stock indices, and location links. "
        "Do not make up data. If a tool returns specific data, use it exactly. "
        "Output the final answer as a structured summary, but you can also include the raw JSON in a code block if requested."
    )

    with st.status("🤖 Analyzing Financial Data...", expanded=True) as status:
        st.write("🔍 Identifying Jurisdiction...")
        st.write("💱 Fetching Exchange Rates...")
        st.write("📈 Aggregating Market Indices...")
        
        try:
            # We ask the agent to return JSON in its final text
            # LangGraph usage: invoke({"messages": [("system", system_prompt), ("user", prompt_text)]})
            response = agent_executor.invoke({"messages": [("system", system_prompt), ("user", prompt_text)]})
            # Response is a state dict, key 'messages' has the conversation history.
            # The last message is the AI's final answer.
            output_text = response["messages"][-1].content
            status.update(label="Analysis Complete!", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Agent execution failed: {str(e)}")
            st.stop()

    # --- Display Results ---
    
    # Try to parse JSON from output if the agent followed instructions well
    # The agent might wrap it in ```json ... ```
    import re
    json_match = re.search(r"```json\s*(\{.*?\})\s*```", output_text, re.DOTALL)
    
    if json_match:
        data_str = json_match.group(1)
        try:
            data = json.loads(data_str)
            
            # 1. Currency Section
            currency_data = data.get('currency', {})
            if isinstance(currency_data, str):
                currency_name = currency_data
                currency_code = "N/A"
            else:
                currency_name = currency_data.get('name', 'N/A')
                currency_code = currency_data.get('code', 'N/A')
            
            data_source = data.get('source', 'Mock Data')
            source_color = "green" if data_source == "Live API" else "orange"
            
            st.subheader(f"💱 Currency: {currency_name} ({currency_code})")
            st.markdown(f":{source_color}[Source: {data_source}]")
            
            cols = st.columns(4)
            rates = data.get('exchange_rates', {})
            currencies = ["USD", "INR", "GBP", "EUR"]
            for idx, curr in enumerate(currencies):
                if curr in rates:
                    cols[idx].metric(f"To {curr}", f"{rates[curr]}")
            
            st.markdown("---")
            
            # 2. Stocks Section
            st.subheader("📈 Major Stock Indices")
            indices = data.get('stock_indices', [])
            
            # If indices is a dict (mock tool returns dict sometimes), normalize it
            if isinstance(indices, dict): 
                # Handle structured dict if Agent reformats it
                pass 
            elif isinstance(indices, list):
                s_cols = st.columns(len(indices) if len(indices) <= 3 else 3)
                for i, idx in enumerate(indices):
                    col = s_cols[i % 3]
                    col.metric(
                        label=idx.get('name', 'Index'),
                        value=f"{idx.get('value', 0):,}",
                        delta=idx.get('change', None)
                    )
            
            st.markdown("---")

            # 3. Maps Section
            st.subheader("📍 Stock Exchange HQ")
            maps_link = data.get('maps_link', '#')
            st.link_button("View on Google Maps 🗺️", maps_link)

        except json.JSONDecodeError:
            st.warning("Could not parse structured JSON. Showing raw agent output below.")
            st.markdown(output_text)
    else:
        # Fallback if no JSON block found
        st.markdown(output_text)

    # Debug Section
    with st.expander("🛠️ Debug Information"):
        st.text("Raw Agent Response:")
        st.write(output_text)

elif run_btn and not target_country:
    st.warning("Please enter a country name.")
