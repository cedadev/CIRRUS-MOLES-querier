# CIRRUS project documentation

## Project description

design and implement a Large Language Model with tool capability using local model hosting to allow natural language querying of the CEDA MOLES catalogue for improved dataset accessibility to data scientists.

Codename CIRRUS (CEDA Intelligent Retrieval and Research User System) for ease of communication.

The Query response accuracy spreadsheet is included in the documentation file.

</br>

### Project Goals:

Implement natural language catalogue search
-	Enable users to query the MOLES catalogue using plain English.
-	Convert user prompts into valid MOLES API requests.
-	Retrieve relevant catalogue metadata records.

Provide user-readable responses
-	Summarise returned information into natural language.
-	Present information like dataset title, description and other identifiers in readable ways

Test system performance
-	Test the accuracy of API tools.
-	Measure relevance of returned datasets.
-	Test robustness against irrelevant or jailbreak prompts.



</br></br>




## System structure
### description

The project is structured as shown in the tree below. Here I explain what each section does.

Within the `root` directory:
- license
- log files
- readme
- requirements file
- the multiple different setup scripts

The setup scripts are split into windows (ps1) and linux/ mac (sh) and are explained when to be used in the README\
The env setup scripts will create the venv if it doesn't exist, populate it with the requirements and run it in the same shell that ran the setup script\
The ui start script will run the setup script and will create a .env with the CHAINLIT_AUTH_SECRET that it generates if it doesn't exist, and will create the chainlit.db if it doesn't exist, it will then run the interface file (and will run it slightly differently if it is JASMIN or local)

`src` has the main code. It has many folders and two main files
- `main.py` What is used in the terminal based setup, but some functions within are used in the UI.
- `system.py` has the system prompt and the config loader within.

`etc` has the config files in
- `config.yml.example` is the base config to copy to config.yml which is what is used
- `config.yml` needs to be created and is what should be changed for your requirements

`graphical_interface` has all the files used for the UI
- `chainlit.db` created when the UI setup script is ran, is what is used for conversation history for the UI
- `init_sqlite_db.py` this is ran by the setup scripts to create the database with everything it needs in.
- `chainlit_chatbot.py` What runs the UI. **This currently does not have a proper authentication system as this project has not been deployed** 

`langchain_tools` has a single file for tool wrappers
- `langchain_tools.py` imports each tool function, wraps them in langchain ready for use, and gives them a description for the LLM to see

`tool_functionality` holds a file per tool, allows easy conversion of functions to tools using wrappers, splitting each functionality up for ease
- `common.py` has common functions used across tools such as `call_api()`
- `get_record.py` code for UUID search
- `heartbeat_monitor.py` code for ollama checks and API checks
- `search_catalogue.py` code for API filter search
- `search_redirect.py` code for creating a custom google search URL

`tests` holds a lot of pytests for the majority of the static code (tools, common functions, config). Does not test LLM capability or API calling.


</br>

### tree diagram
```
.
├── LICENSE
├── ollama.log
├── README.md
├── requirements.txt
├── run-ollama.sh
├── setup-env.ps1
├── setup-env.sh
├── src
│   ├── chainlit.md
│   ├── etc
│   │   ├── config.yml
│   │   └── config.yml.example
│   ├── graphical_interface
│   │   ├── chainlit_chatbot.py
│   │   ├── chainlit.db
│   │   └──init_sqlite_db.py
│   ├── langchain_tools
│   │   └── langchain_tools.py
│   ├── main.py
│   ├── system.py
│   ├── tests
│   │   ├── run_pytests.md
│   │   ├── test_common
│   │   │   ├── test_call_api.py
│   │   │   └── test_check_link.py
│   │   ├── test_config.py
│   │   └── test_tools
│   │       ├── test_get_record.py
│   │       ├── test_heartbeat_monitor.py
│   │       ├── test_search_catalogue.py
│   │       └── test_search_redirect.py
│   └── tool_functionality
│       ├── common.py
│       ├── get_record.py
│       ├── heartbeat_monitor.py
│       ├── search_catalogue.py
│       └── search_redirect.py
├── start-ui.ps1
└── start-ui.sh
```


</br></br>


## How to use and setup

This project can be used either locally or via JASMIN. Please see the README file for detailed setup guides.\
It has been made intentionally easy for this project to be connected to an API LLM and easy to add additional tools.

</br></br>



## diagram explanations
### Structure_diagram
A user message is created and is sent to either the User interface or the terminal interface. Both are sent to the LLM and given a chat history. For the terminal interface, it uses just a list but for the UI interface it uses a database which stores user and the user chats (as the UI is meant to be ran as a server, but for testing purposes, it is ran per user). The LLM can then choose to call tools which then call external services and then produce a response.

### Module_dependency_diagram
This diagram shows each file and the functions within. The functions are either public (marked with a +) in which they are used in other files, or private (marked with a -) where they are only used in the same file. chainlit_chatbot.py has no markings as they are all used internally. A query can either be sent directly to main, ignoring the chainlit file, or can be sent to the UI via the chainlit chatbot.

### Script_setup_diagram
A simple explanation of the setup scripts. start-ui depends on setup-env and setup env can be used on its own for the basic terminal interface or development.

### Sequence_diagram
This diagram shows a user query that requires multiple tool calls to the MOLES API. Invoke(prompt, history) is used for the terminal and UI interfaces.


</br></br></br>


# Troubleshooting
## LLMs to use
This project will use the Gemma4:31b model on JASMIN (this can be exchanged for the llama3.1:70b model (with some difficulty), but this project was built for gemma).
However, it is unlikely you will be able to run the 31b Gemma model at home.

I have found that the 26b parameter model works well also and I was able to run this locally on my GPU.
If you do not have a porwerful GPU or want ot run a different model, make sure the model says "tools" in the tags so that it can use the langchain tools (or it will give you a warning when trying to query it)

To use the llama3.1:70b model, you need to change the run-ollama script to use the old llama location from the high5 project and change the config file to use that llama model.


## JASMIN UI portforwarding
port forwarding when running the UI can be tricky on JASMIN. I have tried to explain it as best as I could on the README but it is likely you will run into problems. Just make sure you are using VSCode when trying to run the UI from JASMIN as that is what handles the port forwarding.
However, you do not need VS code to run the terminal version of the LLM


## Getting orchid resources
after running the srun command to get the resources required to run the model on ollama, it may get stuck on waiting for resources. This could be for a number of reasons. It could get stuck for just a minute or so, or it could be stuck for large sections of the day during peak usage.

If it is getting stuck and you have waited a very long time for resources, it is best to leave it and come back to it another time (maybe a few hours later) when it might work.


## Permissions
You will need to have orchid permissions on your JASMIN account to run the project through JASMIN (UI or terminal versions)
You also may not be able to access the file location where ollama and the model are because of GWS permissions, however you still should be able to use them just fine.


## SSH
You may have a problem SSHing to JASMIN. If you do, consult the JASMIN guides.
You should be in the sci-ph machines (as they are the ones I have tested in), but it may work in the sci-vm machines (not tested)


## Known UI issues 
The UI is a temporary thing set up to demonstrate it, the terminal version was used for most testing.
These problems have been encountered when running the UI:
- Using the stop button doesn't work and may cause later prompts to fail.
- Sometimes the UI will not display any information after the LLM has processed. if this happens, prompt it again saying to do it again.