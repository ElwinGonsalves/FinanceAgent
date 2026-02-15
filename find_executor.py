import os

# Define the path to langchain
langchain_path = r"C:\Users\ELWIN G\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\site-packages\langchain"

print(f"Searching in {langchain_path}...")

for root, dirs, files in os.walk(langchain_path):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "class AgentExecutor" in content:
                        print(f"Found AgentExecutor in: {path}")
            except Exception as e:
                pass
print("Search complete.")
