import yaml
import logging

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage
from langchain_tools.langchain_tools import (
    search_catalogue_tool,
    get_record_tool,
    search_redirect_tool,
)

from tool_functionality.heartbeat_monitor import check_services
from system import get_system_prompt

logging.basicConfig(level=logging.INFO)


def heartbeat():
    heartbeat = check_services()
    if False in heartbeat.values():
        if not heartbeat["api_online"]:
            logging.warning("THE MOLES API IS LIKELY OFFLINE")

        if not heartbeat[
            "ollama_online"
        ]:  # This can have an and added to determine if ollama is being used
            logging.warning("OLLAMA IS LIKELY OFFLINE")


def setup_agent():
    # Load model from config
    with open("etc/config.yml", "r") as f:
        config = yaml.safe_load(f)

    host_type = config["Host-type"]["host"]

    if host_type == "JASMIN":
        model = config["LLM-type"]["JASMIN_LLM"]
    else:
        model = config["LLM-type"]["LOCAL_LLM"]
    logging.info("loaded %s", model)

    # set up tools
    tools = [search_catalogue_tool, get_record_tool, search_redirect_tool]

    llm = ChatOllama(model=model)

    system_prompt = get_system_prompt()

    # prompt template with placeholders (agent_scratchpad is important for tool calling)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


def chat_loop():
    while True:
        user_input = input(
            "\n--------------------\n\nEnter your query (or 'exit' to quit): "
        )
        if user_input.lower() in ["exit", "quit"]:
            logging.info("Exiting agent interaction.")
            break

        try:
            response = agent_executor.invoke(
                {"input": user_input, "chat_history": history}
            )
            # Add messages to history
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response["output"]))
            print(f"\n**Agent response:**\n\n{response['output']}")
        except KeyboardInterrupt:
            print("\nGeneration stopped by user.")
        except Exception as e:
            logging.error("\nAn error occurred: %s", e)


if __name__ == "__main__":
    # check if systems are online
    heartbeat()

    # setup the agent
    agent_executor = setup_agent()

    # conversation history
    history = []

    # run the LLM interface
    chat_loop()
