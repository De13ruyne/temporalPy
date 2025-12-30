import asyncio
import uuid
from temporalio.client import Client
from common import InputJson
from common import TEMPORAL_HOST

async def start_job(input: InputJson):
    client = await Client.connect(TEMPORAL_HOST)

    # 生成唯一的工作流 ID
    id = f"say-hello-workflow-{uuid.uuid4()}"

    # 启动工作流
    res = await client.execute_workflow(
        "SayHelloWorkflow",
        input,
        id=id,
        task_queue="my-task-queue",
    )
    # 返回建立的 job 结果
    return {
        "job_id": id,
        "result": res,
    }