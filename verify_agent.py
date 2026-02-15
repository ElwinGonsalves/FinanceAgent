from dotenv import load_dotenv
import os
import sys

# Ensure we can import from the directory
sys.path.append(os.getcwd())

# No try-except for import to let it crash and show traceback
from finance_agent.agent import initialize_agent

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY not found.")
    sys.exit(1)

print("Initializing Agent...")
try:
    agent_executor = initialize_agent()
    print("Agent Initialized.")
    
    input_text = "Give me financial details for India."
    print(f"Running query: {input_text}")
    
    response = agent_executor.invoke({"input": input_text})
    print("\n--- Agent Response ---")
    print(response["output"])
    print("\n--- End Response ---")
    print("Verification Successful.")
except Exception as e:
    print(f"Verification Failed: {e}")
