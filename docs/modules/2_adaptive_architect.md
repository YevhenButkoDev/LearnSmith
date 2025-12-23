To implement an **Adaptive Architect**, you need to evolve the module from a simple "Syllabus Generator" into a **Knowledge-Gap Analyzer**.

In SOLID terms, the Architect's single responsibility remains: **Curriculum Mapping**. However, the input to this mapping process is now a "Knowledge Profile" rather than just a skill name.

### 1. The Adaptive Input: `KnowledgeProfile`

Instead of a simple string, the Architect now accepts a structured profile.

Python

```
# src/mentor_app/architect/models.py
from pydantic import BaseModel
from typing import List, Dict

class KnowledgePoint(BaseModel):
    topic: str
    confidence: int  # 1 (No idea) to 5 (Expert)

class KnowledgeProfile(BaseModel):
    target_skill: str
    user_level: str  # e.g., "Intermediate"
    known_topics: List[KnowledgePoint]
```

---

### 2. The Architect's Decision Logic

When generating the scenario, the Architect must follow a **"Pruning & Bridging"** logic:

1. **Pruning:** If a topic has a confidence of **4 or 5**, the Architect should omit the "Reading" part of that lesson and instead generate a "Quick Review" or skip it entirely.
    
2. **Reinforcing:** If a topic has a confidence of **1 or 2**, the Architect marks this module as a "High-Priority Focus," signaling the **Builder** to generate deeper explanations.
    
3. **Advanced Bridging:** If a beginner has a high confidence in a specific advanced sub-topic, the Architect identifies the "Missing Link" modules needed to support that advanced knowledge.
    

---

### 3. Updated Database Schema for Personalization

To store this, we need to track not just what the course _is_, but why it was built this way for _this_ user.

**New Table: `User_Knowledge_State`**

- `user_id` (FK)
    
- `topic_name` (String)
    
- `confidence_score` (Int)
    
- `last_assessed` (DateTime)
    

**Updated Table: `Module_Metadata`**

- `module_id` (FK)
    
- `is_skipped` (Boolean) — _If the user already knows this._
    
- `is_remediation` (Boolean) — _If this was added because the user failed a previous check._
    

---

### 4. Logic Implementation in `architect/service.py`

The "Brain" of the Architect now uses the list of known topics to "shape" the prompt.

Python

```
# src/mentor_app/architect/service.py

class ArchitectService:
    def create_custom_scenario(self, profile: KnowledgeProfile):
        # 1. Convert knowledge profile into a prompt instruction
        knowledge_context = "\n".join([
            f"- {p.topic}: Level {p.confidence}/5" 
            for p in profile.known_topics
        ])
        
        system_prompt = f"""
        Act as a Technical Curriculum Designer. 
        Target: {profile.target_skill}.
        User Background: {profile.user_level}.
        Current Knowledge: {knowledge_context}
        
        Rules:
        1. If confidence is 4-5, SKIP the lesson but include a 1-question 'Mastery Check'.
        2. If confidence is 1-2, add 'Deep Dive' indicators.
        3. Do not teach topics the user clearly knows.
        """
        
        # 2. Call LLM (o1 or GPT-4o)
        # 3. Parse into CourseScenario object
        pass
```

---

### 5. Why this is still "Modular"

- **The Architect** still only cares about the **Syllabus**. It doesn't know how to talk to a user.
    
- **The Mentor** module is what collects the "Confidence 1-5" data (perhaps through a UI survey) and passes it to the Architect.
    
- **The Infrastructure** module is what saves the `KnowledgePoint` into the database.
    

### Summary of Workflow

1. **Mentor** asks User: "Rate your SQL skills from 1-5."
    
2. **Mentor** bundles this into a `KnowledgeProfile`.
    
3. **Architect** receives the profile, calls the LLM with the "Pruning" instructions.
    
4. **Architect** returns a JSON scenario where Lesson 1 (Basic Selects) is marked `status="skipped"` because the user's confidence was 5.
    

**Would you like me to show you how the "Mentor" module would coordinate the first "Knowledge Assessment" survey before calling the Architect?**