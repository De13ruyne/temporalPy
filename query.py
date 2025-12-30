from temporalio.client import Client
from common import OutputJson

# 通过传入 job_id 查询工作流状态
# 返回 OutputJson 数据结构
async def query_job(job_id: str):
    # 获取客户端
    client = await Client.connect("localhost:7233")
    
    # 获取句柄
    handle = client.get_workflow_handle(job_id)
    
    # 调用 describe()
    description = await handle.describe()

    # 访问基本状态
    print(f"Workflow 状态: {description.status}")
    print(f"Workflow 类型: {description.workflow_type}")
    print(f"开始时间: {description.start_time}")
    print(f"结束时间: {description.close_time}")

    # 返回查询结果封装
    return OutputJson(
        job_id=job_id,
        status=description.status,
        start_time=str(description.start_time),
        end_time=str(description.close_time),
        # attempt=description.raw_description.pending_activities.attempts if description.raw_description.pending_activities else 0,
        attempt=1,
    )

