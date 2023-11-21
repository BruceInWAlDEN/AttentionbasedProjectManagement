# -*- coding:utf-8 -*-
import os
from .RECORD import read_json
from .RECORD import save_json
from .RECORD import _get_time_string_now
from .RECORD import RECORDManager


WORK_DIR = r"C:\Users\Bruce\Desktop\AttentionbasedProjectManagement\DATA"
ACTION_FILE_NAME = 'ACTION_*.json'
ACTION_FILE_NETA = 'ACTION_META.json'


def show_action_template():
    print('{')
    print("\t" + "\"" + "goal" + "\"" + ": " + "\"\"" + ",")
    print("\t" + "\"" + "methods" + "\"" + ": " + "\"\"" + ",")
    print("\t" + "\"" + "feedback" + "\"" + ": " + "\"\"" + ",")
    print("\t" + "\"" + "realated_files" + "\"" + ": " + "\"\"" + ",")
    print('}')


def _check_action_format(action_dict: dict):
    flag = True
    for k, v in action_dict.items():
        if isinstance(v, str):
            pass
        else:
            flag = False

    return flag


def get_related_file_string(basicfile_list: list):
    related_file_string = ""
    for file in basicfile_list:
        related_file_string += "||"
        related_file_string += file.get_file_string()
    related_file_string += "||"

    return related_file_string


def _get_action_dict_by_id(record_id: str):
    info_dict = read_json(os.path.join(WORK_DIR, ACTION_FILE_NAME.replace('*', record_id)))

    return info_dict


class BasicFile(object):
    def __init__(self, file_type: str, context: str):
        # file_full_path url description
        if not isinstance(context, str):
            print('wrong file context')
            raise AssertionError
        if file_type not in ['file_full_path', 'url', 'description']:
            print('wrong file_type')
            raise AssertionError

        self.type = file_type
        self.context = context

    def get_file_string(self):
        return self.type + "-->" + self.context


class ACTION(object):
    def __init__(self):
        self.meta = read_json(os.path.join(WORK_DIR, ACTION_FILE_NETA))
        self.max_file_id = self.meta['max_file_id']
        self.delete_id = self.meta['delete_action_id']
        self.available_id = [_ for _ in self.meta['submit_record'].values()]

        self.action_related_record = self.meta["action_related_record"]

    def _renew_meta(self):
        save_json(self.meta, os.path.join(WORK_DIR, ACTION_FILE_NETA))
        self.available_id = [_ for _ in self.meta['submit_record'].values()]
        self.action_related_record = self.meta["action_related_record"]
        self.delete_id = self.meta['delete_action_id']
        print('renew meta')

    def delete(self, delete_id):
        if isinstance(delete_id, str):
            if delete_id in self.available_id:
                self.meta['delete_action_id'].append(delete_id)
                self._renew_meta()
                print('delete sumit id: {}'.format(delete_id))

    def add_action(self, sumit_dict: dict):
        if _check_action_format(sumit_dict):
            temp_id = str(int(self.max_file_id) + 1)
            self.meta['max_file_id'] = temp_id
            self.meta['submit_record'][_get_time_string_now()] = temp_id
            self.meta['action_related_record'][temp_id] = []
            save_json(sumit_dict, os.path.join(WORK_DIR, ACTION_FILE_NAME.replace('*', temp_id)))
            print('save submit: ', temp_id)
            self._renew_meta()

    def check_by_id(self, check_id: str):
        """
        :param check_id:
        :return: info
        """
        if check_id not in self.meta['delete_action_id'] and check_id in self.available_id:
            info = _get_action_dict_by_id(check_id)
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

    def check_action(self, check_id=None, year=None, month=None, day=None):
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

    def check_related_record(self, action_id):
        records = RECORDManager()
        for check_id in self.action_related_record[action_id]:
            records.check(check_id=check_id)

    def add_record(self, action_id, record_id):
        if action_id in self.available_id:
            if record_id not in self.action_related_record[action_id]:
                self.meta["action_related_record"][action_id].append(record_id)
                self._renew_meta()
            else:
                print("record id {}, already added".format(record_id))
        else:
            print('action id {} do not exist'.format(action_id))
