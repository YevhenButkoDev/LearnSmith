To build this AI Mentor, you need an architecture that supports **stateful learning**. Because the AI generates content on the fly, the app must "remember" what you've already learned and where you struggled.

### 1. High-Level Technical Stack

The goal is to keep the "Brain" (LLM) separate from the "Memory" (Database) and the "Execution" (Sandbox).

|**Layer**|**Recommended Technology**|**Why?**|
|---|---|---|
|**Backend**|**Python (FastAPI)**|Best ecosystem for AI (LangChain, LangGraph).|
|**LLM Orchestrator**|**LangGraph**|Perfect for "looping" logic where the AI checks its own work.|
|**Primary Database**|**PostgreSQL (with pgvector)**|Stores user profiles, course structures, and vector embeddings for RAG.|
|**Code Sandbox**|**E2B or Piston API**|Safely runs the user's SQL or Python code to check for correctness.|
|**Frontend**|**Next.js (React)**|Provides a smooth, real-time "chat + workspace" interface.|

---

### 2. The Course Data Architecture

You shouldn't store the course as one giant text block. Store it as a **Graph** or a **Nested JSON**.

- **The Master Plan:** A high-level list of `Modules`.
    
- **The Atomic Unit:** A `Lesson` object containing:
    
    - `content_markdown`: The theory text.
        
    - `key_concepts`: List of keywords for later review.
        
    - `task_prompt`: The challenge for the user.
        
    - `validation_logic`: The "hidden" criteria or unit tests to pass.
        

---

### 3. The "Read → Solve → Progress" Workflow

This is the core logic of your application. The app shouldn't just show text; it should act as a **Gatekeeper**.

#### A. Content Delivery (The "Read" Phase)

The app pulls the next `Lesson` from the database.

- **Action:** The UI renders Markdown text and code snippets.
    
- **UI Tip:** Use a "Progressive Disclosure" UI—don't show the task until the user clicks "I've read this."
    

#### B. The Challenge (The "Solve" Phase)

The app switches to an interactive mode (e.g., a SQL console or a coding IDE).

- **The Prompt:** "Now, write a query to find the top 3 customers by spend."
    
- **The Execution:** When the user hits "Run," the code is sent to your **Code Sandbox**.
    
- **The Feedback Loop:** * **If correct:** The Sandbox returns the result; the AI congratulates the user and unlocks the next lesson.
    
    - **If incorrect:** The error message is sent back to the AI. The AI _explains_ why it failed (without giving the answer) and asks the user to try again.
        

#### C. Adaptive Branching (The "Logic" Phase)

If a user fails a task 3 times, the **Agent Orchestrator** triggers a "Pivot."

- **Pivot Logic:** "User is struggling with Joins. Generate a 'Bridge Lesson' that explains Joins using a simpler analogy, then re-test."
    

---

### 4. Visualizing the Process

### Next Step for You

To get a "Minimum Viable Product" (MVP) running, you don't need a fancy UI. You can build the core logic in a Python script first.

**Would you like me to provide a Python snippet using LangChain that generates a syllabus and then "locks" the second lesson until a mock task is completed?**