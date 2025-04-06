# AI Music Agent

An AI-powered music assistant that creates personalized Spotify playlists using user top tracks.

## 🚀 Proof of Concept

### Test run of the Agent

![Test Image](/img/testrun.png "Image showing test run of the agent")

---

### 🔧 Setup Instructions

1. **Create and activate a virtual environment**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file**

    ```bash
    cp sample.env .env
    ```

4. **Get the required API keys**

    - [Groq API Key](https://console.groq.com/keys)
    - [Spotify API Key](https://developer.spotify.com/dashboard)
        - Add "https://google.com/" as redirect URI
    - [LangSmith API Key](https://smith.langchain.com/)

5. **Authorize Spotify access**

    ```bash
    python spotify.py
    ```

    - Click the URL shown in the terminal.
    - Log in and authorize access.
    - Copy the full redirected URL and paste it back in the terminal.
    - After successful authorization, you’ll see:

    ```
    Spotify User ID: <Your User ID>
    ```

6. **Run the main AI Agent**

    ```bash
    python main.py
    ```

---

### 🎧 Features

- 🎵 Create new Spotify playlists
- ➕ Add tracks to existing playlists
- 📈 Fetch user's top tracks and add to playlists
- 🤖 Get recommended tracks based on top tracks (Only basic recommendation right now using Reccobeats API)

---


