# -*- coding:utf-8 -*-
"""
meta.json
    adjacency_matrix: [[0/1]],
    name_list:["name",],
    type_list:["document"/"action"/"record"],
    submit_time_list:["year:0000||month:00||day:00||hour:00||minute:00||second:00", ],
    last_modify_time_list:["year:0000||month:00||day:00||hour:00||minute:00||second:00",],
    version_list:["0.3"],
    show_flag_list:["on"/"off"]
data.json
    name: {"key":"line1", "key": ["line1", "line2"]}

def get(name) -> get certain content
def reset() -> reset system
def add(data_dict, name) -> add
def delete(name) -> delete
def overwrite_data(data_dict, name)
def overwrite_related_names(father_name, name)
def overwrite_name(name)
def overwrite_type(type, name)
def overwrite_version(version, name)
def overwrite_show_flag(glag, name)
"""
import json
import os
import time


def read_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        j = json.load(f)

    return j


def save_json(dict_dataset: dict, name: str):
    """原文件将被覆盖"""
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_dataset, ensure_ascii=False, indent=4))


def get_time_string_now():
    time_p = time.localtime()
    time_string = 'year:{}||month:{}||day:{}||hour:{}||minute:{}||second:{}'.format(
        time_p.tm_year, time_p.tm_mon, time_p.tm_mday, time_p.tm_hour, time_p.tm_min, time_p.tm_sec)

    return time_string


MAIN_WORK_DIR = r'C:\BruceMySpace\_data\APM_backup_version_0.3\DATA'
META = 'meta.json'
DATA = 'data.json'


class FileManager(object):
    def __init__(self):
        self.DATA = read_json(os.path.join(MAIN_WORK_DIR, DATA))
        self.META = read_json(os.path.join(MAIN_WORK_DIR, META))

    def renew_data(self):
        save_json(self.DATA, os.path.join(MAIN_WORK_DIR, DATA))
        save_json(self.META, os.path.join(MAIN_WORK_DIR, META))
        print('successfully submit !')


def check_data_dict_format(data_dict):
    flag = True
    for k, v in data_dict.items():
        if isinstance(k, str):
            if isinstance(v, list):
                for kk in v:
                    if isinstance(kk, str):
                        pass
                    else:
                        flag = False
                        print('item: {} in list value is not a string'.format(kk))
            else:
                if isinstance(v, str):
                    pass
                else:
                    flag = False
                    print('value: {} in data_dict is not a string or list of strings !'.format(v))
        else:
            flag = False
            print('key: {} in data_dict is not string !'.format(k))

    return flag


def get(name: str):
    result = {}
    if isinstance(name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            result['name'] = name
            result['data'] = fm.DATA[name]

            index = fm.META['name_list'].index(name)
            result['type'] = fm.META['type_list'][index]
            result['submit_time'] = fm.META['submit_time_list'][index]
            result['last_modify_time'] = fm.META['last_modify_time_list'][index]
            result['version'] = fm.META['version_list'][index]
            result['show_flag'] = fm.META['show_flag_list'][index]

            temp = []
            for re_index, connect in enumerate(fm.META['adjacency_matrix'][index]):
                if connect:
                    temp.append(fm.META["name_list"][re_index])
            result['related_names'] = temp

            return result

        else:
            print('{} does not exists !'.format(name))
            return result
    else:
        print('delete name should be string !')
        return result


def add(data_dict: dict, name: str, type_: str, version: str, show_flag_list: str, related_names: list):
    flag = True
    fm = FileManager()

    if isinstance(data_dict, dict) and isinstance(name, str) and isinstance(type_, str) \
            and isinstance(version, str) and isinstance(show_flag_list, str) and isinstance(related_names, list):
        for related_name in related_names:
            if not isinstance(related_name, str):
                flag = False
                print('wrong name list, not string !')
            if related_name not in fm.META['name_list']:
                flag = False
                print('wrong name list, unknown name: {} !'.format(related_name))
    else:
        flag = False
        print('wrong add input, not string or dict!')

    if not check_data_dict_format(data_dict):
        flag = False

    if flag:
        if name not in fm.META['name_list']:
            fm.DATA[name] = data_dict
            fm.META['name_list'].append(name)
            fm.META['type_list'].append(type_)
            fm.META['submit_time_list'].append(get_time_string_now())
            fm.META['last_modify_time_list'].append(get_time_string_now())
            fm.META['version_list'].append(version)
            fm.META['show_flag_list'].append(show_flag_list)

            for row in fm.META['adjacency_matrix']:
                row.append(0)
            fm.META['adjacency_matrix'].append([0] * (len(fm.META['name_list']) - 1) + [1])

            for re_name in related_names:
                re_index = fm.META['name_list'].index(re_name)
                fm.META['adjacency_matrix'][re_index][-1] = 1
                fm.META['adjacency_matrix'][-1][re_index] = 1

            fm.renew_data()
        else:
            print('name: {}, exists !'.format(name))


def delete(name: str):
    if isinstance(name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            index = fm.META['name_list'].index(name)
            del fm.DATA[name]
            del fm.META['name_list'][index]
            del fm.META['type_list'][index]
            del fm.META['submit_time_list'][index]
            del fm.META['last_modify_time_list'][index]
            del fm.META['version_list'][index]
            del fm.META['show_flag_list'][index]

            for row in fm.META['adjacency_matrix']:
                del row[index]
            del fm.META['adjacency_matrix'][index]

            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))
    else:
        print('delete name should be string !')


def overwrite_data(data_dict: dict, name: str):
    flag = True
    fm = FileManager()

    if isinstance(data_dict, dict) and isinstance(name, str):
        pass
    else:
        flag = False
        print('wrong add input, not string or dict !')

    if not check_data_dict_format(data_dict):
        flag = False

    if flag:
        if name in fm.META['name_list']:
            fm.DATA[name] = data_dict
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()
            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))


def overwrite_related_names(related_names: list, name: str):
    flag = True
    fm = FileManager()

    if isinstance(name, str) and isinstance(related_names, list):
        for related_name in related_names:
            if not isinstance(related_name, str):
                flag = False
                print('wrong name list, not string !')
            if related_name not in fm.META['name_list']:
                flag = False
                print('wrong name list, unknown name: {} !'.format(related_name))
    else:
        flag = False
        print('wrong add input, not string or dict!')

    if flag:
        if name in fm.META['name_list']:
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()

            for row in fm.META['adjacency_matrix']:
                row[index] = 0
            fm.META['adjacency_matrix'][index] = [0]*len(fm.META['name_list'])

            for re_name in related_names:
                re_index = fm.META['name_list'].index(re_name)
                fm.META['adjacency_matrix'][re_index][-1] = 1
                fm.META['adjacency_matrix'][-1][re_index] = 1

            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))


def overwrite_name(new_name: str, name: str):
    if isinstance(name, str) and isinstance(new_name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            data_dict = fm.DATA[name]
            del fm.DATA[name]
            fm.DATA[new_name] = data_dict
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()
            fm.META['name_list'][index] = new_name
            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))
    else:
        print('wrong input type, not string !')


def overwrite_type(type_: str, name: str):
    if isinstance(type_, str) and isinstance(name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()
            fm.META['type_list'][index] = type_
            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))
    else:
        print('wrong input type, not string !')


def overwrite_version(version: str, name: str):
    if isinstance(version, str) and isinstance(name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()
            fm.META['version_list'][index] = version
            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))
    else:
        print('wrong input type, not string !')


def overwrite_show_flag(flag: str, name: str):
    if isinstance(flag, str) and isinstance(name, str):
        fm = FileManager()
        if name in fm.META['name_list']:
            index = fm.META['name_list'].index(name)
            fm.META['last_modify_time_list'][index] = get_time_string_now()
            fm.META['version_list'][index] = flag
            fm.renew_data()
        else:
            print('{} does not exists !'.format(name))
    else:
        print('wrong input type, not string !')


def reset():
    check = input('system will be reset, Make sure the data is backed up'
                  'if you want to reset system, please input [reset now]: ')
    if check == 'reset now':
        fm = FileManager()
        fm.DATA = {}
        fm.META = {
            "adjacency_matrix": [],
            "name_list": [],
            "type_list": [],
            "submit_time_list": [],
            "last_modify_time_list": [],
            "version_list": [],
            "show_flag_list": []
        }
        fm.renew_data()
