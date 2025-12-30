import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflows import SayHelloWorkflow
from activities import greet
from common import TEMPORAL_HOST

# 启动 Worker 来处理工作流和活动
async def main():
    client = await Client.connect(TEMPORAL_HOST)

    # 创建并启动 Worker
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[SayHelloWorkflow],
        activities=[greet],
    )
    print("Worker started.")
    # 运行 Worker
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())