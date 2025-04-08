from langchain_groq import ChatGroq
from spotify import create_spotify_playlist, add_tracks_to_playlist, get_user_top_tracks, get_recommendation
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
import logging
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_tool_calling_agent
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

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

# ------------- Terminal Section -------------------------------------------------------------
#-------------- Comment this part before running websocket part-------------------------------

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

# -------------- WebSocket Section -------------------

# logging.basicConfig(level=logging.INFO, 
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# app = FastAPI(title="MusicAI WebSocket API")

# @app.websocket("/chat")
# async def chat_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     session_id = f"session_{id(websocket)}"
#     logger.info(f"New WebSocket connection established: {session_id}")
    
#     config = {"configurable": {"thread_id": session_id}}
    
#     try:
#         # Send welcome message
#         welcome_message = {
#             "type": "welcome",
#             "content": "Connected to MusicAI! What kind of playlist would you like to create?"
#         }
#         await websocket.send_text(json.dumps(welcome_message))
        
#         # Main interaction loop
#         while True:
#             raw_data = await websocket.receive_text()
#             logger.info(f"Received message from {session_id}: {raw_data}")
            
#             try:
#                 data = json.loads(raw_data)
#                 user_message = data.get("message", "")
#             except json.JSONDecodeError:
#                 user_message = raw_data
            
#             if user_message.lower() in ["quit", "exit", "disconnect"]:
#                 goodbye_message = {
#                     "type": "goodbye",
#                     "content": "Goodbye! Enjoy your playlist!"
#                 }
#                 await websocket.send_text(json.dumps(goodbye_message))
#                 break
            
#             logger.info(f"Invoking agent for {session_id}")
#             response = await agent.ainvoke(
#                 {
#                     "messages": [
#                         HumanMessage(content=user_message)
#                     ]
#                 },
#                 config=config
#             )
            
#             ai_message = response["messages"][-1].content
#             response_data = {
#                 "type": "response",
#                 "content": ai_message
#             }
#             logger.info(f"Sending response to {session_id}")
#             await websocket.send_text(json.dumps(response_data))
            
#     except WebSocketDisconnect:
#         logger.info(f"WebSocket disconnected: {session_id}")
#     except Exception as e:
#         logger.error(f"Error in WebSocket connection {session_id}: {str(e)}", exc_info=True)
#         error_message = {
#             "type": "error",
#             "content": f"An error occurred: {str(e)}"
#         }
#         try:
#             await websocket.send_text(json.dumps(error_message))
#         except:
#             pass


# @app.get("/")
# def read_root():
#     return {"status": "MusicAI is running", "websocket_endpoint": "/chat"}

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)