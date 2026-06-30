import pytest

from system import load_config


def test_load_config_file_not_found(monkeypatch):
    def mock_open_missing(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open_missing)

    with pytest.raises(FileNotFoundError) as exc_info:
        load_config()
    assert str(exc_info.value) == "Configuration file not found at etc/config.yml"


def test_load_config_malformed_yaml(mocker):
    bad_yaml = "Host-type:\n  host: 'local"
    mocker.patch("builtins.open", mocker.mock_open(read_data=bad_yaml))

    with pytest.raises(ValueError) as exc_info:
        load_config()
    assert (
        str(exc_info.value) == "Configuration file at etc/config.yml is malformed YAML"
    )


def test_load_config_invalid_structure(mocker):
    list_yaml = "- item1\n- item2"
    mocker.patch("builtins.open", mocker.mock_open(read_data=list_yaml))

    with pytest.raises(ValueError) as exc_info:
        load_config()
    assert (
        str(exc_info.value)
        == "Configuration file at etc/config.yml must contain a valid YAML structure"
    )


def test_load_config_missing_host_type(mocker):
    missing_host = """
    LLM-type:
      LOCAL_LLM: "gemma4:31b"
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=missing_host))

    with pytest.raises(KeyError) as exc_info:
        load_config()
    assert "Configuration missing required key path: ['Host-type']['host']" in str(
        exc_info.value
    )


def test_load_config_missing_llm_type(mocker):
    missing_llm = """
    Host-type:
      host: "local"
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=missing_llm))

    with pytest.raises(KeyError) as exc_info:
        load_config()
    assert "Configuration missing required 'LLM-type' section" in str(exc_info.value)


def test_load_config_missing_local_llm(mocker):
    missing_local_model = """
    Host-type:
      host: "local"
    LLM-type:
      JASMIN_LLM: "gemma4:31b"
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=missing_local_model))

    with pytest.raises(ValueError) as exc_info:
        load_config()
    assert (
        str(exc_info.value)
        == "Host is set to 'local', but 'LOCAL_LLM' model is missing or empty."
    )


def test_load_config_missing_jasmin_llm(mocker):
    missing_jasmin_model = """
    Host-type:
      host: "JASMIN"
    LLM-type:
      LOCAL_LLM: "gemma4:31b"
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=missing_jasmin_model))

    with pytest.raises(ValueError) as exc_info:
        load_config()
    assert (
        str(exc_info.value)
        == "Host is set to 'JASMIN', but 'JASMIN_LLM' model is missing or empty."
    )


def test_load_config_success(mocker):
    valid_yaml = """
    Host-type:
      host: "local"
    LLM-type:
      LOCAL_LLM: "gemma4:31b"
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=valid_yaml))

    config = load_config()
    assert config["Host-type"]["host"] == "local"
