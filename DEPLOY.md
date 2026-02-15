# Deploying to Streamlit Cloud ☁️

This guide will help you deploy the **Financial Intelligence Agent** to Streamlit Cloud for free.

## 1. Prerequisites
- A GitHub account.
- A Streamlit Cloud account (sign up at [share.streamlit.io](https://share.streamlit.io/)).

## 2. Push Code to GitHub
1.  Initialize a git repository in your project folder:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Push your code:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git branch -M main
    git push -u origin main
    ```

## 3. Deploy on Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your repository, branch (`main`), and the main file path:
    - **Main file path**: `finance_agent/app.py` (if you pushed the whole folder) OR just `app.py` (if you pushed only the contents of `finance_agent` to root).

## 4. Configure Secrets (CRITICAL) 🔑
Streamlit Cloud does NOT read your `.env` file. You must add your API keys manually.

1.  In your deployed app dashboard, go to **Settings** -> **Secrets**.
2.  Copy the contents below into the secrets text area:

```toml
GROQ_API_KEY = "your_actual_groq_key_here"
EXCHANGERATE_API_KEY = "your_actual_exchange_key_here"
```

3.  Click **Save**.

## 5. Verify
- The app should restart automatically.
- Check the "Source" badge in the app to confirm it's using the "Live API".

## 🚀 Troubleshooting
- If you see `ModuleNotFoundError`, check your directory structure.
- If the app says "Mock Data", check your Secrets spelling.
