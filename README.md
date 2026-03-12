# Adaptive Diagnostic Engine

An **AI-powered adaptive testing system** that dynamically adjusts question difficulty based on a student's responses to efficiently estimate their proficiency. After the test completes, the system analyzes performance and generates a **personalized learning plan using an LLM (Groq GPT-OSS-20B)**.

This project was built as part of an AI engineering assignment focused on system design, adaptive algorithms, and practical AI integration using FastAPI, MongoDB, and Python.

## Core Features
1. **Adaptive Testing Engine:** Adjusts difficulty progressively (±0.1 increments smoothed at boundaries) using Item Response Theory principles.
2. **AI Study Plan Generation:** Uses session accuracy and topic modeling metadata to query Groq GPT for customized tutoring. 
3. **Interactive Terminal Experience:** Mock CLI environment designed to stream learning questions exactly as a student would experience them.

---

## 🚀 How to Run the Project

### 1. Prerequisites
Ensure you have Python 3.9+ and pip installed. You will also need access to a running MongoDB instance.

### 2. Setup the Environment
Clone the repository and spin up a virtual environment:

```bash
git clone https://github.com/yogimait/Adaptive-Diagnostic-Engine


# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Application Variables
Create a `.env` file in the root directory:

```env
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=adaptive_testing
TEST_LENGTH=10
ABILITY_START=0.5
ABILITY_STEP=0.1
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Seed the Database
Seed the local MongoDB instance with foundational GRE-style mathematical and vocabulary questions:
```bash
# Windows
venv\Scripts\python.exe seed\seed_questions.py

# Mac/Linux 
python seed/seed_questions.py
```

### 6. Start the API Server
Run the FastAPI backend using `uvicorn`:
```bash
# Windows
venv\Scripts\uvicorn.exe app.main:app --reload

# Mac/Linux
uvicorn app.main:app --reload
```
The server will be available at `http://127.0.0.1:8000`. You can passively verify backend health by visiting `http://127.0.0.1:8000/health`.


### 7. Run the built-in CLI demo to experience the adaptive test interactively. (Recommended)
You can take the adaptive test yourself via the built-in Terminal UI! Keep the `uvicorn` server running in a background process, open a new terminal, and run:
```bash
# Windows
venv\Scripts\python.exe cli_demo.py

# Mac/Linux
python cli_demo.py
```

---

## 🧠 Adaptive Algorithm Logic

The system utilizes an implementation of a 1-dimensional adaptive testing loop inspired by bounds-protected Item Response Theory (IRT). 

1. **Start Point**: Every student session initializes at a medium baseline `ability_score = 0.5`. 
2. **Evaluation & Update**: Each correct and incorrect answer modifies the estimated ability dynamically by an increment of `ABILITY_STEP` (default `0.1`). Note: Adjustments are intentionally smoothed out (i.e., halving step increments) near the absolute extremes (`< 0.2` and `> 0.9`) to prevent volatile difficulty spiking.
3. **Question Selector Loop**: The engine fetches an un-encountered question mapped as close to the newly calculated ability score as possible. To ensure a question is always found gracefully regardless of DB sparsity, the system iteratively widens its search radius by thresholds of `±0.05`, `±0.10`, `±0.20`, `±0.30`, up to `±1.0`. 

## 🤖 AI Log

Modern developer tooling was actively utilized during development to heavily accelerate architecture, configuration, and endpoint implementations.

### Tools Used
- **Antigravity (System AI Assistant)**: Acted as primary collaborator managing iterative project scaffolding, file orchestration, code implementation, and Python runtime execution directly on the integrated workspace. 
- **ChatGPT**: Primarily consulted iteratively for resolving theoretical edge cases, establishing structured architecture patterns prior to generation, and debugging LLM prompt hallucinations.

### Challenges Faced & Resolved Context
1. **Preventing Question Repetition** 

Adaptive engines must recall previously iterated arrays to avoid repeat querying. Addressed functionally cleanly by implementing a historical query array inside the internal MongoDB `Session` tracking data structure passed as a strict `$nin` exclusion operator to the database.

2. **Token Consumption by Reasoning Models**

The `openai/gpt-oss-20b` model used via Groq is a reasoning-oriented model that may internally generate reasoning tokens before producing a final answer. During testing this occasionally caused truncated or empty outputs because the token budget was consumed during the model's internal reasoning phase.

To resolve this issue:
- The system prompt was redesigned to discourage internal reasoning.
- Temperature was lowered to encourage deterministic responses.
- Output format constraints were enforced.
- A fallback response was implemented to guarantee a valid study plan even if the model returns empty output.

---

For detailed API definitions, see the [API_Documentation.md](API_Documentation.md) file.
