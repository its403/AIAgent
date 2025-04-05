from langchain_groq import ChatGroq
from spotify import create_spotify_playlist, add_tracks_to_playlist, get_user_top_tracks, get_recommendation
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
import logging
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
import uuid
from langchain.agents import create_tool_calling_agent

load_dotenv()

# logging.basicConfig(level=logging.INFO)
# langsmith_logger = logging.getLogger("langsmith")
# langsmith_logger.setLevel(logging.DEBUG)

model = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.7,
    max_tokens=1000 # Tested upto 50 tracks playlist usinng gemma2-9b-it
)

tools = [get_user_top_tracks, create_spotify_playlist, get_recommendation, add_tracks_to_playlist]

model_with_tools = model.bind_tools(tools=tools)

prompt = (
    """
        You are a MusicAI, an AI agent specializing in creating personalized Spotify playlists. 
        Use the available tools to help users generate playlists based on their preferences.

        Available Tools:
        - get_user_top_tracks: Retrieve user's top tracks
        - create_spotify_playlist: Create a new playlist
        - add_tracks_to_playlist: Add tracks to a playlist
        - get_recommendation: Get song recommendations

        Respond directly and use tools as needed to fulfill the user's music playlist request.
    """
)

memory = MemorySaver()

agent = create_react_agent(model=model_with_tools, tools=tools, prompt=prompt, checkpointer=memory) # debug=True for logs

def run_chatbot():

    config = {"configurable": {"thread_id": "abc123"}}

    print("MusicAI Playlist Agent 🤖")

    print("Type 'quit/exit' to end the conversation!")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye! Enjoy your playlist!")
                break

            response = agent.invoke(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=config
            )

            print(f"MusicAI: {response["messages"][-1].content}")
    
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    run_chatbot()