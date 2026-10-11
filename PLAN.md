# Plan: sistema multi-agente con LangChain y Langfuse

> **Vocabulario:** los términos en mayúscula inicial (Router, Route, Area, Specialist, Section, Judge, Check, …) están definidos en `CONTEXT.md`. Ese archivo manda: si este plan y el glosario difieren, se corrige el plan.
> **Decisiones difíciles de revertir:** `docs/adr/`.

## 1. Consigna y contexto

### Contexto

Eres un/a AI engineer en una empresa SaaS mediana que gestiona consultas de clientes a través de múltiples áreas (HR, IT Support, Finance, Legal). El equipo de soporte está desbordado porque muchos tickets se enrutan mal: preguntas de HR terminan en IT, consultas financieras llegan al equipo legal, etc. La dirección te pidió construir un sistema de routing inteligente que clasifique automáticamente las preguntas entrantes por departamento y las dirija a AI agents especializados, capaces de dar respuestas precisas y con contexto usando la documentación interna de la empresa.

El sistema debe manejar consultas reales de clientes, mantener observability completa para depurar preguntas mal enrutadas y evaluar automáticamente la calidad de las respuestas para detectar errores antes de que lleguen a los clientes.

### Objetivos (qué vas a entregar y por qué importa)

1. Construir un sistema de multi-agent orchestration con un orchestrator que clasifique la intención del usuario y, de forma condicional, enrute las consultas a RAG agents especializados. Esto resuelve el problema real de manejar consultas diversas con conocimiento específico por dominio.
2. Implementar todo el workflow usando LangChain para aprovechar componentes production-grade (chains, retrievers, agents) en lugar de código custom frágil. Esto asegura mantenibilidad y sigue estándares de la industria.
3. Instrumentar workflow tracing completo con Langfuse para que el equipo pueda depurar misclassifications, retrievals fallidos y respuestas incorrectas inspeccionando todo el execution path. Esto habilita production monitoring e incident response.
4. Crear RAG agents especializados (mínimo 3) con colecciones de documentos por dominio que "groundeen" las respuestas en la documentación de la empresa. Esto reduce hallucinations y asegura que las respuestas reflejen políticas reales.
5. Documentar decisiones técnicas explicando por qué elegiste componentes específicos de LangChain, estrategias de routing y configuraciones de RAG. Esto demuestra criterio de ingeniería más allá de simplemente "hacer que funcione".
6. Desplegar un evaluator agent automatizado dentro de Langfuse que puntúe cada respuesta en dimensiones de calidad (relevance, completeness, accuracy). Esto detecta respuestas de baja calidad antes de que las vea el cliente y genera métricas continuas de calidad.

> **¿Por qué esto es importante?** Los sistemas multi-agent con buena orchestration, uso de frameworks y observability son la base de las aplicaciones LLM en producción. Este proyecto simula requisitos empresariales reales: manejar consultas diversas, usar herramientas existentes correctamente (LangChain), depurar workflows complejos (Langfuse) y mantener estándares de calidad (evaluation). Estas habilidades se transfieren directamente a la construcción de productos de IA de cara al cliente.

### Consigna

Desarrolla un sistema multiagente en el que un Agente Orquestador clasifique la intención de la consulta del usuario (por ejemplo, RR. HH. o Tecnología). Esta clasificación activa un enrutamiento condicional que delega la tarea de recuperación al Agente RAG especializado correcto, para generar una respuesta contextualmente fundamentada. Todo el flujo dinámico debe implementarse con LangChain y quedar trazado completamente con Langfuse.

Además, implementa un Agente Evaluador dentro de Langfuse para asignar automáticamente a cada respuesta RAG un puntaje de calidad de 1 a 10, basado en la consulta original y la respuesta final.

### Estructura de repositorio esperada

| Entregable | Archivo/Formato | Contenido mínimo |
|---|---|---|
| Main notebook | `multi_agent_system.ipynb` o múltiples archivos: `src/multi_agent_system.py`, `src/agents/orchestrator.py`, `src/agents/hr_agent.py`, `src/agents/tech_agent.py`, `src/agents/finance_agent.py` | Toda la implementación en un notebook organizado por secciones: (1) Setup e imports, (2) carga de documentos y vector stores, (3) definición de agentes, (4) orquestador y enrutamiento, (5) pruebas y ejemplos, (6) integración con Langfuse. Debe haber encabezados claros en Markdown separando cada sección. |
| Colecciones de documentos | `data/hr_docs/`, `data/tech_docs/`, `data/finance_docs/` | Mínimo 50 chunks por dominio. Documentos en formato .txt, .pdf, .md o .csv. Cada carpeta representa la base de conocimiento de un agente especializado. |
| Test queries | `test_queries.json` o definidas en el notebook | Mínimo 10 consultas de prueba con la categoría de intención esperada. Puede ser un archivo JSON o un diccionario en una celda del notebook. Debe cubrir todos los tipos de agente y casos borde. |
| README | `README.md` | Descripción del proyecto, instrucciones de instalación (instalar requirements, configurar API keys), cómo ejecutar el notebook (orden de ejecución de celdas), ejemplos de uso (qué celdas correr), notas de configuración y limitaciones conocidas. |
| Dependencias | `requirements.txt` | langchain, langchain-openai, langfuse, openai, una librería de vector store, tiktoken, python-dotenv, jupyter, ipykernel (mínimo 9 paquetes). |
| Environment template | `.env.example` | `OPENAI_API_KEY=your-key-here`, `LANGFUSE_PUBLIC_KEY=pk-lf-xxx`, `LANGFUSE_SECRET_KEY=sk-lf-xxx`, `LANGFUSE_HOST=https://cloud.langfuse.com` |
| Agente evaluador | En una sección del notebook o `evaluator.py` | Implementación del Evaluator usando la Score API de Langfuse. Puede estar en una sección dedicada del notebook con explicación en Markdown o en un archivo .py separado importado desde el notebook. |

### Cómo se mapea la consigna al vocabulario del proyecto

La consigna usa "agente" para tres cosas distintas. Acá cada una tiene su nombre (ver `CONTEXT.md`), y el README lleva esta misma tabla:

| Consigna | Este proyecto | Por qué |
|---|---|---|
| Agente Orquestador | **Router** (produce una **Route**) + el grafo que la ejecuta | Lo que clasifica es el Router; "orquestar" es lo que hace el grafo entero |
| Agente RAG / `hr_agent.py` | **Specialist** (`specialists/specialist.py`, `build_specialist(Area.HR, ...)`) | No son agentes con tool-calling: son cadenas deterministas (ADR 0002). Hay una sola fábrica que se instancia por Area; no hay un archivo por Area. El README mapea los nombres de la consigna a esta fábrica |
| Agente Evaluador | **Judge** (`judging/answer_judge.py`, `build_judge`) | "Evaluator" ya lo usa Langfuse para las funciones de los experimentos, que acá se llaman **Checks** |
| categoría / departamento / dominio | **Area** (`hr` \| `tech` \| `finance`) | Una palabra, un concepto |
| chunk | **Section** | Por diseño, 1 sección `##` = 1 chunk. "Chunk" solo aparece dentro de `chunker.py` |

### Punto de partida del repo

- Proyecto `uv` con Python 3.14.
- Ya existe `src/orchestration/config.py`, con `Settings` y `load_settings()`, que lee `OPENAI_API_KEY`, `LLM_MODEL` y `LLM_TEMPERATURE` desde `.env`. Se reemplaza en el ticket 01.
- Ya existe `src/orchestration/llm.py` con `get_chat_model(settings)`, que crea un único modelo global. Se reescribe en el ticket 01 como fábrica por rol.
- Existe `src/core/LLM.py`, vacío y fuera del paquete. Se borra en el ticket 01.
- Existe `CLAUDE.md` con solo el bloque `## Agent skills` (tracker local en `.scratch/`, etiquetas de triage, docs de dominio; ver `docs/agents/`). Los bloques de la sección 7 se agregan arriba en el ticket 01.
- Hay tests con pytest en `tests/`.
- `CONTEXT.md` (glosario) y `docs/adr/0001..0003` ya están escritos.

## 2. Herramientas

### Ya instaladas ✅

| Herramienta | Para qué la usamos |
|---|---|
| Python 3.14 + uv | Lenguaje, y gestor de paquetes y entorno virtual |
| langchain + langchain-core | Framework para armar cadenas, retrievers y salida estructurada |
| langgraph | Viene como dependencia de `langchain>=1.4`. Es el grafo que ejecuta el enrutamiento condicional |
| langchain-openai | Conecta LangChain con OpenAI: el LLM que responde y el modelo de embeddings |
| openai | SDK oficial de OpenAI, que langchain-openai usa por debajo |
| tiktoken | Contar tokens, para medir el tamaño de las secciones |
| python-dotenv | Leer el `.env` (lo usa pydantic-settings por debajo) |
| pydantic | Definir estructuras de datos: `Route`, `QualityVerdict`, `SupportAnswer` |
| pytest | Correr los tests |

### Faltan instalar ❌

| Herramienta | Para qué la usamos |
|---|---|
| pydantic-settings | Leer y validar las ~13 variables de entorno de `Settings` sin repetir `os.getenv` |
| langfuse | Tracing de todo el flujo, Score API para el Judge, Datasets + Experiments para medir |
| langchain-text-splitters | Partir los documentos en secciones |
| langchain-chroma (Chroma) | Vector store: guarda las secciones y las busca por significado |
| jupyter + ipykernel | Abrir y ejecutar el notebook |

### Cuentas necesarias (no se instalan)

- **OpenAI:** API key → `OPENAI_API_KEY`.
- **Langfuse:** proyecto gratis en cloud.langfuse.com → `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`.

### Riesgo conocido

Python 3.14 es muy nuevo y puede que Chroma todavía no lo soporte. Se comprueba al instalar. Si falla, el proyecto baja a Python 3.12. Nota: `RAG-Concepts/M2-Project` ya usa `chromadb==1.5.9` con Python 3.14, lo que reduce el riesgo.

## 3. Arquitectura

### 3.1 Flujo

El sistema trabaja en dos momentos separados.

**Momento A: preparación (una sola vez).** Se arman las Knowledge Bases: cada Document de cada Area se corta en Sections y se guarda en el vector store, con una colección por Area (HR, Tech, Finance). Se hace una vez y queda guardado, porque repetirlo en cada consulta sería lento y caro: cada guardado usa la API de OpenAI. Volver a correrlo no reindexa (ver 3.2).

**Momento B: cada Query.**

```
1. Llega la Query:          "¿Cuántos días de vacaciones tengo?"
2. El Router produce una Route:   hr | tech | finance | out_of_scope
3. El Specialist del Area busca las Sections más parecidas en su Knowledge Base
4. El Specialist responde usando solo esas Sections (o se abstiene si ninguna supera el umbral)
5. El Judge califica la Answer (cuatro Ratings de 1 a 10)
```

**Los pasos 2 a 4 son un grafo de LangGraph** (`StateGraph`): un nodo `route`, una arista condicional que lee `Route.target`, un nodo por Specialist y un nodo `out_of_scope`. La selección del Specialist **es** la arista condicional; no hay un módulo aparte que elija. LangGraph vive solo en la capa de composición (`multi_agent_system.py`, `build_graph`); `routing/`, `specialists/` y `judging/` aportan Runnables y callables ya construidos que el grafo invoca.

**El paso 5 corre fuera del grafo, pero dentro de la misma traza.** `build_answer_query(graph, judge, publisher)` devuelve `answer_query`, que envuelve `graph.invoke` en un span de Langfuse; después del grafo, si corresponde, llama al Judge y publica los scores sobre esa traza a través del puerto `ScorePublisher` (3.4). Así el grafo solo enruta y responde, y mover el Judge a un proceso aparte más adelante es cambiar tres líneas sin tocar el routing. En esta entrega el Judge corre **sincrónico**: sí suma latencia; es una decisión de alcance, no una propiedad del diseño.

**Reglas del flujo:**

- **Una Query → una Route.** Si la Query pide dos cosas de Areas distintas ("¿cuánto cuesta sumar 10 usuarios y cómo los doy de alta?"), el Router elige el Area que resuelve el **pedido principal** (la primera acción concreta que alguien tendría que hacer) y el Specialist responde lo que su Knowledge Base cubre. Responder las dos mitades es una limitación conocida, documentada en el README.
- **Out of Scope** (la Query no es de Atalaya, por ejemplo "¿quién ganó el partido?"): no se llama a ningún Specialist; se responde con `OUT_OF_SCOPE_MESSAGE`.
- **Abstention** (la Query es del Area pero ninguna Section supera el umbral): el Specialist responde con `NO_INFORMATION_MESSAGE` **sin llamar al LLM**. Es distinta de Out of Scope: la pregunta era legítima, pero no está documentada.
- **El Judge califica solo Answers grounded.** Out of Scope y Abstention **no se juzgan**: con cero Sections, el Judge no puede distinguir una abstención correcta de una falsa (umbral demasiado alto) y gastaría una llamada a `gpt-4.1` para devolver ruido. En su lugar, cada traza lleva un score booleano `abstained` (1 o 0), para que el equipo filtre y revise las abstenciones a mano. Las abstenciones falsas se detectan offline con el Check de retrieval (sección 5).

Langfuse graba los pasos 1 a 5 como una sola **traza**. `SupportAnswer` lleva el `trace_id` para que el notebook muestre el link.

**Diagrama animado del flujo:** https://claude.ai/artifact/VaNc6rmJabNk9EpwJww7Y8

### 3.2 Embeddings y vector store

Se toman las mismas decisiones que en `RAG-Concepts/M2-Project`, pero implementadas con LangChain en lugar de llamar directo a `openai` y `chromadb`.

| Decisión | M2-Project (a mano) | Este proyecto (LangChain) |
|---|---|---|
| Modelo de embedding | `text-embedding-3-small` | `OpenAIEmbeddings(model=settings.embedding_model)` |
| Configuración | `Settings` + env var `EMBEDDING_MODEL` | Igual |
| Vector store | `chromadb.PersistentClient`, distancia coseno | `Chroma(persist_directory=..., embedding_function=..., collection_metadata={...})` |
| Distancia | coseno | **Hay que pedirla explícitamente**: `collection_metadata={"hnsw:space": "cosine"}`. El default de Chroma es L2, y con L2 el umbral de 3.5 no significa nada |
| Protección contra mezclar modelos | El nombre del modelo va en la metadata de la colección; si no coincide, da error | Igual: `collection_metadata={"hnsw:space": "cosine", "embedding_model": "..."}` |

Se usa el **mismo modelo** para guardar las Sections y para convertir las Queries. Si no, los vectores no son comparables.

**Reindexado.** `index_all_areas(force=False)` es idempotente:

- Si la colección del Area existe, tiene documentos y su metadata dice el mismo modelo de embedding → **la salta** y lo informa.
- Si el modelo no coincide → **error**.
- Si no existe → la crea e indexa.
- `force=True` borra la colección y la reconstruye. Se usa cuando cambiaron los Documents o el corte.
- Cada Section se agrega con un **ID determinista** (`f"{area}:{section_title}"`), así ni un `force` interrumpido genera duplicados. Importa porque `add_documents` no deduplica por contenido, y tres copias de la misma Section ocuparían los tres lugares de `top_k`.

### 3.3 Modelos por rol

Cada rol recibe su propio objeto de modelo. `llm.py` expone `build_chat_model(model_name, api_key, temperature)` y `multi_agent_system.py` lo llama una vez por rol con el nombre que lee de `Settings`.

| Rol | Variable de entorno | Modelo | Por qué |
|---|---|---|---|
| Router | `ROUTER_MODEL` | `openai:gpt-4o-mini` | Clasificar en 4 opciones es una tarea acotada. Corre en cada Query y antes de responder, así que conviene que sea rápido y barato |
| Specialists (HR, Tech, Finance) | `SPECIALIST_MODEL` | `openai:gpt-4o-mini` | Responden con las Sections recuperadas: el trabajo pesado lo hace la búsqueda |
| Judge | `JUDGE_MODEL` | `openai:gpt-4.1` | Juzgar relevancia, completitud y precisión exige más razonamiento. El juez debe ser más capaz que el generador para detectar sus errores |

Si la accuracy del Router sobre los Test Queries da baja, el orden de ajuste es: (1) mejorar las descripciones de las Areas en el prompt, (2) subir el modelo, (3) agregar few-shots **nuevos**, nunca sacados de `test_queries.json`. La decisión se toma con datos.

**Configuración (`config.py`).** `Settings` pasa a `pydantic-settings` (`BaseSettings` + `SettingsConfigDict(env_file=".env")`): cada campo se declara una vez con tipo, default y validación, y `load_settings()` queda como `return Settings()`. Campos:

| Variable | Default | Sección |
|---|---|---|
| `OPENAI_API_KEY` | — (obligatoria) | — |
| `ROUTER_MODEL`, `SPECIALIST_MODEL`, `JUDGE_MODEL` | ver tabla | 3.3 |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | 3.2 |
| `LLM_TEMPERATURE` | `0.0` | — |
| `SIMILARITY_THRESHOLD` | `0.42` | 3.5 |
| `RETRIEVAL_TOP_K` | `3` | 3.6 |
| `CHUNK_MAX_TOKENS`, `CHUNK_OVERLAP_TOKENS` | `800`, `120` | 3.6 |
| `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` | — | 2 |

### 3.4 Estructura de carpetas

Estructura modular: cada carpeta tiene una sola responsabilidad y lleva el nombre del término del glosario.

**Diagrama animado de la estructura:** https://claude.ai/artifact/6G98oFCTgV964vGh3r2Vat

```
CONTEXT.md                  ← glosario (manda sobre este plan)
docs/adr/                   ← decisiones difíciles de revertir
data/
  hr_docs/  tech_docs/  finance_docs/   ← Documents de cada Knowledge Base (.md)
  .chroma/                              ← índice persistido (en .gitignore)
src/orchestration/
  config.py                 ← Settings (pydantic-settings) + load_settings()
  llm.py                    ← build_chat_model(model_name, api_key, temperature)
  area.py                   ← Area (StrEnum: hr | tech | finance) + AREA_DESCRIPTIONS
  section.py                ← RetrievedSection(title, text, similarity)
  multi_agent_system.py     ← composición: build_graph(router, specialists) + build_answer_query(graph, judge, publisher) → answer_query(query) → SupportAnswer
  routing/
    route.py                ← Route(reasoning, target: hr | tech | finance | out_of_scope)
    router.py               ← ROUTER_PROMPT + build_router(chat_model) → Runnable[str, Route]
  specialists/
    specialist.py           ← SPECIALIST_PROMPT + build_specialist(area, retrieve, chat_model, threshold) → SpecialistReply
    out_of_scope.py         ← OUT_OF_SCOPE_MESSAGE
  judging/
    quality_verdict.py      ← QualityVerdict (quality, relevance, completeness, accuracy: 1-10; reason)
    answer_judge.py         ← JUDGE_PROMPT + build_judge(chat_model) → Runnable[..., QualityVerdict]
  knowledge_base/           ← interfaz pública: index_all_areas(...), build_retrieve(...)
    document_loader.py      ← load_area_documents(area_dir)            (interno)
    chunker.py              ← split_into_sections(documents)           (interno, con test propio)
    vector_store.py         ← colecciones de Chroma (coseno + control del modelo) + build_retrieve
    indexer.py              ← index_all_areas(force=False)
  checks/
    test_query.py           ← TestQuery + load_test_queries(path, split)
    checks.py               ← routing_correct, retrieval_hit, abstained
    threshold_sweep.py      ← sweep_threshold(retrieve_by_area, test_queries, thresholds)
  observability/
    tracing.py              ← init_langfuse(public_key, secret_key, host)
    score_publisher.py      ← ScorePublisher (Protocol) + LangfuseScorePublisher
    experiments.py          ← upload_test_queries(...), run_validation_experiment(...)
tests/                      ← un paquete de tests por paquete de src/, sobre su interfaz pública
multi_agent_system.ipynb    ← demo en 6 secciones, usa answer_query()
```

| Carpeta / archivo | Responsabilidad | Tipo |
|---|---|---|
| `multi_agent_system.py` | Armar el grafo (`build_graph`) y `answer_query` (`build_answer_query`) a partir de piezas ya construidas, y conectarlas con Settings, Chroma y Langfuse. No tiene lógica propia: los prompts viven en cada paquete | Composición |
| `area.py`, `section.py` | Tipos compartidos del dominio: `Area` (con sus descripciones) y `RetrievedSection`. Los produce la infraestructura y los consume la lógica del negocio, por eso viven en la raíz | Tipos del dominio |
| `routing/` | Decidir a qué Area va la Query (prompt + `Route`) | Lógica del negocio |
| `specialists/` | Responder usando las Sections del Area (retrieve → umbral → abstención \| LLM) | Lógica del negocio |
| `judging/` | Ponerle Ratings a una Answer (prompt + `QualityVerdict`) | Lógica del negocio |
| `checks/` | Comparar resultados con lo esperado, sin LLM: `TestQuery`, los tres Checks y el barrido del umbral | Lógica del negocio |
| `knowledge_base/` | Preparar y buscar Sections en Chroma. Interfaz pública de dos funciones: `index_all_areas` y `build_retrieve`; el resto es interno | Infraestructura |
| `observability/` | Comunicarse con Langfuse (cliente, scores, datasets, experimentos) | Infraestructura |
| `config.py`, `llm.py` | Leer el `.env`; construir modelos | Configuración |

**Reglas**

1. **La lógica del negocio no conoce la infraestructura.** `routing/`, `specialists/`, `judging/` y `checks/` no importan Langfuse, Chroma ni LangGraph. Reciben lo que necesitan como parámetro. Por ejemplo, el Judge devuelve un `QualityVerdict` y es `observability/` quien lo publica en Langfuse.
2. **Cada paquete de negocio construye su propio Runnable; la composición los recibe ya construidos** (ADR 0003). `routing/` expone `build_router(chat_model)` (`ROUTER_PROMPT | chat_model.with_structured_output(Route)`), `judging/` expone `build_judge(chat_model)` y `specialists/` expone `build_specialist(area, retrieve, chat_model, threshold)`. `build_graph(router, specialists)` y `build_answer_query(graph, judge, publisher)` reciben esas piezas y nunca las arman. El seam de testeo está en la composición: los tests del grafo y de `answer_query` inyectan `RunnableLambda` con `Route` / `QualityVerdict` fijos, un `retrieve` falso que devuelve `RetrievedSection` con Similarities inventadas y un `RecordingScorePublisher`. `build_router` y `build_judge` no tienen test unitario: sin modelo no hay nada que probar; su prueba es el Check `routing_correct` y la corrida de integración. Motivo del seam: los modelos falsos de `langchain_core` no implementan `bind_tools`, así que `with_structured_output` falla con ellos.
3. **`config.py` se lee una sola vez**, en `multi_agent_system.py`, y cada módulo recibe solo el dato que necesita (`init_langfuse` recibe tres strings, no `Settings`). Ningún otro módulo llama a `load_settings()`.
4. **Nombres que dicen qué hacen, con el vocabulario de `CONTEXT.md`.** Los archivos llevan el nombre de su responsabilidad (`router.py`, `answer_judge.py`) y las funciones son verbo + objeto (`build_router`, `build_specialist`, `publish_quality_scores`).
5. **Los tests replican los paquetes de `src/` y prueban su interfaz pública, no cada archivo.** Un test directo de un archivo interno solo si tiene lógica propia (en `knowledge_base/`, solo `chunker.py`). Los tests de `knowledge_base/` usan Chroma en memoria (`Chroma(collection_name=..., embedding_function=...)`, sin `persist_directory`) y `DeterministicFakeEmbedding` de `langchain_core.embeddings`: indexan un `.md` chico con tres `##` y verifican tres Sections, IDs deterministas, que una segunda corrida no reindexa, que un modelo de embedding distinto da error y que `build_retrieve` devuelve `RetrievedSection`. Por eso `index_all_areas` y `build_retrieve` reciben `embeddings` y `persist_directory` (`None` = memoria) como parámetros.

**Estado del grafo y resultado.**

```python
class SupportState(TypedDict):
    query: str
    route: Route | None                 # Route.target: hr | tech | finance | out_of_scope
    sections: list[RetrievedSection]    # las que superaron el umbral
    answer: str | None
    abstained: bool

class SupportAnswer(BaseModel):
    query: str
    route: Route
    answer: str
    sections: list[RetrievedSection]    # las usadas, para mostrar fuentes en el notebook
    abstained: bool
    verdict: QualityVerdict | None      # None en Out of Scope y Abstention
    trace_id: str
```

**Seam con Langfuse.** `observability/score_publisher.py` define el `Protocol` `ScorePublisher`, con `publish_quality_scores(trace_id, verdict)` y `publish_abstention(trace_id, abstained)`. En producción lo implementa `LangfuseScorePublisher(client)`; en los tests, un `RecordingScorePublisher` que guarda las llamadas en una lista. Dos adaptadores, producción y test, hacen que el seam sea real. Sin él, la regla "no se juzga, se marca" (3.1) no se podría verificar sin keys: sin keys el cliente de Langfuse se deshabilita y `create_score` es un no-op silencioso. Pendiente de verificar en el ticket 02: qué `trace_id` devuelve un span con el cliente deshabilitado; afecta solo a lo que los tests aceptan en `SupportAnswer.trace_id`.

### 3.5 Umbral de similitud

Cada Section recuperada trae una **Similarity** con la Query (0 a 1). Las Sections por debajo del **Similarity Threshold** se descartan. Si no queda ninguna, el Specialist se abstiene sin llamar al LLM (3.1).

- **Valor inicial: `0.42`**, el mismo de M2-Project. Ahí el barrido (`outputs/threshold_sweep.json`, `top_k=3`) mostró que entre 0.40 y 0.44 se mantenía 100% de recall y se bloqueaban las 5 preguntas trampa.
- **Calibración:** cuando estén los Documents, se repite el barrido con los Test Queries de cada Area, incluidas preguntas trampa, y se elige el valor del medio de la zona buena. Hace falta porque las Similarities dependen de los Documents y del tamaño de las Sections, que acá cambian. El barrido corre en local y sin LLM (sección 5.5).
- **Rol en este sistema:** es la segunda red de seguridad. El primer filtro de preguntas fuera de tema es el Router (Out of Scope). El umbral atrapa Queries que parecen de un Area pero cuya respuesta no está en su Knowledge Base.
- Se configura en `Settings` con la variable `SIMILARITY_THRESHOLD`.

### 3.6 Corte y búsqueda

**Corte (en `knowledge_base/chunker.py`).** Se encadenan dos piezas de LangChain, que reemplazan al `split_manual` de M2-Project:

| Paso | Pieza | Qué hace |
|---|---|---|
| 1 | `MarkdownHeaderTextSplitter` | Corta en cada `##`. Guarda el título de la Section como metadata, para citarlo como fuente |
| 2 | `RecursiveCharacterTextSplitter` (largo medido con tiktoken) | Red de seguridad: solo actúa si una Section supera los **800 tokens**, y la parte con **120 tokens de solapamiento** (15%), igual que en M2 |

- El título de la Section queda **también dentro del texto**, no solo en la metadata, porque ayuda a la búsqueda.
- `CHUNK_MAX_TOKENS` y `CHUNK_OVERLAP_TOKENS` se configuran en `Settings`. "Chunk" es el término del splitter y solo aparece en este módulo; para el resto del sistema la unidad es la Section (por diseño, 1 Section = 1 chunk; sección 4.3).

**Búsqueda (`build_retrieve` en `knowledge_base/vector_store.py`).**

- `build_retrieve(area, top_k, embeddings, persist_directory)` devuelve el `retrieve: Callable[[str], list[RetrievedSection]]` que recibe el Specialist. Por dentro usa `similarity_search_with_relevance_scores(query, k=top_k)`, que devuelve `(Document, Similarity)` con Similarity en 0-1 cuando la colección es coseno, y convierte cada par en un `RetrievedSection(title, text, similarity)`. Es el único lugar donde se lee la metadata del `Document`; de ahí en adelante nadie conoce LangChain `Document`.
- El umbral se aplica **en Python, en el Specialist**, no en `retrieve`. No se usa `as_retriever(search_type="similarity_score_threshold")` porque filtra adentro y esconde la Similarity, que el barrido de calibración necesita ver. El mismo `retrieve` sirve para responder y para calibrar.
- **`top_k = 3`**: trae las 3 Sections más parecidas y después el umbral (3.5) descarta las que no alcanzan. En el barrido de M2 el recall fue 100% desde `top_k=2`, así que 3 deja una Section de margen sin sumar demasiado ruido.
- Se configura en `Settings` con la variable `RETRIEVAL_TOP_K`.

### 3.7 Router

- **Construcción:** `routing/router.py` expone `build_router(chat_model) -> Runnable[str, Route]`, que arma `ROUTER_PROMPT | chat_model.with_structured_output(Route)`. El prompt vive en `routing/`, no en la composición.
- **Salida estructurada:** `Route(reasoning, target)`, obtenida con `with_structured_output(Route)` (modo JSON estricto de OpenAI; no falla el parseo). `target` es `Literal["hr", "tech", "finance", "out_of_scope"]`: se llama `target` y no `area` porque Out of Scope es una Route, no un Area (`CONTEXT.md`). Un test verifica que ese `Literal` es exactamente los valores de `Area` más `out_of_scope`. `reasoning` va **primero** en el esquema: el modelo razona antes de decidir, y la razón queda grabada en la traza, así cuando una Query se enruta mal se ve por qué sin volver a correr nada.
- **Prompt zero-shot:** describe cada Area por **qué resuelve** (la regla de 4.4) con 2-3 líneas derivadas de los bloques de 4.5, y `out_of_scope` para todo lo que no sea de Atalaya. Esas descripciones son `AREA_DESCRIPTIONS` en `area.py`, la misma fuente que usa el prompt del Specialist: si cambia la regla para un tema, se toca un solo texto. **Cero Test Queries en el prompt**: si los ejemplos frontera del prompt fueran también Test Queries, la accuracy medida sería mentira.

### 3.8 Judge

- **Entrada:** Query, Answer **y las Sections usadas**. La consigna pide juzgar "basado en la consulta y la respuesta", pero sin las Sections el Judge no puede saber si la Answer es correcta *según la documentación*: solo si suena plausible. Pasar las Sections es un superconjunto de lo que pide la consigna y lo único que hace que *accuracy* signifique algo (groundedness).
- **Construcción:** `judging/answer_judge.py` expone `build_judge(chat_model) -> Runnable[..., QualityVerdict]`, que arma `JUDGE_PROMPT | chat_model.with_structured_output(QualityVerdict)`. El formateo de las Sections para el modelo ocurre dentro de la plantilla del prompt.
- **Salida (`QualityVerdict`):** cuatro Ratings de 1 a 10 — `relevance`, `completeness`, `accuracy` (los Dimensions del objetivo 6) y `quality` (el global que pide la consigna) — y `reason`. Sale todo de **una sola llamada** con `with_structured_output`.
- **Publicación:** `answer_query` manda los cuatro como scores de Langfuse sobre la misma traza a través del puerto `ScorePublisher` (`publish_quality_scores`). Así se puede filtrar "Answers con accuracy < 5" y encontrar retrievals fallidos (objetivo 3).
- Qué no se juzga: ver reglas del flujo en 3.1.

## 4. Documentos

Los Documents los generó un LLM a pedido del autor, siguiendo el formato y los límites de esta sección; el autor los revisa antes de usarlos.

### 4.1 La empresa: Atalaya Data

- **Qué es:** una empresa SaaS mediana (400 a 500 personas). Es ficticia y no copia ninguna marca real.
- **Qué vende:** una plataforma que integra datos de distintos organismos públicos, los analiza y los muestra en tableros, con control estricto de accesos y registro de auditoría.
- **Clientes:** administraciones públicas, como ministerios, gobiernos provinciales, municipios y organismos de salud y de seguridad.

Cumple lo que pide la consigna: una "empresa SaaS mediana que gestiona consultas de clientes".

### 4.2 Quién pregunta (Asker)

El sistema atiende a dos tipos de Asker:

| Asker | Qué pregunta |
|---|---|
| **Client** (usuarios de los organismos) | Sobre todo Tech (accesos, uso de la plataforma, incidentes) y Finance (facturas, órdenes de compra, contratos) |
| **Staff** (empleados y consultores de Atalaya) | Las tres Areas. HR es mayormente para ellos: habilitaciones de seguridad, licencias, guardias y trabajo en las oficinas del cliente |

Una misma palabra puede significar cosas distintas según quién pregunta. Por ejemplo, "factura" puede ser la que recibe el organismo o un gasto que rinde un empleado. Eso genera casos borde para probar el Router.

### 4.3 Extensión y formato

| Knowledge Base | Extensión mínima | Sections aprox. |
|---|---|---|
| `data/hr_docs/` | 9.000 palabras | 55-60 |
| `data/finance_docs/` | 9.000 palabras | 55-60 |
| `data/tech_docs/` | 11.000 palabras | 65-70 |

- El formato es el mismo estilo que el manual de M2-Project: título, línea de versión, una introducción corta y secciones `##`.
- **Un tema por Section**, en 1 o 2 párrafos (~150-200 palabras). Si una Section cubre dos temas, se parte en dos. Así las palabras extra se convierten en más Sections, no en Sections más largas.
- Las Sections quedan muy por debajo del máximo de 800 tokens, así que **1 Section = 1 chunk**. Con más de 55 Sections hay margen sobre los 50 chunks que exige la consigna. Un test lo verifica.
- Referencia medida en M2: ~1,5 tokens por palabra y ~380 tokens por Section.

### 4.4 Límites entre Areas (ADR 0001)

**Regla:** cada tema va en el Area que **resuelve** lo que la persona pide. No importa de qué trata la pregunta, sino quién hace algo para contestarla.

**Cada respuesta vive en una sola Knowledge Base.** Si estuviera en dos, el Router podría enviar la Query a cualquiera de las dos y ambas serían correctas, así que no se podría medir si clasificó bien.

Ejemplos de temas en la frontera (Frontier Queries), resueltos con la regla:

| Query | Area | Por qué |
|---|---|---|
| "¿Cuándo me entregan la notebook?" | HR | Es parte de la incorporación |
| "Mi notebook nueva no conecta a la VPN" | Tech | Hay que arreglar un sistema |
| "Me voy de la empresa, ¿qué tengo que hacer?" | HR | Es la baja laboral |
| "Un analista se fue del ministerio, ¿cómo le saco el acceso?" | Tech | Hay que revocar un acceso |
| "¿Cuánto cuesta sumar 10 usuarios?" | Finance | Es precio y licencias |
| "¿Cómo doy de alta a esos 10 usuarios?" | Tech | Es una tarea en la plataforma |
| "¿Cuándo cobro el sueldo?" | Finance | Finance hace el pago |
| "¿Cuándo es la revisión salarial?" | HR | Es una condición laboral |

Estos casos de frontera se usan también como Test Queries del Router.

### 4.5 Bloques de temas por Area

Son los grandes bloques de cada Document. Cada bloque se parte en varias Sections de un tema cada una.

#### HR (`data/hr_docs/`, 55-60 Sections)

| Bloque | Asker | Ejemplos de Sections |
|---|---|---|
| Incorporación | Staff | Verificación de antecedentes, primer mes, entrega de equipo |
| Habilitaciones de seguridad | Staff | Niveles, cómo se tramitan, renovación, qué pasa si se pierde una |
| Confidencialidad y ética | Staff | Acuerdo de confidencialidad, regalos de funcionarios, conflictos de interés |
| Licencias y ausencias | Staff | Vacaciones, enfermedad, licencia parental, cómo pedirlas |
| Modalidad de trabajo | Staff | Trabajo en oficinas del cliente, remoto, guardias, horarios |
| Desarrollo | Staff | Evaluaciones, formación obligatoria, revisión salarial |
| Salida de la empresa | Staff | Renuncia, preaviso, qué pasa con la habilitación al irse |
| Consultores asignados | Client | Quién es su consultor, cómo pedir un reemplazo, qué habilitación tiene |

#### Tech (`data/tech_docs/`, 65-70 Sections)

| Bloque | Asker | Ejemplos de Sections |
|---|---|---|
| Acceso a la plataforma | Client | Alta de usuarios, recuperar contraseña, doble factor, cuenta bloqueada |
| Roles y permisos | Client | Roles disponibles, quién puede asignarlos, baja de un usuario que se fue |
| Clasificación de datos | Client | Niveles (público, reservado, secreto), quién ve cada nivel, cómo reclasificar |
| Fuentes de datos | Client | Conectar una base del organismo, formatos aceptados, frecuencia de actualización, errores de carga |
| Tableros y exportaciones | Client | Crear un tablero, compartirlo, exportar a CSV o PDF, límites de exportación |
| Auditoría | Client | Qué queda registrado, cómo consultar quién vio un dato, cuánto tiempo se guardan los registros |
| Despliegue y mantenimiento | Client | Nube o servidores del organismo, ventanas de mantenimiento, avisos de actualización |
| Soporte e incidentes | Ambos | Cómo reportar, niveles de severidad, tiempos de respuesta, seguimiento de un ticket |
| Seguridad interna | Staff | VPN, phishing, qué hacer ante un incidente de seguridad, uso de USB |
| Equipamiento | Staff | Configuración de la notebook, software permitido, pedir un periférico, reemplazo por falla |

#### Finance (`data/finance_docs/`, 55-60 Sections)

| Bloque | Asker | Ejemplos de Sections |
|---|---|---|
| Contratación con el Estado | Client | Cómo contratar a Atalaya (licitación o contratación directa), documentación que presentamos, garantías de contrato |
| Órdenes de compra | Client | Qué datos tiene que tener la orden, a quién se envía, qué pasa si tiene errores |
| Facturación a organismos | Client | Cuándo se emite la factura, dónde descargarla, datos fiscales, cómo pedir una corrección |
| Pagos y cobranzas | Client | Plazos de pago, medios de pago, qué pasa si el pago se atrasa, constancias |
| Precios, licencias y renovaciones | Client | Cómo se calcula el precio, sumar usuarios, renovación anual, ajustes de precio, notas de crédito |
| Gastos y viáticos | Staff | Viáticos por trabajo en oficinas del cliente, topes, cómo rendir, plazos de reintegro |
| Tarjeta corporativa | Staff | Quién la tiene, límites, gastos no permitidos, qué hacer si se pierde |
| Sueldos y recibos | Staff | Fecha de cobro, dónde ver el recibo, cómo leer los descuentos, cambio de cuenta bancaria |

Casos ambiguos resueltos con la regla de 4.4:

- **"Factura":** la del organismo va en *Facturación a organismos*. El comprobante de un gasto del empleado va en *Gastos y viáticos*. Son Sections distintas del mismo Document.
- **"Sueldo":** cuándo y cómo se cobra es Finance (*Sueldos y recibos*). Cuánto se cobra y cuándo aumenta es HR (*Desarrollo*).

## 5. Test Queries

Archivo: `test_queries.json`. Se escriben **después de los Documents**, porque `expected_section` tiene que coincidir con un título real.

### 5.1 Para qué se usan

Cada uso es un **Check**: una comparación determinista, sin LLM, entre lo que hizo el sistema y lo esperado. Viven en `checks/checks.py` como funciones puras con la firma `(SupportAnswer, TestQuery) -> bool`.

| Check | Pregunta que responde | Sobre qué tipos |
|---|---|---|
| `routing_correct` | ¿`route.target` == `expected_area`? | Todos |
| `retrieval_hit` | ¿`expected_section` está entre las Sections usadas? | `direct`, `frontier` |
| `abstained` | ¿El Specialist se abstuvo? (debe ser sí en `unanswerable`, no en el resto) | Todos los que tienen Area |

`retrieval_hit` en falso sobre una `direct` es una **abstención falsa** o un retrieval fallido: es la forma de detectar un umbral demasiado alto (3.1).

### 5.2 Composición (~48 consultas)

| Tipo | Cantidad | Ejemplo | Qué prueba |
|---|---|---|---|
| `direct` | 24 (8 por Area, mezclando `client` y `staff`) | "¿Cómo exporto un tablero a PDF?" → tech | El caso normal |
| `frontier` | 12 | "¿Cuándo cobro el sueldo?" → finance | La regla de 4.4 |
| `out_of_scope` | 5 | "¿Quién ganó el partido?" → out_of_scope | La cuarta opción del Router |
| `unanswerable` | 7 (2 o 3 por Area) | "¿Cuál es la política de mascotas en la oficina?" → hr, sin respuesta en el Document | El umbral y la Abstention |

Por qué 48 y no 10:

- Con pocas consultas, cada error mueve mucho la accuracy: con 24, cada fallo pesa ~4 puntos.
- El umbral necesita varios casos negativos para calibrarse bien.
- Se cubre una parte razonable de las ~180 Sections sin que escribirlas y mantenerlas sea una carga excesiva.

No hay un tipo para Queries multi-área: "una Query → una Route" (3.1) es una limitación aceptada, y medirla sería medir una capacidad que decidimos no tener.

### 5.3 Calibración y validación separadas

Si el umbral se calibra con las mismas consultas con las que después se mide, el resultado sale demasiado optimista. Por eso se separan:

- **`calibration` (~2/3):** se usan para elegir el umbral.
- **`validation` (~1/3):** se usan solo al final, para medir.

Las proporciones de cada tipo se mantienen en los dos grupos.

### 5.4 Formato

```json
{
  "id": "tech-03",
  "query": "¿Cómo exporto un tablero a PDF?",
  "expected_area": "tech",
  "expected_section": "Exportar un tablero a PDF",
  "asker": "client",
  "type": "direct",
  "split": "calibration"
}
```

- `expected_area`: `hr` | `tech` | `finance` | `out_of_scope`
- `expected_section`: título exacto de la Section con la respuesta. Va en `null` en `out_of_scope` y `unanswerable`.
- `asker`: `client` | `staff`
- `type`: `direct` | `frontier` | `out_of_scope` | `unanswerable`
- `split`: `calibration` | `validation`

### 5.5 Cómo se corre (híbrido)

- **Lectura de los Test Queries:** `checks/test_query.py` define el modelo `TestQuery` (los campos de 5.4) y `load_test_queries(path, split)`, que lee `test_queries.json` y filtra por split.
- **Barrido del umbral → local**, sobre el split `calibration`. `checks/threshold_sweep.py` expone `sweep_threshold(retrieve_by_area, test_queries, thresholds) -> list[SweepPoint]`: una función pura que prueba ~20 valores de umbral comparando Similarities; **no llama al LLM** ni crea trazas. El notebook la llama y guarda `outputs/threshold_sweep.json`, como en M2. Hacerlo como experimentos de Langfuse serían 20 corridas que ensucian el proyecto para nada.
- **Medición final → experimento en Langfuse**, sobre el split `validation`. `observability/experiments.py` sube `test_queries.json` como Dataset (`input` = query, `expected_output` = `{area, section, type}`) y corre `dataset.run_experiment(task=answer_query, evaluators=[los tres Checks])`. Cada ítem queda vinculado a su traza; en la UI se ve la accuracy por corrida y se puede comparar "prompt v1 vs v2" o "gpt-4o-mini vs gpt-4.1" lado a lado. Esa es la corrida que muestran el notebook y el README.
- Los Checks son funciones puras de `checks/checks.py`; `experiments.py` solo adapta `TestQuery` a ítem de Dataset y cada Check a la firma `Evaluation` de Langfuse.

## 6. Orden de construcción

**Idea clave:** el código no necesita los Documents reales para construirse. Cada ticket se prueba con un `.md` chico de ejemplo y con Runnables falsos que no llaman a OpenAI (regla 2 de 3.4). Así los Documents se escriben **en paralelo** con los tickets 01 a 07.

El trabajo está partido en **diez tickets** en `.scratch/support-routing/issues/` (spec completa en `.scratch/support-routing/PRD.md`). Son **cortes verticales**: cada ticket atraviesa routing, grafo, observabilidad y tests hasta algo que se puede demostrar, en lugar de terminar una capa entera antes de empezar la siguiente. El ticket manda sobre esta tabla si difieren.

| Ticket | Qué entrega | Bloqueado por | ¿Necesita los Documents reales? |
|---|---|---|---|
| 01 | **Preparación y tipos compartidos:** dependencias (confirmar Chroma en Python 3.14); `Settings` con `pydantic-settings` y las variables de 3.3; `llm.py` → `build_chat_model`; borrar `src/core/LLM.py`; `area.py` (`Area` + `AREA_DESCRIPTIONS`); `section.py` (`RetrievedSection`); `.env.example`; `.gitignore` (`.chroma/`); los bloques de la sección 7 **agregados arriba** del bloque `## Agent skills` que ya existe en `CLAUDE.md`; marker `integration` registrado y excluido por defecto | — | No |
| 02 | **Out of Scope de punta a punta:** `Route` (`reasoning`, `target`), `build_router` con `ROUTER_PROMPT`, nodo `out_of_scope`, `build_graph`, `build_answer_query` con el span de Langfuse, `init_langfuse`, `ScorePublisher` + `LangfuseScorePublisher`, score `abstained`. Los nodos de Area quedan como placeholders. Verificar qué `trace_id` devuelve un span con el cliente deshabilitado | 01 | No |
| 03 | **Knowledge Base: indexar y buscar:** `load_area_documents`, `split_into_sections`, colecciones de Chroma (coseno + control del modelo), `index_all_areas` idempotente con `force` e IDs deterministas, `build_retrieve` → `RetrievedSection`. Tests sobre la interfaz pública con Chroma en memoria y `DeterministicFakeEmbedding`; test propio solo para `chunker` | 01 (paralelo con 02) | No, usa un `.md` de prueba |
| 04 | **Answer grounded y Abstention de punta a punta:** `build_specialist` (retrieve → umbral → abstención \| LLM), `SpecialistReply`, los tres nodos de Area en el grafo, `SupportAnswer.sections` y `abstained`. Sin Judge todavía (`verdict` en `None`) | 02, 03 | No |
| 05 | **Judge:** `QualityVerdict`, `build_judge` con `JUDGE_PROMPT`, el Judge fuera del grafo solo para Answers grounded, los cuatro scores por `ScorePublisher` | 04 | No |
| 06 | **Checks y barrido del umbral:** `TestQuery`, `load_test_queries`, los tres Checks, `sweep_threshold` | 02 (paralelo con 03, 04 y 05) | No |
| 07 | **Experimento en Langfuse:** `upload_test_queries`, `run_validation_experiment` con los tres Checks adaptados | 05, 06 | No |
| 08 | **Primera corrida real:** **armar el sistema real** (`Settings` leído una vez en `multi_agent_system.py`, modelos, Chroma y Langfuse reales), indexar los Documents, barrido del umbral con `calibration` (local), elegir el umbral, medición final con `validation` (experimento en Langfuse), test de >50 Sections por Knowledge Base | 07 | **Sí**, Documents y Test Queries |
| 09 | **Notebook** `multi_agent_system.ipynb` con las 6 secciones de la consigna | 08 | Sí |
| 10 | **README** (con la tabla de mapeo de la sección 1, los resultados medidos y las limitaciones conocidas) y **`requirements.txt`** | 08 (paralelo con 09) | — |

**Frentes en paralelo:** 01 → 02 ∥ 03 → 04 → 05; 06 corre junto a 03, 04 y 05; 07 espera a 05 y 06; 09 ∥ 10 después de 08.

**Por qué este orden:** cada ticket deja algo que funciona y se puede ver en una traza, no una capa a medio conectar. El primero que atraviesa todo el sistema (02) es el camino más corto posible: Router → mensaje fijo → traza. Los siguientes lo ensanchan. Cuando se llega a un ticket, todo lo que usa ya existe y está probado.

**Decisiones abiertas** (anotadas en el ticket que las necesita; se confirman con el autor, no se inventan): cómo se saltan los tests de integración sin keys (01); las Queries de muestra de los tests de integración viven dentro de los tests y no entran a `test_queries.json` (02); el Document de muestra es un fixture de test, no un Document de Atalaya (03); si `outputs/` se versiona (01).

**Cómo se trabaja cada ticket (TDD):**

1. Se escribe un test que describe qué debe hacer la pieza. Falla, porque la pieza no existe.
2. Se escribe el código mínimo para que pase.
3. Se ordena el código sin romper el test.

- Los tests unitarios inyectan `RunnableLambda` con `Route` / `QualityVerdict` fijos en lugar del router y del judge, un `retrieve` falso que devuelve `RetrievedSection` con Similarities inventadas, `FakeListChatModel` solo para el paso de redacción del Specialist (ahí es `invoke` plano y funciona) y un `RecordingScorePublisher` para `answer_query`. No consumen API. El Specialist no tiene tests propios: su umbral y su abstención se prueban a través de `answer_query`.
- Los tests de `knowledge_base/` usan Chroma en memoria y `DeterministicFakeEmbedding` (regla 5 de 3.4). Tampoco consumen API.
- Los tests que llaman a servicios reales (OpenAI, Langfuse, Chroma con embeddings) se marcan como `integration` y solo corren con las keys configuradas.
- Cada ticket termina con sus criterios de aceptación cumplidos y sus tests en verde, y se revisa antes de seguir.

## 7. CLAUDE.md

`CLAUDE.md` es el archivo que Claude Code lee automáticamente al empezar cada sesión en este repo. Ya existe con el bloque `## Agent skills`; los bloques de 7.2 se **agregan arriba de ese bloque en el ticket 01**, sin reemplazarlo, para que estén activos desde la primera línea de código.

### 7.1 Principios (guía `writing-for-agents`)

1. **Corto (~40-60 líneas).** Se carga en todas las sesiones, así que cada línea cuesta siempre.
2. **No repite `PLAN.md` ni `CONTEXT.md`: apunta a ellos.** Cada decisión vive en un solo lugar, para que no quede desactualizada en otro.
3. **Solo guarda lo que no se descubre mirando el repo:** convenciones no escritas, el porqué de una decisión, trampas. Lo que ya dicen `pyproject.toml` o `uv.lock` no se copia.

### 7.2 Contenido

| Bloque | Qué incluye |
|---|---|
| Qué es el proyecto | Dos líneas: sistema multi-agente de soporte para Atalaya Data. Punteros: antes de implementar un paso, leer `PLAN.md`; para nombrar cualquier cosa, usar `CONTEXT.md`; antes de "arreglar" algo que parece raro, leer `docs/adr/` |
| Comandos | `uv run pytest`, `uv run pytest -m integration`, `uv add` en lugar de `pip` |
| Reglas de arquitectura | La lógica del negocio (`routing/`, `specialists/`, `judging/`, `checks/`) no importa Langfuse, Chroma ni LangGraph. Cada paquete de negocio construye su propio Runnable (`build_router`, `build_judge`, `build_specialist`); `build_graph` y `build_answer_query` los reciben construidos. `config.py` se lee una sola vez, en `multi_agent_system.py`. Funciones con nombre verbo + objeto. Tests por paquete, sobre su interfaz pública |
| Forma de trabajo | Un paso del plan por vez, con TDD. Revisión del autor antes de seguir. Explicaciones simples, porque el autor está aprendiendo. Discutir antes de escribir en `PLAN.md` |
| Lo que escribe el autor | Los Documents de `data/` y `test_queries.json` los escribe el autor. Claude no los genera |
| Trampas conocidas | Mismo modelo de embedding para indexar y buscar. Chroma usa L2 por default: pedir coseno explícito. Los modelos falsos no soportan `with_structured_output`. `.chroma/` no se sube a git. Los tests unitarios no llaman a la API. Llamar a `langfuse.flush()` al final del notebook y de los scripts cortos |
| Idioma | Código, nombres, comentarios, tests, **system prompts** y `CONTEXT.md`/ADRs en inglés; los prompts indican "answer in the same language as the question". Los Documents de `data/`, `PLAN.md`, los **mensajes fijos al usuario** (`OUT_OF_SCOPE_MESSAGE`, `NO_INFORMATION_MESSAGE`), el `reason` del Judge y las explicaciones al autor en español |
