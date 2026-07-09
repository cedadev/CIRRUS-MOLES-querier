# CIRRUS project documentation

## Project description

design and implement a Large Language Model with tool capability using local model hosting to allow natural language querying of the CEDA MOLES catalogue for improved dataset accessibility to data scientists.

Codename CIRRUS (CEDA Intelligent Retrieval and Research User System) for ease of communication.

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