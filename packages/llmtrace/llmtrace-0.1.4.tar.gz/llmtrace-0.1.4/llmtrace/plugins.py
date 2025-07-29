"""
Módulo para la gestión de plugins de LLMTrace.

Permite el descubrimiento y la carga de instrumentadores, backends de almacenamiento
y evaluadores a través de los entry points de setuptools.
"""

import logging
import pkg_resources
from typing import Type, Dict, Any

logger = logging.getLogger("llmtrace.plugins")

def discover_plugins(group: str) -> Dict[str, Type[Any]]:
    """
    Descubre plugins registrados a través de setuptools entry points.

    :param group: El nombre del grupo de entry points a buscar (ej., "llmtrace.instrumentors").
    :type group: str
    :returns: Un diccionario donde las claves son los nombres de los plugins
              y los valores son las clases de los plugins.
    :rtype: Dict[str, Type[Any]]
    """
    plugins = {}
    for entry_point in pkg_resources.iter_entry_points(group=group):
        try:
            plugin_class = entry_point.load()
            plugins[entry_point.name] = plugin_class
            logger.debug(f"Discovered plugin: {entry_point.name} from group {group}")
        except Exception as e:
            logger.error(f"Error loading plugin {entry_point.name} from group {group}: {e}")
    return plugins

_registered_instrumentors: Dict[str, Type[Any]] = {}
_registered_backends: Dict[str, Type[Any]] = {}
_registered_evaluators: Dict[str, Type[Any]] = {}

def _load_all_plugins():
    """Carga todos los plugins al inicio."""
    global _registered_instrumentors, _registered_backends, _registered_evaluators
    _registered_instrumentors = discover_plugins("llmtrace.instrumentors")
    _registered_backends = discover_plugins("llmtrace.backends")
    _registered_evaluators = discover_plugins("llmtrace.evaluators")
    logger.info("LLMTrace plugins loaded.")

# Cargar plugins al importar el módulo
_load_all_plugins()

def get_instrumentor_class(name: str) -> Type[Any] | None:
    """
    Obtiene la clase de un instrumentador registrado por su nombre.

    :param name: El nombre del instrumentador.
    :type name: str
    :returns: La clase del instrumentador o None si no se encuentra.
    :rtype: Type[Any] | None
    """
    return _registered_instrumentors.get(name)

def get_backend_class(name: str) -> Type[Any] | None:
    """
    Obtiene la clase de un backend de almacenamiento registrado por su nombre.

    :param name: El nombre del backend.
    :type name: str
    :returns: La clase del backend o None si no se encuentra.
    :rtype: Type[Any] | None
    """
    return _registered_backends.get(name)

def get_evaluator_class(name: str) -> Type[Any] | None:
    """
    Obtiene la clase de un evaluador registrado por su nombre.

    :param name: El nombre del evaluador.
    :type name: str
    :returns: La clase del evaluador o None si no se encuentra.
    :rtype: Type[Any] | None
    """
    return _registered_evaluators.get(name)

def list_registered_instrumentors() -> list[str]:
    """
    Lista los nombres de todos los instrumentadores registrados.

    :returns: Una lista de nombres de instrumentadores.
    :rtype: list[str]
    """
    return list(_registered_instrumentors.keys())

def list_registered_backends() -> list[str]:
    """
    Lista los nombres de todos los backends de almacenamiento registrados.

    :returns: Una lista de nombres de backends.
    :rtype: list[str]
    """
    return list(_registered_backends.keys())

def list_registered_evaluators() -> list[str]:
    """
    Lista los nombres de todos los evaluadores registrados.

    :returns: Una lista de nombres de evaluadores.
    :rtype: list[str]
    """
    return list(_registered_evaluators.keys())
