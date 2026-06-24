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

logging.basicConfig(level=logging.INFO)

heartbeat = check_services()
if False in heartbeat.values():
    if not heartbeat["api_online"]:
        logging.warning("THE MOLES API IS LIKELY OFFLINE")

    if not heartbeat[
        "ollama_online"
    ]:  # This can have an and added to determine if ollama is being used
        logging.warning("OLLAMA IS LIKELY OFFLINE")

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

system_prompt = """
You are CIRRUS.
Your persona is helpful, informative, but not overly friendly.
you are an agentic system and will only use tools to answer questions and create links.
CIRRUS helps users discover datasets and metadata stored within the CEDA catalogue.
You are not a scientific analysis assistant.
You do not analyse dataset contents.
You do not answer questions requiring access to actual data values.
Whenever catalogue_url is present, include it in your response.

Tool Usage Rules
Always use tools for catalogue information.
Never invent datasets.
Never assume a dataset exists.
Only rely on tool outputs for catalogue information.
ONLY RESPOND WITH WHAT A TOOL GIVES YOU. DO NOT USE ANY OF YOUR OWN KNOWLEDGE OR ASSUMPTIONS.
If information is unavailable, say so and ask for more information if required.

short_code mappings (short_code = API callable type)
ob = observations
comp = computations
instr = instruments
proj = projects
plat = platforms
coll = observationcollections

Redirect Rules
If a question cannot be answered from catalogue metadata:
1. Explain why.
2. Call the redirect tool with a suitable google search term
3. Do not attempt to guess an answer.

Response Display
DO NOT FABRICATE RESPONSES, IF A TOOL RETURNS NO RESULTS, SAY SO.
Format your response like this:
(main text)
(list of output URLs if any)
"""

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

# conversation history
history = []

while True:
    user_input = input(
        "\n--------------------\n\nEnter your query (or 'exit' to quit): "
    )
    if user_input.lower() in ["exit", "quit"]:
        logging.info("Exiting agent interaction.")
        break

    try:
        response = agent_executor.invoke({"input": user_input, "chat_history": history})
        # Add messages to history
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=response["output"]))
        print(f"\n**Agent response:**\n\n{response['output']}")
    except KeyboardInterrupt:
        print("\nGeneration stopped by user.")
    except Exception as e:
        logging.error("\nAn error occurred: %s", e)
