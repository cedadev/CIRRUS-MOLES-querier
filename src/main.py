from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, AIMessage
#from langchain_tool import get_record_from_uuid

# set up tools
#tools = [get_record_from_uuid]
tools = []

#llm = ChatOllama(model="llama3.1:8b-instruct-q8_0")
llm = ChatOllama(model="qwen3:14b")
system_prompt = "You are a helpful assistant you have access to tools, but should only use them if prompted. If I say 'banana' anywhere, you will respond with: 'MONKEY!!'"

# prompt template with placeholders (agent_scratchpad is important for tool calling)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# conversation history
history = []

while True:
    user_input = input("\n--------------------\n\nEnter your query (or 'exit' to quit): ")
    if user_input.lower() in ['exit', 'quit']:
        print("Exiting agent interaction.")
        break
    
    
    try:
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": history
        })
        # Add messages to history
        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=response["output"]))
        print(f"\n**Agent response:**\n\n{response['output']}")
    except KeyboardInterrupt:
        print("\nGeneration stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    print(history)
