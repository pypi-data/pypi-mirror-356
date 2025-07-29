"""
Módulo para la configuración centralizada del sistema de logging de LLMTrace.
Permite configurar el formato (texto o JSON) y el nivel de los logs.
"""

import logging
import os
from pythonjsonlogger import jsonlogger as JsonFormatter # type: ignore

def setup_logger(json_format: bool = False, level: str | None = None):
    """
    Configura el logger principal de LLMTrace.

    :param json_format: Si es True, los logs se formatearán como JSON.
                        Si es False, se usarán logs de texto legible.
    :type json_format: bool
    :param level: El nivel de logging (ej. "INFO", "DEBUG", "WARNING").
                  Si es None, se leerá de la variable de entorno LLMTRACE_LOG_LEVEL
                  o se usará "INFO" por defecto.
    :type level: str | None
    """
    logger = logging.getLogger("llmtrace")
    
    # Eliminar handlers existentes para evitar duplicados al reconfigurar
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    # Determinar el nivel de logging
    if level is None:
        log_level_str = os.getenv("LLMTRACE_LOG_LEVEL", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
    else:
        log_level = getattr(logging, level.upper(), logging.INFO)
    
    logger.setLevel(log_level)

    # Configurar el formato del log
    if json_format:
        formatter = JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Añadir un StreamHandler para la salida a consola
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False # Evitar que los logs se propaguen al logger raíz de Python
    
    logger.info(f"LLMTrace logger configured. Format: {'JSON' if json_format else 'Text'}, Level: {logging.getLevelName(log_level)}")

# Configuración inicial por defecto al importar el módulo
# Lee LLMTRACE_LOG_FORMAT del entorno, por defecto a 'text'
_log_format = os.getenv("LLMTRACE_LOG_FORMAT", "text").lower()
_json_format_default = _log_format == "json"
setup_logger(json_format=_json_format_default)
