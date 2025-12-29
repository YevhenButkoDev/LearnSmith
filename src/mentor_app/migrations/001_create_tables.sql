-- Create courses table
CREATE TABLE courses (
    id VARCHAR(255) PRIMARY KEY,
    course_title VARCHAR(255) NOT NULL,
    estimated_duration INTEGER NOT NULL,
    difficulty_level VARCHAR(50) NOT NULL,
    prerequisites JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create modules table
CREATE TABLE modules (
    id VARCHAR(255) NOT NULL,
    course_id VARCHAR(255) NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    learning_objectives JSONB NOT NULL,
    estimated_duration INTEGER NOT NULL,
    dependencies JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, course_id)
);

-- Create lessons table (created when module content is generated)
CREATE TABLE lessons (
    id VARCHAR(255) NOT NULL,
    module_id VARCHAR(255) NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    key_concepts JSONB NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    content_markdown TEXT,
    estimated_duration INTEGER,
    code_examples JSONB,
    interactive_elements JSONB,
    practice_tasks JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id, course_id) REFERENCES modules(id, course_id) ON DELETE CASCADE,
    PRIMARY KEY (id, course_id, module_id)
);

-- Create indexes for better performance
CREATE INDEX idx_modules_course_id ON modules(course_id);
CREATE INDEX idx_lessons_module_id ON lessons(module_id);
CREATE INDEX idx_courses_difficulty ON courses(difficulty_level);
CREATE INDEX idx_lessons_type ON lessons(type);
