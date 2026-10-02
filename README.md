# unikX AI Studio

A Streamlit chat app powered by Groq. It supports text chat, photo analysis, voice transcription, and copying assistant replies.

## Run locally

1. Install Python 3.11 or newer.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create `.streamlit/secrets.toml` with your Groq API key:

   ```toml
   GROQ_API_KEY = "your-groq-api-key"
   ```

4. Start the app:

   ```powershell
   streamlit run ai.py
   ```

The secrets file is excluded by `.gitignore`. Never commit API keys; configure `GROQ_API_KEY` in your hosting provider's secret settings when deploying.
