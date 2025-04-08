# AI Music Agent

An AI-powered music assistant that creates personalized Spotify playlists using user top tracks.

## 🚀 Proof of Concept

### Test run of the Agent

![Test Image](/img/testrun.png "Image showing test run of the agent")

---

### 🔧 Setup Instructions

> **Requirements**: Tested with Python 3.12

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

4. **Get the required API keys and paste them into your .env file**

    - [Groq API Key](https://console.groq.com/keys)
    - [Spotify API Key](https://developer.spotify.com/dashboard)
        - Set https://google.com/ as the Redirect URI in your Spotify app settings.
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

### Now test AI Agent over websocket

![Websocket Test](/img/websocket_test.png "Image showing test run of the agent over websocket connection")

1. In **main.py**, uncomment the WebSocket section and comment out the terminal section.

2. Then run

    ```bash
    python main.py
    ```

3. Now go to [Hoppscotch](https://hoppscotch.io/realtime/websocket)

4. Add **ws://localhost:8000/chat** in the URL field and click the **Connect** button

5. To send message, go to communication field and enter the message in below format
    ```
    {
        "message": "<Your message>"
    }   
    ```