from datetime import timedelta
from temporalio import workflow
from activities import greet
from common import ActParams
from common import InputJson
from temporalio.common import RetryPolicy

# 工作流定义
@workflow.defn(name="SayHelloWorkflow")
class SayHelloWorkflow:
    @workflow.run
    async def run(self, input: InputJson) -> str:
        # attempt = workflow.info().attempt
        print(f"Workflow attempt: {workflow.info().attempt}")

        # 执行活动
        return await workflow.execute_activity(
            greet,
            ActParams(input.msg, input.fail_first_attempt),
            schedule_to_close_timeout=timedelta(seconds=10),
            # 设置重试策略
            retry_policy=RetryPolicy(
                backoff_coefficient=2.0,
                maximum_attempts=3,         # 最大尝试次数
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(seconds=2),
                # non_retryable_error_types=["ValueError"],
            )
        )