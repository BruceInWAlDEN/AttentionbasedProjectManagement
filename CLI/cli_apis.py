"""
实现交互输入过程
prompt实现block的提交
用ptpython实现block显示面板，只读
"""
import os

from core.DataStructure import *
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as fprint
from prompt_toolkit import HTML as H
import shutil

apis = [
    'create',
    'show_all',
    'modify',
    'show',
    'help',
    'backup',
    'reset_system',
    'load_backup',
    'manual',
]


def create():
    block_completer = WordCompleter(
        [
            get_time_string_now(),
            'document',
            'action',
        ],
        ignore_case=True,
    )

    block_type = None
    while block_type not in ['r', 'a', 'd']:
        block_type = prompt(
            "choose type: d / a / r: ",
            completer=block_completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
        )
        block_type = block_type.lower()

    json_dict = {}
    block = eval({'r': 'RECORD', 'a': 'ACTION', 'd': 'DOCUMENT'}[block_type] + '()')

    if block_type == 'r' or block_type == 'd':
        for k, v in block.__dict__.items():
            re = prompt(
                "{}: ".format(k),
                completer=block_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
                default=v if isinstance(v, str) else str(v)
            )
            json_dict[k] = re

    if block_type == 'a':
        for k, v in block.__dict__.items():
            if k != 'steps':
                re = prompt(
                    "{}: ".format(k),
                    completer=block_completer,
                    complete_style=CompleteStyle.MULTI_COLUMN,
                    default=v if isinstance(v, str) else str(v)
                )
                json_dict[k] = re
            else:
                session = PromptSession()
                text = 'None'
                data = []
                while text and '##' not in text:
                    text = session.prompt(
                        completer=block_completer,
                        complete_style=CompleteStyle.MULTI_COLUMN,
                        default=v[0]
                    )
                    if text:
                        data.append(text.replace('##', ''))

                json_dict[k] = data

    print('----------------------------------{}----------------------------------'.format(block_type.upper()))
    for k, v in json_dict.items():
        if 'file' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in decoder_file_string(v):
                fprint(H('  ' + "<b>" + vv + "</b>"))
        if 'steps' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in v:
                fprint(H('  ' + "<b>" + vv + "</b>"))
        else:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ": " + "<b>" + v + "</b>"))
    print('')

    y_or_n = prompt(
        "if you want to create: yes or no: ",
        completer=block_completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default='yes'
    )

    if y_or_n.lower() == 'yes' or y_or_n.lower() == 'y':
        if block_type == 'r':
            re = 'none'
            while re.lower() not in ['document', 'action']:
                re = prompt(
                    "choose doc or action: ",
                    completer=block_completer,
                    complete_style=CompleteStyle.MULTI_COLUMN,
                    default='action'
                )
            if re == 'document':
                re = prompt(
                    "choose document id: ",
                    completer=block_completer,
                    complete_style=CompleteStyle.MULTI_COLUMN,
                )

                write_record(json_dict, document_id=re)
            if re == 'action':
                re = prompt(
                    "choose action id: ",
                    completer=block_completer,
                    complete_style=CompleteStyle.MULTI_COLUMN,
                )
                write_record(json_dict, action_id=re)

        if block_type == 'a':
            re = prompt(
                "choose document id: ",
                completer=block_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
            )
            write_action(json_dict, document_id=re)
        if block_type == 'd':
            write_document(json_dict)


def modify():
    block_completer = WordCompleter(
        [
            get_time_string_now(),
            'document',
            'action',
        ],
        ignore_case=True,
    )

    modify_id = prompt(
        "choose modify block id: ",
        completer=block_completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
    )

    json_dict = get_block(block_id=modify_id)[0]
    block_type = json_dict['block_type']
    out_keys = ['block_type', 'block_id', 'submit_time', 'last_overwrite_time', 'block_state']
    json_dict = {k: v for k, v in json_dict.items() if k not in out_keys}

    print('----------------------------------{}----------------------------------'.format(block_type))
    for k, v in json_dict.items():
        if 'file' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in decoder_file_string(v):
                fprint(H('  ' + "<b>" + vv + "</b>"))
        if 'steps' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in v:
                fprint(H('  ' + "<b>" + vv + "</b>"))
        else:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ": " + "<b>" + v + "</b>"))
    print('')
    print('------overwrite here -')
    new_json_dict = {}
    for k, v in json_dict.items():
        if k != 'steps':
            re = prompt(
                "{}: ".format(k),
                completer=block_completer,
                complete_style=CompleteStyle.MULTI_COLUMN,
                default=json_dict[k]
            )
            new_json_dict[k] = re
        else:
            session = PromptSession()
            text = 'None'
            data = []
            count = 0
            while text and '##' not in text:
                text = session.prompt(
                    completer=block_completer,
                    complete_style=CompleteStyle.MULTI_COLUMN,
                    default=json_dict[k][count] if count <= len(json_dict[k]) - 1 else json_dict[k][-1]
                )
                count += 1
                if text:
                    data.append(text.replace('##', ''))

            new_json_dict[k] = data

    print('----------------------------------{}----------------------------------'.format(block_type.upper()))
    for k, v in json_dict.items():
        if 'file' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in decoder_file_string(v):
                fprint(H('  ' + "<b>" + vv + "</b>"))
        if 'steps' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in v:
                fprint(H('  ' + "<b>" + vv + "</b>"))
        else:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ": " + "<b>" + v + "</b>"))
    print('')

    y_or_n = prompt(
        "if you want to modify: yes or no: ",
        completer=block_completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default='yes'
    )

    state = prompt(
        "if you want to close the block: ",
        completer=block_completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default='no'
    )

    if y_or_n.lower() == 'yes' or y_or_n.lower() == 'y':
        if state == 'yes':
            overwrite_block(block_type=block_type, block_id=modify_id, json_dict=new_json_dict, state='off')
        else:
            overwrite_block(block_type=block_type, block_id=modify_id, json_dict=new_json_dict, state='on')


def show_all():
    fm = FileManager()
    document_ids = fm.FILE_META['submit_type_id_statistic']['DOCUMENT']
    for document_id in document_ids:
        fprint(H('<b>---------------------------------------------------------------------------------------</b>'))
        if fm.FILE_META['block_state'][document_id] == 'on':
            temp = '|' + '<style fg="ansiwhite" bg="ansiblue">D[' + document_id + ']</style> ' + \
                   fm.FILE_BLOCK_DATA[document_id]['doc_outline']
            fprint(H(temp))
        else:
            temp = '<s>' + '|' + '<style fg="ansiwhite" bg="ansiblue">D[' + document_id + ']</style> ' + \
                    fm.FILE_BLOCK_DATA[document_id]['doc_outline'] + "</s>"
            fprint(H(temp))
        index = fm.FILE_DATA_ID_LIST['id_list'].index(document_id)

        for block_index, connect in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][index]):
            if connect and block_index != 0:
                if fm.FILE_DATA_ID_LIST['id_list'][block_index] in fm.FILE_META['submit_type_id_statistic']['ACTION']:
                    if fm.FILE_META['block_state'][fm.FILE_DATA_ID_LIST['id_list'][block_index]] == 'on':
                        temp = '|--|' + '<style fg="ansiwhite" bg="ansiyellow">A[' + fm.FILE_DATA_ID_LIST['id_list'][
                            block_index] + ']</style> ' + \
                               fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['goal']
                    else:
                        temp = "<s>" + '|--|' + '<style fg="ansiwhite" bg="ansiyellow">A[' + fm.FILE_DATA_ID_LIST['id_list'][
                            block_index] + ']</style> ' + \
                            fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['goal'] + "</s>"
                    fprint(H(temp))

                    for block_index_, connect_ in enumerate(
                            fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][block_index]):
                        if connect_ and block_index_ != block_index and block_index_ != index:
                            if fm.FILE_META['block_state'][fm.FILE_DATA_ID_LIST['id_list'][block_index_]] == 'on':
                                temp = '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + \
                                       fm.FILE_DATA_ID_LIST['id_list'][block_index_] + ']</style> ' + \
                                       str(calculate_time(
                                           fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time'],
                                           fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['end_time']
                                       )) + ' minutes ' + \
                                       fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time']
                            else:
                                temp = "<s>" + '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + \
                                       fm.FILE_DATA_ID_LIST['id_list'][block_index_] + ']</style> ' + \
                                       str(calculate_time(
                                           fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]][
                                               'start_time'],
                                           fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['end_time']
                                       )) + ' minutes ' + \
                                       fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time'] + '</s>'
                            fprint(H(temp))
                else:
                    if fm.FILE_META['block_state'][fm.FILE_DATA_ID_LIST['id_list'][block_index]] == 'on':
                        temp = '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + fm.FILE_DATA_ID_LIST['id_list'][
                            block_index] + ']</style> ' + \
                               str(calculate_time(
                                   fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['start_time'],
                                   fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['end_time']
                               )) + ' minutes ' + \
                               fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['start_time']
                    else:
                        temp = "<s>" + '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + fm.FILE_DATA_ID_LIST['id_list'][
                            block_index] + ']</style> ' + \
                               str(calculate_time(
                                   fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['start_time'],
                                   fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['end_time']
                               )) + ' minutes ' + \
                               fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['start_time'] + '</s>'
                    fprint(H(temp))


def show():
    show_id = prompt(
        "choose modify block id: ",
        complete_style=CompleteStyle.MULTI_COLUMN,
    )

    json_dict = get_block(block_id=show_id)[0]
    block_type = json_dict['block_type']
    out_keys = ['block_type', 'block_id', 'submit_time', 'last_overwrite_time']
    json_dict = {k: v for k, v in json_dict.items() if k not in out_keys}

    print('----------------------------------{}----------------------------------'.format(block_type))
    for k, v in json_dict.items():
        if 'file' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in decoder_file_string(v):
                fprint(H('  ' + "<b>" + vv + "</b>"))
        if 'steps' in k:
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ":"))
            for vv in v:
                fprint(H('  ' + "<b>" + vv + "</b>"))
        else:
            v = v if isinstance(v, str) else str(v)
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ": " + "<b>" + v + "</b>"))
    print('')


def backup():
    save_path = prompt(
        "backup data to dir path (full path): ",
        complete_style=CompleteStyle.MULTI_COLUMN,
    )
    if not os.path.exists(save_path):
        print('path {} do not exists'.format(save_path))

    else:
        if not os.path.isdir(save_path):
            print('path {} is not a dir'.format(save_path))
        else:
            check = input('if you want to backup the data? \n'
                          'des dir files will be overwritten, please make sure a blank dir\n'
                          'you can input: $i$really$want$to$do$that$ to backup \n -> ')
            if check == '$i$really$want$to$do$that$':
                if len(os.listdir(save_path)) == 0:
                    for file in os.listdir(MAIN_WORK_DIR):
                        shutil.copy(os.path.join(MAIN_WORK_DIR, file), save_path)
                    print('Successfully backup data at --> {}'.format(save_path))
                else:
                    print('des dir is not a blank dir')


def reset_system():
    reset_sys()


def load_backup():
    load_path = prompt(
        "load backup from dir path (full path): ",
        complete_style=CompleteStyle.MULTI_COLUMN,
    )
    if not os.path.exists(load_path):
        print('path {} do not exists'.format(load_path))

    else:
        if not os.path.isdir(load_path):
            print('path {} is not a dir'.format(load_path))
        else:
            out = input('if you want to reset the whole system ? \n'
                        'ori data will be covered, please make sure you have backup the data.\n'
                        'you can input: $i$really$want$to$do$that$ to load backup \n -> ')
            if out == '$i$really$want$to$do$that$':
                flag = 0
                for file in os.listdir(load_path):
                    if file in [FILE_META, FILE_BLOCK_DATA, FILE_DATA_ID_LIST, FILE_DATA_RELATION_MATRIX]:
                        flag += 1

                if flag == 4:
                    for file in os.listdir(load_path):
                        if file in [FILE_META, FILE_BLOCK_DATA, FILE_DATA_ID_LIST, FILE_DATA_RELATION_MATRIX]:
                            shutil.copy(os.path.join(load_path, file), os.path.join(MAIN_WORK_DIR, file))
                    print('Successfully load data from --> {}'.format(load_path))
                else:
                    print('Incomplete files in dir: {}'.format(load_path))
