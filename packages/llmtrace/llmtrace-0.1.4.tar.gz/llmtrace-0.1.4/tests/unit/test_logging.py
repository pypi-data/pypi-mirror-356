"""
Tests unitarios para el módulo de logging de LLMTrace.
"""

import pytest
import logging
import os
import json
from llmtrace._logging import setup_logger

@pytest.fixture(autouse=True)
def reset_logger():
    """
    Fixture para resetear el logger de llmtrace antes y después de cada test.
    """
    logger = logging.getLogger("llmtrace")
    original_handlers = logger.handlers[:]
    original_level = logger.level
    
    # Limpiar handlers existentes
    for handler in logger.handlers:
        logger.removeHandler(handler)
    
    yield # Ejecutar el test

    # Restaurar handlers y nivel originales
    for handler in logger.handlers:
        logger.removeHandler(handler)
    for handler in original_handlers:
        logger.addHandler(handler)
    logger.setLevel(original_level)

def test_setup_logger_text_format(capsys):
    """
    Verifica que el logger se configure con formato de texto por defecto.
    """
    os.environ["LLMTRACE_LOG_FORMAT"] = "text"
    setup_logger(json_format=False, level="INFO")
    logger = logging.getLogger("llmtrace")
    
    logger.info("Test message for text format.")
    captured = capsys.readouterr()
    
    assert "Test message for text format." in captured.out
    assert " - INFO - " in captured.out
    assert "llmtrace - INFO - LLMTrace logger configured. Format: Text, Level: INFO" in captured.out
    
    # Asegurarse de que no es JSON
    try:
        json.loads(captured.out.splitlines()[0])
        assert False, "Log output should not be JSON"
    except json.JSONDecodeError:
        pass # Expected for text format

def test_setup_logger_json_format(capsys):
    """
    Verifica que el logger se configure con formato JSON.
    """
    os.environ["LLMTRACE_LOG_FORMAT"] = "json"
    setup_logger(json_format=True, level="DEBUG")
    logger = logging.getLogger("llmtrace")
    
    logger.debug("Test message for JSON format.")
    captured = capsys.readouterr()
    
    # El primer log es la confirmación de configuración, el segundo es el mensaje de prueba
    log_lines = captured.out.strip().splitlines()
    
    # Verificar el mensaje de configuración
    assert "LLMTrace logger configured. Format: JSON, Level: DEBUG" in log_lines[0]

    # Verificar el formato JSON del mensaje de prueba
    try:
        log_entry = json.loads(log_lines[1])
        assert log_entry["levelname"] == "DEBUG"
        assert log_entry["name"] == "llmtrace"
        assert log_entry["message"] == "Test message for JSON format."
    except json.JSONDecodeError as e:
        pytest.fail(f"Log output is not valid JSON: {e}\nOutput: {log_lines[1]}")

def test_setup_logger_level_from_env(capsys):
    """
    Verifica que el nivel de logging se lea correctamente de la variable de entorno.
    """
    os.environ["LLMTRACE_LOG_LEVEL"] = "WARNING"
    setup_logger(json_format=False) # No pasar nivel, debe leer del env
    logger = logging.getLogger("llmtrace")
    
    logger.info("This info message should not appear.")
    logger.warning("This warning message should appear.")
    
    captured = capsys.readouterr()
    
    assert "This info message should not appear." not in captured.out
    assert "This warning message should appear." in captured.out
    assert "LLMTrace logger configured. Format: Text, Level: WARNING" in captured.out

def test_setup_logger_level_override(capsys):
    """
    Verifica que el nivel de logging pasado como argumento sobrescriba el de la variable de entorno.
    """
    os.environ["LLMTRACE_LOG_LEVEL"] = "ERROR" # Env var es ERROR
    setup_logger(json_format=False, level="INFO") # Argumento es INFO
    logger = logging.getLogger("llmtrace")
    
    logger.info("This info message should appear.")
    logger.error("This error message should appear.")
    
    captured = capsys.readouterr()
    
    assert "This info message should appear." in captured.out
    assert "This error message should appear." in captured.out
    assert "LLMTrace logger configured. Format: Text, Level: INFO" in captured.out
