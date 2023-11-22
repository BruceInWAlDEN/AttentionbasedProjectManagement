# -*- coding:utf-8 -*-
"""
file
    data_relation_matrix.json
    data_id_list.json
    block_data.json
    meta.json

class
    BasicBlock
    DOCUMENT
    ACTION
    RECORD

def
    get_time_string_now()
    get_file_string(type, content)
    get_file_string_list(file_string_list)
    read_json()
    save_json()

def
    get_block(type, id, name, year, month, day) -> json_dict_list
    overwrite_block(type, id, json_dict)
    write_record(json_dict, document_id, action_id)
    write_action(json_dict, document_id)
    write_document(json_dict)
    delete_block(type, id)
    show_simple()
"""
import os
import json
import time


def get_time_string_now():
    time_p = time.localtime()
    time_string = 'year:{}||month:{}||day:{}||hour:{}||minute:{}||second:{}'.format(
        time_p.tm_year, time_p.tm_mon, time_p.tm_mday, time_p.tm_hour, time_p.tm_min, time_p.tm_sec)

    return time_string


def decode_time_string(time_string):
    # 'year:{}||month:{}||day:{}||hour:{}||minute:{}||second:{}'
    year_index_s = time_string.index('year:') + 5
    year_index_e = time_string.index('||month')
    year = time_string[year_index_s:year_index_e]
    month_index_s = time_string.index('month:') + 6
    month_index_e = time_string.index('||day')
    month = time_string[month_index_s:month_index_e]
    day_index_s = time_string.index('day:') + 4
    day_index_e = time_string.index('||hour')
    day = time_string[day_index_s:day_index_e]

    return year, month, day


def get_file_string(file_type, content):

    return file_type + "-->" + content


def get_file_string_list(file_string_list):
    related_file_string = ""
    for file in file_string_list:
        related_file_string += "||"
        related_file_string += file
    related_file_string += "||"

    return related_file_string


class BasicBlock(object):
    def get_template(self):
        print('{')
        for k, v in self.__dict__.items():
            if k != 'ID' and k != 'submit_time' and k != 'block_type':
                v = "\"" + v + "\"" if isinstance(v, str) else str(v)
                print("\t" + "\"" + k + "\"" + ": " + v + ",")
        print('}')

    def get_json_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != 'ID' and k != "submit_time"}

    def check_submit_format(self, json_dict):
        flag = True
        if isinstance(json_dict, dict):
            for key in self.__dict__.keys():
                if key in json_dict.keys():
                    if 'score' in key:
                        if json_dict[key] in [1, 2, 3, 4, 5]:
                            pass
                        else:
                            print('error info format: wrong score: , should be 1-5', json_dict[key])
                            flag = False
                    elif 'time' in key:
                        if isinstance(key, str):
                            if time.strptime(json_dict[key], 'year:%Y||month:%m||day:%d||hour:%H||minute:%M||second:%S'):
                                pass
                            else:
                                print('error info format: wrong time')
                                flag = False
                        else:
                            print('error info format: wrong time')
                            flag = False
                    else:
                        if isinstance(json_dict[key], str):
                            pass
                        else:
                            print('error info format: value of -> {} <- not a str'.format(key))

                else:
                    print('error info format: key missing: ', key)
                    flag = False
        else:
            print('not a json_dict')
            flag = False

        return flag


class DOCUMENT(BasicBlock):
    def __init__(self):
        super().__init__()
        self.doc_outline = "a program for attetnionbasedProjectManagement project"
        self.doc_file = get_file_string_list([
            get_file_string('file_full_path', 'init'),
            get_file_string('url', 'init'),
            get_file_string('description', 'init'),
        ])


class ACTION(BasicBlock):
    def __init__(self):
        super().__init__()
        self.related_file = get_file_string_list([
            get_file_string('file_full_path', 'init'),
            get_file_string('url', 'init'),
            get_file_string('description', 'init'),
        ])

        self.goal = "a result"
        self.methods = "detailed"
        self.feedback = "statement but feeling"


class RECORD(BasicBlock):
    def __init__(self):
        super().__init__()
        self.start_time = get_time_string_now()
        self.end_time = get_time_string_now()
        self.start_passion_score = 5
        self.end_feeling_score = 5
        self.attention_score = 5
        self.passion_description = "feeling and reason"
        self.feeling_description = "feeling and reason"
        self.attention_description = "feeling and reason"
        self.work_env_description = "objective"


def read_json(json_path: str) -> dict:
    with open(json_path, 'r', encoding='utf-8') as f:
        j = json.load(f)

    return j


def save_json(dict_dataset: dict, name: str):
    """原文件将被覆盖"""
    with open(name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(dict_dataset, ensure_ascii=False, indent=4))


def get_temp_late(block_type=None):
    if block_type in ['RECORD', 'ACTION', 'DOCUMENT']:
        block = eval(block_type + "()")
        block.get_template()
    else:
        print('wrong block type: ', block_type)

"""
every call of follow func, file should renew and show sign
"""
MAIN_WORK_DIR = r'C:\Users\Bruce\Desktop\AttentionbasedProjectManagement\DATA'
FILE_DATA_RELATION_MATRIX = 'data_relation_matrix.json'     # [[0/1]]
FILE_DATA_ID_LIST = 'data_id_list.json'     # [""]
FILE_BLOCK_DATA = 'block_data.json'     # {"": {}}
FILE_META = 'meta.json'     # {"": }


class FileManager(object):
    def __init__(self):
        self.FILE_DATA_RELATION_MATRIX = read_json(os.path.join(MAIN_WORK_DIR, FILE_DATA_RELATION_MATRIX))
        self.FILE_DATA_ID_LIST = read_json(os.path.join(MAIN_WORK_DIR, FILE_DATA_ID_LIST))
        self.FILE_BLOCK_DATA = read_json(os.path.join(MAIN_WORK_DIR, FILE_BLOCK_DATA))
        self.FILE_META = read_json(os.path.join(MAIN_WORK_DIR, FILE_META))

    def renew_data(self):
        save_json(self.FILE_DATA_RELATION_MATRIX, os.path.join(MAIN_WORK_DIR, FILE_DATA_RELATION_MATRIX))
        save_json(self.FILE_DATA_ID_LIST, os.path.join(MAIN_WORK_DIR, FILE_DATA_ID_LIST))
        save_json(self.FILE_BLOCK_DATA, os.path.join(MAIN_WORK_DIR, FILE_BLOCK_DATA))
        save_json(self.FILE_META, os.path.join(MAIN_WORK_DIR, FILE_META))
        print('data renew')


def get_block(block_type=None, block_id=None, year=None, month=None, day=None):
    all_id = []
    fm = FileManager()
    if block_id is not None and block_id not in fm.FILE_META['delete_id']:
        return [fm.FILE_BLOCK_DATA[block_id]]
    if block_type in ['RECORD', 'ACTION', 'DOCUMENT']:
        for check_id in fm.FILE_META['submit_type_id_statistic'][block_type]:
            check_year, check_month, check_day = decode_time_string(fm.FILE_BLOCK_DATA[check_id]['submit_time'])
            flag = 1
            if not check_year == year or year is None:
                flag = 0
            if not check_month == month or month is None:
                flag = 0
            if not check_day == day or day is None:
                flag = 0
            if flag:
                all_id.append(check_id)
        all_id = [_ for _ in all_id if _ not in fm.FILE_META['delete_id']]
        return [fm.FILE_BLOCK_DATA[_] for _ in all_id]

    if block_type is None:
        for block_type in ['RECORD', 'ACTION', 'DOCUMENT']:
            for check_id in fm.FILE_META['submit_type_id_statistic'][block_type]:
                check_year, check_month, check_day = decode_time_string(fm.FILE_BLOCK_DATA[check_id]['submit_time'])
                flag = 1
                if not check_year == year or year is None:
                    flag = 0
                if not check_month == month or month is None:
                    flag = 0
                if not check_day == day or day is None:
                    flag = 0
                if flag:
                    all_id.append(check_id)
        all_id = [_ for _ in all_id if _ not in fm.FILE_META['delete_id']]
        return [fm.FILE_BLOCK_DATA[_] for _ in all_id]


def overwrite_block(block_type, json_dict, block_id: str):
    fm = FileManager()
    if block_id in fm.FILE_META['all_id'] and block_id not in fm.FILE_META['delete_id']:
        if block_type in ['RECORD', 'ACTION', 'DOCUMENT']:
            block = eval(block_type + '()')
            if block.check_submit_format(json_dict):
                fm.FILE_BLOCK_DATA[block_id] = json_dict
                fm.FILE_META['submit_time'][block_id] = get_time_string_now()
                fm.renew_data()
            else:
                print('wrong json dict format')
        else:
            print('wrong block type: ', block_type)
    else:
        print('block id {}, is not exist or deleted'.format(block_id))


def write_record(json_dict=None, document_id=None, action_id=None):
    fm = FileManager()
    record_block = RECORD()
    if record_block.check_submit_format(json_dict):

        flag = 0
        if document_id in fm.FILE_META['submit_type_id_statistic']['DOCUMENT'] \
                and document_id not in fm.FILE_META['delete_id'] and action_id is None:
            flag = 1
        if action_id in fm.FILE_META['submit_type_id_statistic']['ACTION'] \
                and action_id not in fm.FILE_META['delete_id'] and document_id is None:
            flag = 1

        if flag:
            # add data
            temp_id = str(max([int(_) for _ in fm.FILE_META['all_id']]) + 1)
            fm.FILE_BLOCK_DATA[temp_id] = json_dict
            fm.FILE_META['submit_time'][temp_id] = get_time_string_now()

            # add relation
            fm.FILE_DATA_ID_LIST['id_list'].append(temp_id)
            f_id = document_id if document_id is not None else action_id
            f_index = fm.FILE_DATA_ID_LIST['id_list'].index(f_id)
            for row_index, row in enumerate(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']):
                if row_index == f_index:
                    row.append(1)
                else:
                    row.append(0)
            add_line = [0 for _ in range(len(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']) + 1)]
            add_line[f_index] = 1
            fm.FILE_DATA_RELATION_MATRIX['relation_matrix'].append(add_line)

            # renew statistic
            fm.FILE_META["submit_type_id_statistic"]['RECORD'].append(temp_id)
            fm.FILE_META['all_id'].append(temp_id)

            fm.renew_data()

        else:
            print('give a exist document_id or an action_id')
    else:
        print('wrong record json dict format')


def write_action(json_dict, document_id):
    fm = FileManager()
    action_block = ACTION()
    if action_block.check_submit_format(json_dict):

        if document_id in fm.FILE_META['submit_type_id_statistic']['DOCUMENT'] \
                and document_id not in fm.FILE_META['delete_id']:

            # add data
            temp_id = str(max([int(_) for _ in fm.FILE_META['all_id']]) + 1)
            fm.FILE_BLOCK_DATA[temp_id] = json_dict
            fm.FILE_META['submit_time'][temp_id] = get_time_string_now()

            # add relation
            fm.FILE_DATA_ID_LIST['id_list'].append(temp_id)
            f_index = fm.FILE_DATA_ID_LIST['id_list'].index(document_id)
            for row_index, row in enumerate(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']):
                if row_index == f_index:
                    row.append(1)
                else:
                    row.append(0)
            add_line = [0 for _ in range(len(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']) + 1)]
            add_line[f_index] = 1
            fm.FILE_DATA_RELATION_MATRIX['relation_matrix'].append(add_line)

            # renew statistic
            fm.FILE_META["submit_type_id_statistic"]['ACTION'].append(temp_id)
            fm.FILE_META['all_id'].append(temp_id)

            fm.renew_data()

        else:
            print('give a exist document_id')
    else:
        print('wrong action json dict format')


def write_document(json_dict):
    fm = FileManager()
    document_block = DOCUMENT()
    if document_block.check_submit_format(json_dict):

        # add data
        temp_id = str(max([int(_) for _ in fm.FILE_META['all_id']]) + 1)
        fm.FILE_BLOCK_DATA[temp_id] = json_dict
        fm.FILE_META["submit_time"][temp_id] = get_time_string_now()

        # add relation
        fm.FILE_DATA_ID_LIST['id_list'].append(temp_id)
        f_index = fm.FILE_DATA_ID_LIST['id_list'].index('0')
        for row_index, row in enumerate(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']):
            if row_index == f_index:
                row.append(1)
            else:
                row.append(0)
        add_line = [0 for _ in range(len(fm.FILE_DATA_RELATION_MATRIX['relation_matrix']) + 1)]
        add_line[f_index] = 1
        fm.FILE_DATA_RELATION_MATRIX['relation_matrix'].append(add_line)

        # renew statistic
        fm.FILE_META["submit_type_id_statistic"]['DOCUMENT'].append(temp_id)
        fm.FILE_META['all_id'].append(temp_id)

        fm.renew_data()

    else:
        print('wrong action json dict format')


def delete_block(block_type, block_id: str):
    fm = FileManager()
    if block_id in fm.FILE_META['submit_type_id_statistic'][block_type] and block_id not in fm.FILE_META['delete_id']:
        fm.FILE_META['delete_id'].append(block_id)
        fm.renew_data()
    else:
        print('block_id do not exist or already deleted')


def show_simple():
    fm = FileManager()
    document_ids = fm.FILE_META['submit_type_id_statistic']['DOCUMENT']
    for document_id in document_ids:
        print('->', document_id)
        index = fm.FILE_DATA_ID_LIST['id_list'].index(document_id)
        for block_index, connect in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][index]):
            if connect and block_index != 0:
                print(' ->', fm.FILE_DATA_ID_LIST['id_list'][block_index])
                for block_index_, connect_ in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][block_index]):
                    if connect_ and block_index_ != block_index and block_index_ != index:
                        print('    ->', fm.FILE_DATA_ID_LIST['id_list'][block_index_])

