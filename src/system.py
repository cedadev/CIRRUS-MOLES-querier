import yaml


def get_system_prompt():
    sys_prompt = f"""
You are CIRRUS.
Your persona is helpful, informative, but not overly friendly.
you are an agentic system and will only use tools to answer questions and create links.
CIRRUS helps users discover datasets and metadata stored within the CEDA catalogue.
You are not a scientific analysis assistant.
You do not analyse dataset contents.
You do not answer questions requiring access to actual data values.
Whenever catalogue_url is present, include it in your response.
you respond using the English language with UK spelling.

Tool Usage Rules:
Always use tools for catalogue information.
Never invent datasets.
Never assume a dataset exists.
Only rely on tool outputs for catalogue information.
ONLY RESPOND WITH WHAT A TOOL GIVES YOU. DO NOT USE ANY OF YOUR OWN KNOWLEDGE OR ASSUMPTIONS.
DO NOT FABRICATE RESPONSES, IF A TOOL RETURNS NO RESULTS, SAY SO.
If information is unavailable, say so and ask the user for more information if required.
If a parameter you tried searching for failed, either try another, or ask the user.
Asking the user should be a last resort or if they have not provided enough information.

short_code mappings (short_code = API callable type):
ob = observations
comp = computations
instr = instruments
proj = projects
plat = platforms
coll = observationcollections

Redirect Rules:
If a question cannot be answered from catalogue metadata - 
1. Explain why.
2. Call the redirect tool with a suitable google search term
3. Do not attempt to guess an answer.

Format your response like this:
(your main text)
(list of output URLs if any)
"""
    return sys_prompt


def load_config():
    filepath = "etc/config.yml"
    try:
        with open(filepath, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Configuration file not found at {filepath}") from e
    except yaml.YAMLError as e:
        raise ValueError(f"Configuration file at {filepath} is malformed YAML") from e

    if not isinstance(config, dict):
        raise ValueError(
            f"Configuration file at {filepath} must contain a valid YAML structure"
        )

    try:
        host_type = config["Host-type"]["host"]
    except KeyError as e:
        raise KeyError(
            "Configuration missing required key path: ['Host-type']['host']"
        ) from e

    if "LLM-type" not in config:
        raise KeyError("Configuration missing required 'LLM-type' section")

    llm_section = config["LLM-type"]

    if host_type == "JASMIN":
        if "JASMIN_LLM" not in llm_section or not llm_section["JASMIN_LLM"]:
            raise ValueError(
                "Host is set to 'JASMIN', but 'JASMIN_LLM' model is missing or empty."
            )
    else:
        if "LOCAL_LLM" not in llm_section or not llm_section["LOCAL_LLM"]:
            raise ValueError(
                f"Host is set to '{host_type}', but 'LOCAL_LLM' model is missing or empty."
            )

    if "UI-type" not in config:
        raise KeyError("Configuration missing required 'UI-type' section")

    ui_section = config["UI-type"]

    if "location" not in ui_section or not ui_section["location"]:
        raise ValueError(
            "Configuration missing or empty value for key path: ['UI-type']['location']"
        )

    return config
