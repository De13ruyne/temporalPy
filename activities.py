from temporalio import activity
from common import ActParams
from common import Result

@activity.defn
async def greet(ap: ActParams) -> Result:
    print(f"greet activity attempt: {activity.info().attempt}")

    # 模拟第一次失败
    if (ap.fail_first_attempt and activity.info().attempt == 1):
        print(f"greet activity failing first attempt for: {ap.msg}")
        raise Exception("Intentional failure on first attempt")
    
    # 返回结果
    return Result(msg=f"Hello {ap.msg}", attempt=activity.info().attempt)