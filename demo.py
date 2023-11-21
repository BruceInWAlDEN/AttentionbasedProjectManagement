from core.RECORD import RECORDManager
from core.RECORD import show_submit_template

if __name__ == '__main__':
    APM = RECORDManager()
    # show_submit_template()
    submit = {
        "start_time": "2023-11-21-14-37-49",
        "end_time": "2023-11-21-15-13-0",
        "start_passion_score": 4,
        "end_feeling_score": 4,
        "attention_score": 4,
        "passion_description": "上午没有工作，在宿舍浪费时间，因此现在很有工作的冲动",
        "feeling_description": "思维活跃，正反馈，老师安排的事情在等待程序结果，暂时不用管，因此很安心",
        "attention_description": "没有什么干扰的事物，中间只有一次，看了一下手机马上放下了",
        "work_env_description": "下午的实验室，没有什么人",
    }
    # APM.add_submit(submit)
    APM.check(year=2023, month=11, day=21)
