from core.RECORD import RECORDManager
from core.RECORD import show_record_template
from core.ACTION import ACTION
from core.ACTION import show_action_template
from core.ACTION import get_related_file_string
from core.ACTION import BasicFile


if __name__ == '__main__':
    APM_R = RECORDManager()
    # show_record_template()
    # submit = {
    #     "start_time": "2023-11-21-16-19-2",
    #     "end_time": "2023-11-21-17-40-2",
    #     "start_passion_score": 4,
    #     "end_feeling_score": 4,
    #     "attention_score": 3,
    #     "passion_description": "中途因为要拷数据，去了机房两次，感觉下午还没有开始好好工作多久",
    #     "feeling_description": "工作进度还是有的",
    #     "attention_description": "中途和其他人简单交谈了一下，没有看手机，但是精神力有一点下降",
    #     "work_env_description": "接近晚上的实验室",
    # }
    # APM_R.add_record(submit)
    APM_R.check(year=2023, month=11, day=21)

    # APM_A = ACTION()
    # # show_action_template()
    # file_1 = BasicFile(
    #     file_type='file_full_path',
    #     context=r'C:\u'
    # )
    # action = {
    #     "goal": "写好ACTION模块",
    #     "methods": "仿照RECORD的写法",
    #     "feedback": "感觉设计得不是很优雅",
    #     "related_files": get_related_file_string([file_1]),
    # }
    # APM_A.add_action(action)
    # APM_A.delete()
    # # APM_A.check_action(check_id='1')
    # APM_A.add_record("1", "0")
    # APM_A.add_record("1", "1")
    # APM_A.add_record("1", "2")
    # APM_A.check_related_record("1")

