# -*- coding: utf-8 -*-
import os
import json
import time


WORK_DIR = r'C:\Users\Bruce\Desktop\AttentionbasedProjectManagement\DATA'

"""
to recover file in case of wrong operation
save all RECORD submit without over write and give ID for every RECORD
"""
RECORD_FILE_NAME = 'RECORD_*.json'  # RECORD_{ID}.json
"""
meta infomation:
{
"last_open_file_id": 0,
"submit_record": {'time': id: str},
"max_file_id": 1,
"delete_record_id": [0, 1]   # this file will be skipped when check 
...
}
"""
RECORD_FILE_META = 'RECORD_META.json'


def read_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        j = json.load(f)

    return j


def save_json(dict_dataset: dict, name: str):
    """原文件将被覆盖"""
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_dataset, ensure_ascii=False, indent=4))


def _get_record_dict_by_id(record_id: str):
    info_dict = read_json(os.path.join(WORK_DIR, RECORD_FILE_NAME.replace('*', record_id)))

    return info_dict


def _format_check(info_dict: dict):
    """
    check RECORD format: 工作开始时间，结束时间，开始工作时的意愿程度&原因分析，注意力集中的程度&原因分析，结束后的正反馈程度&原因分析, 工作环境描述
    """
    keys = [
        'start_time',   # format time
        'end_time',
        'start_passion_score',    # 1-5
        'end_feeling_score',    # string
        'attention_score',
        'passion_description',
        'feeling_description',
        'attention_description',
        'work_env_description'  # string
    ]
    flag = True
    for key in keys:
        if key in info_dict.keys():
            if 'score' in key and 'reason' not in key:
                if info_dict[key] in [1, 2, 3, 4, 5]:
                    pass
                else:
                    print('error info format: wrong socre: ', info_dict[key])
                    flag = False
            if 'reason' in key or 'env' in key:
                if isinstance(info_dict[key], str):
                    pass
                else:
                    print('error info format: wrong reason')
                    flag = False
            if 'time' in key:
                if isinstance(key, str):
                    year, month, day, hour, minute, sec = [int(_) for _ in info_dict[key].split('-')]
                    if time.strptime('{}-{}-{}'.format(year, month, day), '%Y-%m-%d') and 0 <= hour <= 24 and 0 <= minute <= 60 and 0 <= sec <= 60:
                        pass
                    else:
                        print('error info format: wrong time')
                        flag = False
                else:
                    print('error info format: wrong time')
                    flag = False
        else:
            print('error info format: key missing: ', key)
            flag = False

    return flag


def _check_time_string(time_string):
    if not time.strptime(time_string, '%Y-%m-%d-%H-%M-%S'):
        print('time is not reasonable')
        return False
    else:
        return True


def _get_time_string_now():
    time_p = time.localtime()
    time_string = '{}-{}-{}-{}-{}-{}'.format(
        time_p.tm_year, time_p.tm_mon, time_p.tm_mday, time_p.tm_hour, time_p.tm_min, time_p.tm_sec)

    return time_string


def show_record_template():
    print('{')
    for k, v in BasicRECORD().__dict__.items():
        if k != 'id':
            v = "\"" + v + "\"" if  isinstance(v, str) else str(v)
            print("\t" + "\"" + k + "\"" + ": " + v + ",")
    print('}')


class BasicTime(object):
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0

    def get_time_string(self):
        return '{}-{}-{}-{}-{}-{}'.format(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            self.second
        )

    def set_by_string(self, time_string):
        if _check_time_string(time_string):
            year, month, day, hour, minute, second = [int(_) for _ in time_string.split('-')]
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour
            self.minute = minute
            self.second = second
        else:
            raise AssertionError


class BasicRECORD(object):
    def __init__(self):
        # auto hyper by manager
        self.id = '0'

        # content
        self.start_time = _get_time_string_now()
        self.end_time = _get_time_string_now()
        self.start_passion_score = 5    # 1-5 do you want ?
        self.end_feeling_score = 5    # 1-5 are you ok ?
        self.attention_score = 5    # 1-5 is there a heart flow ?
        self.passion_description = 'init'
        self.feeling_description = 'init'
        self.attention_description = 'init'
        self.work_env_description = 'init'

    def set_record(self, info_dict: dict):
        try:
            self.id = info_dict['id']
            self.start_time = info_dict['start_time']
            self.end_time = info_dict['end_time']
            self.start_passion_score = info_dict['start_passion_score']
            self.end_feeling_score = info_dict['end_feeling_score']
            self.attention_score = info_dict['attention_score']
            self.passion_description = info_dict['passion_description']
            self.feeling_description = info_dict['feeling_description']
            self.attention_description = info_dict['attention_description']
            self.work_env_description = info_dict['work_env_description']

            return True

        except KeyError:
            print('KeyError: wrong record info dict, Missing Key')

            return False

    def save_record(self):
        save_json(self.__dict__, os.path.join(WORK_DIR, RECORD_FILE_NAME.replace('*', self.id)))
        print('record save, id: ', self.id)


class RECORDManager(object):
    """
    add submit
    check submit by id
    check submit by time
    """
    def __init__(self):
        self.meta = read_json(os.path.join(WORK_DIR, RECORD_FILE_META))
        self.last_open_file_id = self.meta['last_open_file_id']
        self.max_file_id = self.meta['max_file_id']
        self.submit_record = self.meta['submit_record']
        self.delete_record_id = self.meta['delete_record_id']

        self.submit_available_id = [_ for _ in self.meta['submit_record'].values()]
        self.delete_id = self.meta['delete_record_id']

    def _renew_meta(self):
        save_json(self.meta, os.path.join(WORK_DIR, RECORD_FILE_META))
        self.submit_available_id = [_ for _ in self.meta['submit_record'].values()]
        self.delete_id = self.meta['delete_record_id']
        print('renew meta')

    def add_record(self, submit_info: dict):
        if _format_check(submit_info):
            new_record = BasicRECORD()
            temp_id = str(int(self.max_file_id) + 1)
            submit_info["id"] = temp_id
            new_record.set_record(submit_info)
            self.meta['submit_record'][_get_time_string_now()] = temp_id
            self.meta['max_file_id'] = temp_id
            new_record.save_record()
            self._renew_meta()
        else:
            print("submit failed")
            raise AssertionError

    def check_by_id(self, check_id: str):
        """
        :param check_id:
        :return: info
        """
        if check_id not in self.meta['delete_record_id'] and check_id in self.submit_available_id:
            info = _get_record_dict_by_id(check_id)
            self.meta['last_open_file_id'] = check_id
            self._renew_meta()
        else:
            print('check submit id {} do not exist'.format(check_id))
            info = {}

        return info

    def check_by_submit_time(self, year_key: int, month_key: int, day_key: int):
        """
        :param day_key:
        :param month_key:
        :param year_key:
        :return: [info]
        """
        find_id = []
        for time_key in self.meta['submit_record'].keys():
            year, month, day, hour, minute, sec = [int(_) for _ in time_key.split('-')]
            if year_key == year and month_key == month and day_key == day:
                find_id.append(self.meta['submit_record'][time_key])

        find_id = [_ for _ in find_id if _ not in self.delete_id]

        if find_id:
            return [self.check_by_id(_) for _ in find_id]
        else:
            return []

    def check(self, check_id=None, year=None, month=None, day=None):
        all_find = []
        if check_id:
            all_find.append(self.check_by_id(check_id))
        elif year is not None and month is not None and day is not None:
            all_find += self.check_by_submit_time(year, month, day)
        else:
            print('check wrong input')

        for info in all_find:
            print('===' * 20)
            for k, v in info.items():
                print(k, v)

    def delete(self, delete_id):
        if isinstance(delete_id, str):
            if delete_id in self.submit_available_id:
                self.meta['delete_record_id'].append(delete_id)
                self._renew_meta()
                print('delete sumit id: {}'.format(delete_id))


if __name__ == '__main__':
    pass

