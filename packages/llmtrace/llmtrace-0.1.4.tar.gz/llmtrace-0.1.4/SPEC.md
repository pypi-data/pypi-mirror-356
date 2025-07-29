# Especificación de Arquitectura v0 para LLMTrace

Este documento detalla la arquitectura, decisiones clave y procesos operativos para la versión 0 (v0) del proyecto open-source LLMTrace. Sirve como una guía fundamental para el desarrollo, la configuración y el mantenimiento del proyecto.

## 1. Especificación de Arquitectura v0

### 1.1. Dependencias Externas y Librerías de Terceros

*   **Relevancia:** Las dependencias son el esqueleto de nuestra aplicación. Afectan la funcionalidad, el rendimiento, la seguridad y la facilidad de instalación. Las licencias son cruciales para asegurar la compatibilidad con nuestro modelo open-source (MIT).
*   **Decisión Inicial:**
    *   **Gestión:** Usaremos `pyproject.toml` (PEP 621) para declarar las dependencias principales y opcionales.
    *   **Versiones:** Especificaremos versiones mínimas (`package>=X.Y.Z`) para asegurar la compatibilidad y evitar regresiones. Para dependencias críticas o con APIs inestables, podríamos considerar versiones fijas (`package==X.Y.Z`) o rangos más estrictos (`package~=X.Y`).
    *   **Licencias:** Priorizaremos librerías con licencias permisivas (MIT, Apache 2.0, BSD). Realizaremos una revisión manual de las licencias de todas las dependencias directas y transitivas.
*   **Alternativas y Trade-offs:**
    *   **Versiones fijas (`==`):** Mayor reproducibilidad, pero menos flexibilidad para actualizaciones de seguridad automáticas y puede llevar a "dependency hell".
    *   **`requirements.txt` con `pip-tools`:** Permite generar un `requirements.lock` para versiones exactas, lo que es excelente para despliegues. Podríamos añadir esto como una práctica recomendada para entornos de producción.
*   **Riesgos y Mitigación:**
    *   **Conflictos de dependencias:** Mitigación: Especificar rangos de versiones amplios pero seguros. Usar entornos virtuales (`venv`).
    *   **Vulnerabilidades de seguridad en dependencias:** Mitigación: Integrar `Dependabot` (GitHub Actions). Mantener las dependencias actualizadas.
    *   **Incompatibilidad de licencias:** Mitigación: Revisión manual y automatizada de licencias durante el CI/CD.

### 1.2. Variables de Entorno Necesarias

*   **Relevancia:** Las variables de entorno son el método estándar para configurar aplicaciones en diferentes entornos y para gestionar secretos.
*   **Decisión Inicial:**
    *   **Carga:** Usaremos la librería `python-dotenv` para cargar variables de entorno desde un archivo `.env` en desarrollo local.
    *   **Formato:** Las variables seguirán el formato `KEY=VALUE`.
    *   **Nomenclatura:** Prefijo `LLMTRACE_` para variables internas. Las claves de API de terceros mantendrán su nombre estándar (ej., `OPENAI_API_KEY`).
    *   **Gestión de Secretos:** El archivo `.env` **nunca** se versionará en Git. Proporcionaremos un archivo `.env.template`. En producción, se espera que las variables de entorno se inyecten directamente.
*   **Alternativas y Trade-offs:**
    *   **Solo variables de entorno del sistema:** Más seguro en producción, pero menos conveniente para desarrollo local.
    *   **Archivos de configuración (YAML/JSON):** Pueden ser más estructurados, pero menos adecuados para secretos.
*   **Riesgos y Mitigación:**
    *   **Exposición accidental de secretos:** Mitigación: `.gitignore` para `.env`. Documentación clara.
    *   **Configuración inconsistente:** Mitigación: Validar la presencia y el formato de las variables de entorno necesarias.

### 1.3. Estructura de Configuración

*   **Relevancia:** Una estructura de configuración clara y consistente reduce la fricción y previene errores.
*   **Decisión Inicial:**
    *   **Variables de Entorno (`.env`):** Para secretos y configuraciones específicas del entorno.
    *   **Flags CLI (`click`):** Para overrides de configuración en tiempo de ejecución.
    *   **`pyproject.toml`:** Para metadatos del proyecto, dependencias y configuración de herramientas de desarrollo.
    *   **Configuración interna:** La librería tendrá un módulo de configuración interno que cargará las variables de entorno y aplicará valores por defecto.
*   **Alternativas y Trade-offs:**
    *   **Archivos `settings.py`:** Común en Django/Flask, pero puede ser menos flexible.
    *   **Archivos `config.ini` o `config.json`:** Útiles para configuraciones complejas no secretas.
*   **Riesgos y Mitigación:**
    *   **Jerarquía de configuración confusa:** Mitigación: Documentar claramente el orden de precedencia.
    *   **Valores por defecto no obvios:** Mitigación: Asegurar que los valores por defecto sean sensatos y estén bien documentados.

### 1.4. Esquema de Bases de Datos y Migraciones

*   **Relevancia:** La persistencia de datos es central. Un esquema bien definido y un sistema de migraciones robusto son vitales.
*   **Decisión Inicial:**
    *   **Bases de Datos Soportadas:** SQLite (por defecto), PostgreSQL.
    *   **Esquema:** Definido directamente en SQL dentro de las migraciones de Alembic.
    *   **Migraciones:** **Alembic** para gestionar las migraciones.
    *   **Backups:** Responsabilidad del usuario (documentado).
*   **Alternativas y Trade-offs:**
    *   **ORM para esquema:** Simplifica la definición, pero puede ser menos flexible.
    *   **Otros sistemas de migración:** Alembic es el estándar de facto en Python.
*   **Riesgos y Mitigación:**
    *   **Pérdida de datos por migraciones fallidas:** Mitigación: Pruebas exhaustivas de migraciones. Documentación clara sobre cómo revertir.
    *   **Schema drift:** Mitigación: Forzar el uso de Alembic para todos los cambios de esquema.
    *   **Falta de backups:** Mitigación: Documentación clara sobre la importancia y métodos de backup.

### 1.5. Integración con Herramientas de CI/CD

*   **Relevancia:** Esencial para mantener la calidad del código, automatizar pruebas, asegurar la consistencia y acelerar el ciclo de desarrollo.
*   **Decisión Inicial:**
    *   **CI:** **GitHub Actions** para linting, formateo, tests unitarios y de integración, comprobación de dependencias, construcción del paquete y comprobación de docstrings.
    *   **Pre-commit Hooks:** Usaremos `pre-commit` para ejecutar linters y formatters localmente.
    *   **CD (futuro):** Para v0, el CD será manual.
*   **Alternativas y Trade-offs:**
    *   **Otros proveedores de CI:** GitHub Actions es nativo de GitHub.
    *   **No usar pre-commit:** El código puede llegar al repositorio con errores de estilo.
*   **Riesgos y Mitigación:**
    *   **Builds rotos:** Mitigación: Pruebas unitarias y de integración completas.
    *   **Deuda técnica:** Mitigación: `pre-commit` y CI forzado.
    *   **Vulnerabilidades en el código:** Mitigación: Escaneo de seguridad en CI.

### 1.6. Empaquetado y Distribución

*   **Relevancia:** Un empaquetado correcto es crucial para que los usuarios puedan instalar y usar LLMTrace fácilmente.
*   **Decisión Inicial:**
    *   **Empaquetado Python:** Usaremos `setuptools` con `pyproject.toml`.
    *   **Distribución Python:** Publicación en **PyPI** como paquete `llmtrace`.
    *   **Versionado:** **Versionado Semántico (SemVer)**: `MAJOR.MINOR.PATCH`. Para v0, usaremos `0.x.x`.
    *   **Contenedorización:** **Dockerfile** para empaquetar el dashboard web.
    *   **Imagen Base Docker:** `python:3.9-slim-buster` (o la versión más reciente de Python 3.9+).
    *   **Tags Docker:** `llmtrace/dashboard:latest` y `llmtrace/dashboard:0.1.0`.
*   **Alternativas y Trade-offs:**
    *   **Conda:** Otro gestor de paquetes, pero PyPI es más universal.
    *   **Otros formatos de contenedor:** Docker es el estándar.
*   **Riesgos y Mitigación:**
    *   **Errores de empaquetado:** Mitigación: Pruebas de construcción del paquete en CI.
    *   **Dificultad de instalación:** Mitigación: Documentación clara.
    *   **Problemas de versionado:** Mitigación: Adherencia estricta a SemVer.

### 1.7. Licenciamiento OSS vs. Módulos Premium; Protección de Claves

*   **Relevancia:** Define los términos de uso y cómo protegemos nuestra propiedad intelectual.
*   **Decisión Inicial:**
    *   **Licencia OSS:** **MIT License** para el core.
    *   **Módulos Premium (futuro):** Gestionados en repositorios separados con licencias comerciales o propietarias (EULA privado).
    *   **Protección de Claves (API Keys):** **Nunca** se almacenarán en el código fuente ni en la base de datos. Siempre a través de variables de entorno.
*   **Alternativas y Trade-offs:**
    *   **Licencias más restrictivas:** Fomentan la reciprocidad, pero pueden disuadir la adopción.
    *   **Almacenar claves en DB cifradas:** Añade complejidad y riesgo.
*   **Riesgos y Mitigación:**
    *   **Uso indebido del software:** Mitigación: La licencia MIT es clara.
    *   **Fuga de secretos:** Mitigación: Política estricta de no versionar secretos.

### 1.8. Documentación

*   **Relevancia:** La documentación es la interfaz de usuario de una librería.
*   **Decisión Inicial:**
    *   **README.md:** Punto de entrada principal.
    *   **Sitio de Documentación:** Generado con **Sphinx** y alojado en **Read the Docs**.
    *   **Docstrings:** Todos los módulos, clases y funciones Python tendrán docstrings completos (estilo reStructuredText).
    *   **Ejemplos:** Directorio `examples/` con Jupyter Notebooks o scripts.
    *   **CONTRIBUTING.md:** Guía para colaboradores.
*   **Alternativas y Trade-offs:**
    *   **MkDocs, Docusaurus:** Alternativas populares, pero Sphinx es el estándar en Python.
    *   **No usar docstrings:** Reduce la calidad de la documentación.
*   **Riesgos y Mitigación:**
    *   **Documentación desactualizada:** Mitigación: Integrar la generación de docs en CI.
    *   **Documentación poco clara:** Mitigación: Revisión por pares.

### 1.9. Observabilidad Propia (de la Librería)

*   **Relevancia:** LLMTrace es una herramienta de observabilidad, por lo que debe ser observable en sí misma.
*   **Decisión Inicial:**
    *   **Logs:** Usaremos el módulo estándar `logging` de Python para registrar eventos internos. Nivel de log configurable.
    *   **Métricas Internas:** Expondremos métricas básicas a través de la CLI o una API interna.
    *   **Dashboard:** El propio dashboard de LLMTrace mostrará métricas agregadas de las aplicaciones instrumentadas.
*   **Alternativas y Trade-offs:**
    *   **Librerías de métricas dedicadas:** Más potentes, pero añaden complejidad.
    *   **No tener observabilidad interna:** Dificulta la depuración.
*   **Riesgos y Mitigación:**
    *   **Overhead de rendimiento:** Mitigación: Asegurar que el logging sea asíncrono o no bloqueante.
    *   **Falta de visibilidad:** Mitigación: Mejorar métricas y logs a medida que surjan necesidades.

### 1.10. Seguridad de la Cadena de Suministro

*   **Relevancia:** Proteger el proyecto de ataques a la cadena de suministro es crucial.
*   **Decisión Inicial:**
    *   **Escaneo de Vulnerabilidades de Dependencias:** Integrar **Dependabot** (GitHub Actions).
    *   **Escaneo de Código Estático:** Herramientas de linting en CI.
    *   **Firmas de Paquetes (futuro):** Explorar la integración con **Sigstore** para firmar artefactos.
*   **Alternativas y Trade-offs:**
    *   **Otras herramientas de escaneo:** Dependabot es nativo de GitHub.
    *   **No escanear:** Aumenta significativamente el riesgo.
*   **Riesgos y Mitigación:**
    *   **Dependencias comprometidas:** Mitigación: Escaneo continuo, actualizaciones rápidas.
    *   **Builds manipulados:** Mitigación: Asegurar la seguridad del entorno de CI/CD.

### 1.11. Cumplimiento Legal y Privacidad

*   **Relevancia:** Manejar datos de LLMs implica consideraciones de privacidad y cumplimiento normativo.
*   **Decisión Inicial:**
    *   **Retención de Datos:** Documentar claramente que LLMTrace almacena prompts y respuestas. El usuario es responsable.
    *   **Anonimización/Eliminación:** Proporcionar funciones en la API y CLI para eliminar sesiones o mensajes. No anonimización automática en v0.
    *   **GDPR/Privacidad:** Incluir una sección en la documentación que aconseje a los usuarios sobre sus responsabilidades.
*   **Alternativas y Trade-offs:**
    *   **Anonimización automática:** Añade complejidad y puede ser imperfecta.
    *   **No abordar la privacidad:** Riesgo legal y de reputación.
*   **Riesgos y Mitigación:**
    *   **Incumplimiento normativo por parte del usuario:** Mitigación: Documentación clara.
    *   **Almacenamiento de PII sensible:** Mitigación: Aconsejar a los usuarios que eviten enviar PII o que implementen anonimización.

### 1.12. Roadmap de Compatibilidad

*   **Relevancia:** Define el entorno mínimo requerido para ejecutar LLMTrace.
*   **Decisión Inicial:**
    *   **Versión de Python:** **Python 3.9+**.
    *   **Sistemas Operativos:** Linux, macOS (soporte completo); Windows (experimental/WSL2).
    *   **Arquitecturas:** `x86_64` (AMD64) y `arm64` (Apple Silicon, Raspberry Pi).
*   **Alternativas y Trade-offs:**
    *   **Soporte para Python 3.8 o anterior:** Aumenta la base de usuarios, pero limita el uso de nuevas características.
    *   **Soporte nativo completo para Windows:** Requiere más esfuerzo de prueba.
*   **Riesgos y Mitigación:**
    *   **Problemas de compatibilidad:** Mitigación: Matriz de pruebas en CI.
    *   **Base de usuarios limitada:** Mitigación: Comunicar claramente los requisitos.

### 1.13. Estrategia de Extensibilidad

*   **Relevancia:** Un sistema de plugins robusto permite a la comunidad extender LLMTrace.
*   **Decisión Inicial:**
    *   **Sistema de Plugins:** Utilizaremos **`setuptools` entry points** para el descubrimiento y carga de plugins.
    *   **APIs de Extensión:** Definiremos interfaces claras para Instrumentadores, Backends de Almacenamiento y Evaluadores.
    *   **Documentación:** Guías detalladas sobre cómo desarrollar y registrar plugins.
*   **Alternativas y Trade-offs:**
    *   **Carga manual de plugins:** Menos automatizado.
    *   **Frameworks de plugins dedicados:** Podrían ser más potentes, pero `setuptools` es suficiente.
*   **Riesgos y Mitigación:**
    *   **Inestabilidad de la API de plugins:** Mitigación: Versionar explícitamente la API.
    *   **Plugins de baja calidad/maliciosos:** Mitigación: Fomentar la revisión de código.

### 1.14. Estrategia de Monetización Futura

*   **Relevancia:** Asegurar la sostenibilidad del proyecto a largo plazo.
*   **Decisión Inicial:**
    *   **Core Open-Source (MIT):** El corazón de LLMTrace siempre será gratuito y open-source.
    *   **Monetización (futuro):** SaaS Gestionado, Plugins Premium (EULA privado), Soporte y Consultoría Enterprise.
*   **Alternativas y Trade-offs:**
    *   **Donaciones/Patrocinios:** Puede complementar, pero rara vez es suficiente.
    *   **Licencias duales:** Más complejo de gestionar.
*   **Riesgos y Mitigación:**
    *   **Fragmentación de la comunidad:** Mitigación: Mantener el core OSS robusto.
    *   **Dificultad para equilibrar OSS y comercial:** Mitigación: Transparencia con la comunidad.

## 2. Resumen de Decisiones Cerradas

| Tema                 | Decisión v0                         | Nota                                   |
| :------------------- | :---------------------------------- | :------------------------------------- |
| Formato de logs      | Texto legible (config. por defecto) | Documentar cómo cambiar a JSON         |
| Encriptado SQLite    | Postergar a v0.2                    | Valorar `sqlcipher` + gestión de clave |
| Versionado / release | `release-please` + `setuptools-scm` | Acción GitHub para tags y changelog    |
| Plugin premium       | Esqueleto con **EULA privado**      | En repo aparte                         |

\`\`\`

```plaintext file="pyproject.toml"
[project]
name = "llmtrace"
version = "0.1.0"
description = "A lightweight LLM observability and evaluation framework."
readme = "README.md"
requires-python = ">=3.9"
license = { file = "LICENSE" }
keywords = ["llm", "observability", "tracing", "evaluation", "ai"]
authors = [
  { name = "Your Name", email = "your.email@example.com" } # ¡Actualiza esto!
]
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  "Development Status :: 3 - Alpha", # Indica que es una versión inicial
  "Intended Audience :: Developers",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Topic :: Scientific/Engineering :: Artificial Intelligence"
]
dependencies = [
  "Flask>=2.0.0",
  "Flask-Cors>=3.0.10",
  "click>=8.0.0",
  "python-dotenv>=1.0.0", # Para cargar .env
  "zstandard>=0.17.0",    # Para compresión de datos (si se usa)
  "alembic>=1.13.0",      # Para migraciones de DB
  "sqlalchemy>=2.0.0",    # Base para conexiones DB
  "aiosqlite>=0.19.0",    # Para SQLite asíncrono
  "asyncpg>=0.29.0",      # Para PostgreSQL asíncrono
  "httpx>=0.27.0",        # Cliente HTTP asíncrono (para instrumentadores)
  "pydantic>=2.0.0",      # Para modelos de datos (tracing/models.py)
  "python-json-logger>=0.1.0", # Para logs en formato JSON
]

[project.optional-dependencies]
dev = [
  "pytest>=7.0.0",
  "pytest-asyncio>=0.21.0",
  "black>=23.0.0",
  "isort>=5.0.0",
  "flake8>=6.0.0",
  "sphinx>=7.0.0",
  "sphinx_rtd_theme>=2.0.0",
  "myst-parser>=2.0.0",
  "pre-commit>=3.0.0",
  "twine>=4.0.0", # Para subir a PyPI
  "build>=1.0.0", # Para construir el paquete
]
openai = ["openai>=1.14.0"] # Versión mínima testeada
huggingface = ["transformers>=4.38.0"] # Versión mínima testeada
langchain = ["langchain>=0.1.0", "langchain-openai>=0.0.5"] # Versión mínima testeada
eval = ["nltk>=3.8.0", "scikit-learn>=1.0.0"] # Dependencias para evaluación
web = ["gunicorn>=20.0.0"] # Dependencia para el servidor web del dashboard
all = [ # Nuevo extra para instalar todas las dependencias opcionales
  "llmtrace[openai]",
  "llmtrace[huggingface]",
  "llmtrace[langchain]",
  "llmtrace[eval]",
  "llmtrace[web]",
]

[project.urls]
Homepage = "https://github.com/your-org/llmtrace" # ¡Actualiza esto!
Documentation = "https://llmtrace.readthedocs.io" # ¡Actualiza esto!
Repository = "https://github.com/your-org/llmtrace" # ¡Actualiza esto!
Issues = "https://github.com/your-org/llmtrace/issues" # ¡Actualiza esto!

[project.scripts]
llmtrace = "llmtrace.cli.cli:cli"

[project.entry-points."llmtrace.instrumentors"] # Namespace para instrumentadores
openai = "llmtrace.instrumentation.openai:OpenAIInstrumentor"
huggingface = "llmtrace.instrumentation.huggingface:HFInstrumentor"
langchain = "llmtrace.instrumentation.langchain:LangChainCallbackHandler" # O la clase principal del handler

[project.entry-points."llmtrace.backends"] # Namespace para backends de almacenamiento
sqlite = "llmtrace.storage.sqlite:SQLiteStorageBackend"
postgresql = "llmtrace.storage.postgresql:PostgreSQLStorageBackend"

[project.entry-points."llmtrace.evaluators"] # Namespace para evaluadores
# Ejemplo: "bleu" = "llmtrace.evaluation.metrics:BLEUEvaluator"

[build-system]
requires = ["setuptools>=61.0", "wheel", "setuptools_scm[toml]>=6.0"] # setuptools_scm para versionado automático
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["llmtrace*"]

[tool.setuptools_scm]
version_scheme = "no-guess-dev"
local_scheme = "no-local-version"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 88

[tool.pytest.ini_options]
asyncio_mode = "auto"
addopts = "--strict-markers --strict-content"
