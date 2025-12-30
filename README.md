# Temporal Workflow Example
This project demonstrates a **Python-based simple Temporal workflow** for job processing, combined with a FastAPI interface to implement RESTful-style job submission and status query capabilities.

## 1. Environment Requirements
- Python 3.9
- Temporal Server 
- FastAPI & Uvicorn 
- Temporal Python SDK 
- Docker

## 2. QuickStart

### 2.1 Clone the repository

```
git clone git@github.com:De13ruyne/temporalPy.git
cd temporalPy
```

### 2.2 Build and start all services using Docker Compose
Start the services then you can test the api
```
docker-compose up -d --build
```
`Note: --build rebuilds the images, -d runs containers in the background.`

### 2.3 Check the status of services:
```
docker-compose ps
```

### 2.4 Stop and remove containers:
```
docker-compose down
```

## 3. API Usage & Function Verification


### 3.1 Create a New Job 
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

### 3.2 Query Job Status & Details
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
### 3.3 Core Status Code Definition (Unified Explanation)
Add a clear state mapping table for easy status judgment:
| Status Code | Meaning | Corresponding Workflow State |
|-------------|---------|------------------------------|
| 1 | RUNNING | Workflow/Activity is being executed |
| 2 | COMPLETED | Workflow executed successfully |
| 3 | FAILED | Workflow execution failed |

## 4. Key Design Decisions 
### 4.1 Workflow Layer Design (`workflows.py`)
The core of the Temporal task orchestration, responsible for defining the **task execution process and fault-tolerant rules**:
- Configure a complete retry strategy: set the **maximum retry times to 3** for failed activities
- Custom retry rules: specify retry intervals, exclude non-retryable exceptions
- Bind to the specified task queue: ensure that the Worker can correctly listen and execute

### 4.2 Activity Layer Design (`activities.py`)
The **specific business logic execution unit** (stateless, idempotent), core capabilities:
- Implement a controllable failure/retry business logic: when `fail_first_attempt=True`, the first execution fails and the subsequent retries succeed
- Return the execution result and the number of attempts
- Comply with Temporal Activity specifications: stateless design, support repeated execution

### 4.3 Worker Layer Design (`worker.py`)
The **bridge between Temporal Server and business code**, core responsibilities:
- Register all Workflows and Activities to the specified task queue
- Establish a long connection with the Temporal Server, listen to the task queue in real time
- Receive task distribution from the Server and execute the corresponding Workflow/Activity
- Report the execution result and status to the Temporal Server in real time

## 5. Project Structure & File Description

```bash

.
├── README.md          # Project documentation
├── Dockerfile         # Docker image configuration
├── docker-compose.yml # Docker Compose for service orchestration
├── requirements.txt   # Python dependencies
├── worker.py          # Temporal Worker
├── workflows.py       # Workflow orchestration and retry logic
├── activities.py      # Business logic implementation
├── main.py            # FastAPI API server
├── starter.py         # Workflow client for job submission
├── query.py           # Workflow status query helper
└── common.py          # Shared constants and utility functions


```

## 6. AI Usage Disclosure
- Learn the core concepts and usage specifications of the Temporal Python SDK
- Obtain optimization suggestions for Temporal workflow/activity design patterns
- Get guidance on FastAPI interface design and parameter verification best practices
- Optimize the project structure and code writing specifications
- Supplement the project documentation and troubleshoot common problems

