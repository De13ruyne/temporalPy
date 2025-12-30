# Temporal Workflow Example
This project demonstrates a **Python-based simple Temporal workflow** for job processing, combined with a FastAPI interface to implement RESTful-style job submission and status query capabilities.

## 1. Prerequisites
### 1.1 Environment Requirements
- Python 3.9
- Temporal Server 
- FastAPI & Uvicorn 
- Temporal Python SDK 

### 1.2 Dependencies Installation
Execute the following command to install all required Python packages:
```bash
pip install temporalio fastapi uvicorn 
```

## 2. Start Temporal Server 
### 2.1 Start Command
```bash
# Start Temporal standalone server 
temporal server start-dev
```

### 2.2 Verify Server Startup
The Temporal Web UI will be automatically started at `http://localhost:8233` (default port), which can be used to:
- View all workflow instances and their running status
- Check activity execution logs and retry records
- Manually terminate/resume workflow tasks

## 3. Start Core Services (Worker + API Server)

### 3.1 Start Temporal Worker
The Worker is responsible for registering Workflow/Activity, listening to the Temporal task queue, and executing distributed tasks:
```bash
# Run worker (bind to the default task queue of the project)
python3 ./worker.py
```

### 3.2 Start FastAPI API Server
The API server provides external HTTP access capabilities for job submission and status query:
```bash
# Start API service
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```


## 4. API Usage & Function Verification


### 4.1 Create a New Job 
Submit a new task to the Temporal workflow via the POST interface, and return the unique job ID and execution result immediately.
- **Request Method**: POST
- **Request Endpoint**: `http://localhost:8000/jobs`

- **Request Body**:
```json
{
    "msg": "Temporal",
    "fail_first_attempt": false
}
```
- **Successful Response** (200 OK):
```json
{
    "job_id": "say-hello-workflow-b501c059-07c2-4d0e-b102-8efabe06f6f2",
    "result": {
        "attempt": 1,
        "msg": "Hello Temporal"
    }
}
```

### 4.2 Query Job Status & Details
Query the full lifecycle information of the specified job via the job ID returned by the creation interface.
- **Request Method**: GET
- **Request Endpoint**: `http://localhost:8000/jobs/{job_id}`
- **Successful Response** (200 OK):
```json
{
    "job_id": "say-hello-workflow-b501c059-07c2-4d0e-b102-8efabe06f6f2",
    "status": 2,
    "start_time": "2025-12-30 10:44:04.867680+00:00",
    "end_time": "2025-12-30 10:44:04.897119+00:00",
    "attempt": 1
}
```
### 4.3 Core Status Code Definition (Unified Explanation)
Add a clear state mapping table for easy status judgment:
| Status Code | Meaning | Corresponding Workflow State |
|-------------|---------|------------------------------|
| 1 | RUNNING | Workflow/Activity is being executed |
| 2 | COMPLETED | Workflow executed successfully |
| 3 | FAILED | Workflow execution failed |

## 5. Key Design Decisions 
### 5.1 Workflow Layer Design (`workflows.py`)
The core of the Temporal task orchestration, responsible for defining the **task execution process and fault-tolerant rules**:
- Configure a complete retry strategy: set the **maximum retry times to 3** for failed activities
- Custom retry rules: specify retry intervals, exclude non-retryable exceptions
- Bind to the specified task queue: ensure that the Worker can correctly listen and execute

### 5.2 Activity Layer Design (`activities.py`)
The **specific business logic execution unit** (stateless, idempotent), core capabilities:
- Implement a controllable failure/retry business logic: when `fail_first_attempt=True`, the first execution fails and the subsequent retries succeed
- Return the execution result and the number of attempts
- Comply with Temporal Activity specifications: stateless design, support repeated execution

### 5.3 Worker Layer Design (`worker.py`)
The **bridge between Temporal Server and business code**, core responsibilities:
- Register all Workflows and Activities to the specified task queue
- Establish a long connection with the Temporal Server, listen to the task queue in real time
- Receive task distribution from the Server and execute the corresponding Workflow/Activity
- Report the execution result and status to the Temporal Server in real time

## 6. Project Structure & File Description

```bash
.
├── README.md          # Project documentation (usage, design, structure)
├── activities.py      # Business logic implementation (Activity definition)
├── common.py          # Public configuration (task queue name, constant, tool function)
├── main.py            # FastAPI API service (interface definition, request processing)
├── query.py           # Workflow status query tool (public query logic encapsulation)
├── starter.py         # Workflow startup client (task submission core logic)
├── worker.py          # Temporal Worker (register Workflow/Activity, listen task queue)
└── workflows.py       # Workflow definition (orchestration logic, retry strategy)
```

## 7. AI Usage Disclosure
- Learn the core concepts and usage specifications of the Temporal Python SDK
- Obtain optimization suggestions for Temporal workflow/activity design patterns
- Get guidance on FastAPI interface design and parameter verification best practices
- Optimize the project structure and code writing specifications
- Supplement the project documentation and troubleshoot common problems

