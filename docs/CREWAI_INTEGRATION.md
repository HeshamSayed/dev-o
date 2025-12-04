# CrewAI Multi-Agent System Integration

## Overview

DEV-O now includes a Sequential Multi-Agent System powered by CrewAI v1.6.1 that acts as a complete AI Development Team. This system generates fully production-ready applications through a coordinated pipeline of specialized agents.

## Architecture

### Agent Pipeline (Sequential Flow)

```
Product Owner → Backend Developer → Frontend Developer → QA Engineer
```

Each agent completes its tasks before passing control to the next agent in the pipeline.

## Four Specialized Agents

### 1. 🎯 Product Owner Agent

**Role**: Analyzes user requirements and creates detailed specifications

**Responsibilities**:
- Parse user's project idea/description
- Generate user stories with acceptance criteria
- Create technical specifications document
- Define project structure and architecture

**Outputs**:
- `specs/requirements.md` - Detailed functional and non-functional requirements
- `specs/user_stories.md` - User stories with acceptance criteria
- `specs/architecture.md` - System architecture, tech stack, and project structure

### 2. ⚙️ Backend Developer Agent

**Role**: Implements server-side logic based on Product Owner's specifications

**Responsibilities**:
- Create database models/schemas
- Build REST API endpoints
- Implement business logic and services
- Add authentication/authorization if needed
- Create configuration files

**Outputs**:
- Complete backend code (Python/Django or Node.js based on project type)
- Database models
- API endpoints
- Configuration files (requirements.txt, package.json)

### 3. 🎨 Frontend Developer Agent

**Role**: Builds the user interface based on specs and integrates with backend

**Responsibilities**:
- Create React components with TypeScript
- Build pages and routing
- Implement state management
- Style with CSS/Tailwind
- Connect to backend APIs

**Outputs**:
- Complete frontend code (React + TypeScript + Vite)
- UI components
- API integration layer
- Configuration files (package.json, vite.config.ts, tsconfig.json)

### 4. 🧪 QA Engineer Agent

**Role**: Ensures code quality and creates comprehensive tests

**Responsibilities**:
- Write unit tests for backend
- Write component tests for frontend
- Create integration tests
- Validate code against specs
- Generate test coverage report
- Create final README.md with setup instructions

**Outputs**:
- Test files for backend and frontend
- README.md with complete setup instructions
- Docker configuration (optional)
- Documentation

## Usage

### WebSocket Message Format

To trigger the CrewAI pipeline, send a WebSocket message with type `crew_message`:

```json
{
  "type": "crew_message",
  "message": "Build a task management app with user authentication"
}
```

### Event Types

The system streams various event types during execution:

#### 1. Crew Initialization
```json
{
  "type": "crew_init",
  "agents": [
    {"name": "Product Owner", "status": "initialized"},
    {"name": "Backend Developer", "status": "initialized"},
    {"name": "Frontend Developer", "status": "initialized"},
    {"name": "QA Engineer", "status": "initialized"}
  ]
}
```

#### 2. Agent Started
```json
{
  "type": "agent_started",
  "agent": "Product Owner"
}
```

#### 3. Agent Completed
```json
{
  "type": "agent_completed",
  "agent": "Product Owner",
  "files_created": 3
}
```

#### 4. File Tree Update
```json
{
  "type": "file_tree_update",
  "tree": {
    "specs": {
      "type": "directory",
      "children": {
        "requirements.md": {"type": "file", "id": "uuid"},
        "user_stories.md": {"type": "file", "id": "uuid"},
        "architecture.md": {"type": "file", "id": "uuid"}
      }
    }
  }
}
```

#### 5. Crew Completed
```json
{
  "type": "crew_completed",
  "total_files": 25,
  "message": "Development crew completed successfully!"
}
```

#### 6. Error
```json
{
  "type": "error",
  "error": "Error message here"
}
```

## Configuration

### Environment Variables

Add to your `.env` file:

```bash
# CrewAI Configuration
CREWAI_VERBOSE=true          # Enable verbose logging
CREWAI_MAX_ITERATIONS=10     # Maximum iterations per agent
CREWAI_MEMORY=true           # Enable agent memory
```

### Django Settings

The following settings are automatically configured in `config/settings.py`:

```python
CREWAI_VERBOSE = os.getenv('CREWAI_VERBOSE', 'True') == 'True'
CREWAI_MAX_ITERATIONS = int(os.getenv('CREWAI_MAX_ITERATIONS', '10'))
CREWAI_MEMORY = os.getenv('CREWAI_MEMORY', 'True') == 'True'
```

## Session Management & Context Persistence

The CrewAI system maintains session context across multiple executions for each project, enabling agents to remember previous interactions and build upon earlier work.

### How Session Memory Works

1. **Per-Project Sessions**: Each project has its own session context that persists across multiple crew executions
2. **Conversation History**: All user messages and agent responses are stored in the session
3. **Execution Tracking**: The system tracks how many times the crew has been executed for a project
4. **CrewAI Memory**: Built-in CrewAI memory is enabled (`memory=True`) for all crews, allowing agents to:
   - Remember decisions made in previous tasks
   - Access context from earlier agent executions
   - Build upon existing files and specifications
   - Maintain consistency across multiple iterations

### Session Context Structure

```python
{
    'project_id': 'uuid',
    'execution_count': 3,  # Number of times crew has been run
    'last_execution': 'Add authentication to the app',
    'conversation_history': [
        {
            'role': 'user',
            'content': 'Build a task management app',
            'timestamp': '...'
        },
        {
            'role': 'assistant',
            'content': 'Created 25 files across all agents.',
            'files': ['specs/requirements.md', 'backend/models.py', ...]
        }
    ]
}
```

### Benefits of Session Memory

- **Incremental Development**: Users can add features iteratively without losing context
- **Consistent Architecture**: Agents maintain architectural decisions across updates
- **Efficient Updates**: Agents can modify existing files without recreating everything
- **Context-Aware**: Each agent has access to the full project history

### Example: Multi-Request Workflow

```
Request 1: "Build a task management app"
→ Creates complete app with specs, backend, frontend, tests

Request 2: "Add user authentication with JWT"
→ Updates existing files, adds auth endpoints, modifies frontend
→ Remembers existing architecture and file structure

Request 3: "Add email notifications when tasks are assigned"
→ Extends backend services, updates models, adds frontend UI
→ Maintains consistency with previous auth implementation
```

## Technical Implementation

### File Structure

```
backend/
├── services/
│   ├── crew_service.py              # Main orchestration service
│   └── agents/
│       ├── __init__.py
│       ├── product_owner.py         # Product Owner agent
│       ├── backend_dev.py           # Backend Developer agent
│       ├── frontend_dev.py          # Frontend Developer agent
│       ├── qa_engineer.py           # QA Engineer agent
│       └── tools/
│           ├── __init__.py
│           └── file_tools.py        # File operation tools
```

### Custom Tools

The system provides custom tools for agents to interact with files:

1. **FileWriteTool**: Write content to files
2. **FileReadTool**: Read content from files
3. **FileListTool**: List all files in the project

These tools use shared in-memory storage during agent execution, then persist to the database after each agent completes.

### Integration with Existing System

The CrewAI system integrates seamlessly with the existing DEV-O infrastructure:

- **ProjectFile Model**: All generated files are saved to the existing `ProjectFile` model
- **WebSocket Consumer**: New `crew_message` handler in `ProjectConsumer`
- **AI Service**: Uses existing AI service configuration for LLM calls
- **Usage Tracking**: Integrates with existing usage limits and billing system

### Backwards Compatibility

The implementation maintains full backwards compatibility with the existing single-agent functionality:

- Original `project_message` handler still works
- Single agents can still be used independently
- No breaking changes to existing APIs

## Example Usage Flow

1. **User creates a project** with description: "Build a task management app with user authentication"

2. **Frontend sends WebSocket message**:
   ```json
   {
     "type": "crew_message",
     "message": "Build a task management app with user authentication"
   }
   ```

3. **System executes pipeline**:
   - **Product Owner** (1-2 minutes):
     - Analyzes requirements
     - Creates `specs/requirements.md`, `specs/user_stories.md`, `specs/architecture.md`
     - Streams progress to frontend
   
   - **Backend Developer** (3-5 minutes):
     - Reads specs
     - Creates Django models, views, serializers, URLs
     - Creates `backend/requirements.txt`
     - Streams file creation events
   
   - **Frontend Developer** (3-5 minutes):
     - Reads specs and backend API
     - Creates React components, pages, API client
     - Creates `frontend/package.json`, `vite.config.ts`
     - Streams file creation events
   
   - **QA Engineer** (2-3 minutes):
     - Reviews all code
     - Creates tests for backend and frontend
     - Creates `README.md` with setup instructions
     - Streams completion events

4. **User receives complete project**:
   - All files available in the file tree
   - README with instructions to run the application
   - Tests ready to execute
   - Production-ready code

## Output Structure

The generated project follows this structure:

```
generated_project/
├── README.md                 # Setup and run instructions
├── specs/
│   ├── requirements.md
│   ├── user_stories.md
│   └── architecture.md
├── backend/
│   ├── requirements.txt
│   ├── manage.py
│   ├── app/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── serializers.py
│   │   └── services/
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api/
│   │   └── App.tsx
│   └── tests/
├── docker-compose.yml (optional)
└── Makefile (optional)
```

## Dependencies

### Required Packages

- `crewai==1.6.1` - CrewAI framework (no LangChain dependency)
- `python-dotenv>=1.1.1` - Environment variable management
- `httpx>=0.27.0` - HTTP client for API calls
- `uvicorn>=0.31.1` - ASGI server

All dependencies are automatically installed via `requirements.txt`.

### No LangChain Required

CrewAI v1.6.1 uses its native LLM integration and does not require LangChain as a dependency. The system integrates directly with the existing AI service.

## Performance Considerations

- **Sequential Execution**: Agents run one at a time, ensuring quality and consistency
- **Streaming Updates**: Real-time progress updates keep users informed
- **Memory Efficient**: Shared file storage prevents duplication
- **Usage Tracking**: Proper billing and quota management

## Error Handling

The system includes comprehensive error handling:

- **Agent Failures**: Errors are logged and reported to the user
- **Timeout Protection**: Max iterations prevent infinite loops
- **WebSocket Errors**: Connection issues are handled gracefully
- **Database Errors**: File save failures are caught and reported

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Django Not Configured**: Make sure DJANGO_SETTINGS_MODULE is set
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings
   ```

3. **WebSocket Connection Fails**: Check Redis is running
   ```bash
   docker-compose up redis
   ```

4. **Agent Timeout**: Increase CREWAI_MAX_ITERATIONS if needed

### Logging

Enable verbose logging for debugging:

```bash
CREWAI_VERBOSE=true
```

Logs are available in the console with prefixes:
- `[CREW]` - Main orchestration events
- `[FILE_TOOL]` - File operation events

## Future Enhancements

Potential improvements for future versions:

1. **Parallel Execution**: Run compatible tasks in parallel
2. **Agent Communication**: Enable agents to collaborate during execution
3. **Custom Agent Types**: Allow users to define custom agents
4. **Incremental Updates**: Support modifying existing projects
5. **Test Execution**: Automatically run generated tests
6. **Deployment**: Integrate with deployment platforms

## License

This integration is part of DEV-O and follows the same license terms.
