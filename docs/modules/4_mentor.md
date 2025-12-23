In your modular architecture, the **Mentor** is the **Brain** and the **Primary Orchestrator**. If this were a movie production, the Architect is the Screenwriter, the Builder is the Set Designer, but the **Mentor is the Director**.

Following **SOLID principles**, the Mentor’s single responsibility is **Process Orchestration and State Management**. It is the only module that understands the "Status" of the user's journey.

---

### 1. The Role of the Mentor

The Mentor acts as the connective tissue between the user, the AI workers (Architect/Builder), and the data storage (Infrastructure).

- **State Machine Management:** It tracks where the user is (e.g., `STARTING_COURSE`, `READING_LESSON`, `WAITING_FOR_QUIZ_RESULTS`).
    
- **Context Management:** It ensures that when the Builder generates Lesson 2, the Mentor provides the summary of what happened in Lesson 1.
    
- **Gatekeeping:** It prevents the user from moving forward until the "Mastery Criteria" (the quiz) are met.
    
- **Communication:** It transforms technical data into a conversational interface for the user.
    

---

### 2. Main Files in the Module

The `mentor/` package manages the complexity of the "Learning Loop":

- **`coordinator.py`**: The "Heart" of the app. It contains the logic: _If Quiz = Passed, then call Builder for next lesson; else, ask Builder for a hint._
    
- **`flow_manager.py`**: Handles the transitions between different learning states (e.g., moving from the Architect's "Planning Phase" to the Builder's "Execution Phase").
    
- **`prompts.py`**: Contains the "Mentor Personality" prompts—how the AI should greet the user, encourage them, or explain why they failed a quiz.
    
- **`schemas.py`**: Defines the session state (e.g., `active_course_id`, `current_module_index`).
    

---

### 3. The Mentor’s Operational Flow

The Mentor follows a strict **Request-Response-Persist** pattern. It never does the "heavy lifting" (generating content) itself; it delegates and then records.

1. **Event:** User clicks "I'm ready for the next topic."
    
2. **Check:** Mentor queries **Infrastructure** to see which lesson is next in the `CourseScenario`.
    
3. **Action:** Mentor calls **Builder** with the specific requirements for that lesson.
    
4. **Persistence:** Mentor receives the content and saves it via **Infrastructure**.
    
5. **Interaction:** Mentor sends the content to the UI for the user to read.
    

---

### 4. Logic Example: The "Quiz Gatekeeper"

This is the most important logic the Mentor handles. It ensures the user doesn't just scroll through the course.

Python

```
# src/mentor_app/mentor/coordinator.py

class MentorCoordinator:
    def handle_quiz_submission(self, user_id: str, answers: Dict):
        # 1. Logic to check answers
        is_passed = self._evaluate_results(answers)
        
        if is_passed:
            # Update Auditor for stats
            self.auditor.log_success(user_id)
            # Unlock next lesson in DB via Infrastructure
            self.repo.mark_lesson_completed(user_id)
            return "Great job! You've mastered this. Ready for the next lesson?"
        else:
            # Don't unlock. Ask Builder to generate a 'Hint' or 'Explanation'
            explanation = self.builder.get_remediation(answers)
            return f"Not quite. Here is what you missed: {explanation}"
```

---

### 5. Why the Mentor is the "Fat" Module

In modular design, you often hear "Keep your controllers thin." However, in AI agents, the **Orchestrator (Mentor)** is naturally "fatter" because:

- **It handles the "If/Then" of the AI:** AI is unpredictable. The Mentor provides the guardrails.
    
- **It manages the Database:** Since the Architect and Builder are stateless, the Mentor is the only one authorized to tell the Infrastructure to "Save" or "Update."
    

### Summary of Responsibilities

|**Feature**|**Mentor's Job**|
|---|---|
|**Syllabus?**|No, asks **Architect**.|
|**Lesson Text?**|No, asks **Builder**.|
|**User Stats?**|No, asks **Auditor**.|
|**Database?**|No, asks **Infrastructure**.|
|**Decision Making?**|**YES.** Decides when to call which module.|

**Now that we've covered the Brain (Mentor), would you like to see how the "Auditor" module looks, which tracks the user's progress and builds those "Mastery Dashboards"?**