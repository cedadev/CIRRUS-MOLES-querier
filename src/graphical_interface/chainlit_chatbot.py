from main import heartbeat, setup_agent
from system import load_config

import os
import logging

import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from langchain.messages import HumanMessage, AIMessage


logging.basicConfig(level=logging.INFO)

# Global variables
pw = os.environ.get("USER_PW", "UNmatCHEd")


# setup agent, load config and run heartbeat
heartbeat()
agent_executor = setup_agent()
config = load_config()


@cl.data_layer
def get_data_layer():
    db_path = os.path.abspath("./graphical_interface/chainlit.db")
    return SQLAlchemyDataLayer(conninfo=f"sqlite+aiosqlite:///{db_path}")


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Can easily be expanded to add a hosted app.
    if config["UI-type"]["location"] == "local":
        return cl.User(
            identifier=username,
            metadata={"role": "user", "provider": "credentials"},
        )


@cl.on_chat_start
async def on_chat_start():
    # sets up history on new conversation
    cl.user_session.set("history", [])


@cl.on_chat_resume
async def on_chat_resume(thread):
    # Extract previous steps (messages)
    history = []

    for step in thread["steps"]:
        if step["type"] == "user_message" and step.get("input"):
            history.append(HumanMessage(content=step["input"]))
        elif step["type"] == "assistant_message" and step.get("output"):
            history.append(AIMessage(content=step["output"]))

    cl.user_session.set("history", history)


@cl.on_message
async def main(message: cl.Message):
    # Retrieve current session history
    history = cl.user_session.get("history", [])

    # Placeholder message
    msg = cl.Message(content="")
    await msg.send()

    try:
        # Run agent query using async execution
        response = await cl.make_async(agent_executor.invoke)(
            {"input": message.content, "chat_history": history}
        )

        output_text = response["output"]

        # Add history
        history.append(HumanMessage(content=message.content))
        history.append(AIMessage(content=output_text))
        cl.user_session.set("history", history)

        # Update the placeholder message
        msg.content = output_text
        await msg.update()

    except Exception as e:
        logging.error("An error occurred during agent execution: %s", e)
        msg.content = f"An error occurred: {str(e)}"
        await msg.update()
