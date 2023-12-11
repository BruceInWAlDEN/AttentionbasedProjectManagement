# -*- coding:utf-8 -*-
from core.core_json import *
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as fprint
from prompt_toolkit import HTML as H
import shutil

"""
version 0.3.0
"""

apis = [
    'submit',
    'show_all',
    'modify',
]

"""
RECORD:
    start_time:"year:0000||month:00||day:00||hour:00||minute:00||second:00"
    end_time:"year:0000||month:00||day:00||hour:00||minute:00||second:00"
    start_passion: good normal bad
    end_feedback: good normal bad
    environment: env description
    add_info: only about attention and work effectiveness

ACTION:
    goal: " "
    steps: ["step -> result", ""]

DOCUMENT:
    title: " "
    info: ["", ""]
"""

completer = WordCompleter(
    [
        get_time_string_now(),
        'document',
        'action',
        'record',
        'submit',
        'goal',
        'steps',
        'title',
        'info',
        'start_time',
        'end_time',
        'start_passion',
        'end_passion',
        'environment',
        'add_info'
        '||',
        '实验室'
    ],
    ignore_case=True,
)


def _decode_time_string(time_string):
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
    hour_index_s = time_string.index('hour:') + 5
    hour_index_e = time_string.index('||minute')
    hour = time_string[hour_index_s:hour_index_e]
    minute_index_s = time_string.index('minute:') + 7
    minute_index_e = time_string.index('||second')
    minute = time_string[minute_index_s:minute_index_e]
    second_index_s = time_string.index('second:') + 7
    second = time_string[second_index_s:]

    return year, month, day, hour, minute, second


def calculate_time(start_time_string, end_time_string):
    """
    return: minutes int
    """
    s = _decode_time_string(start_time_string)
    e = _decode_time_string(end_time_string)
    year, month, day, hour, minute, second = map(lambda x: int(e[x])-int(s[x]), range(6))
    second_time = day*24*60*60 + hour*60*60 + minute*60 + second

    return second_time // 60


def show_choice_type(key, value):
    if value == "good":
        fprint(H('<orange>' + key + '</orange>' + ": " + "<b>" + value + "</b>"))
    elif value == 'normal':
        fprint(H('<orange>' + key + '</orange>' + ": " + "<b>" + value + "</b>"))
    elif value == 'bad':
        fprint(H('<orange>' + key + '</orange>' + ": " + "<b>" + value + "</b>"))
    else:
        fprint(H('<orange>' + key + '</orange>' + ": " + "<b>" + value + "</b>"))


def show_description_type(key, value):
    fprint(H('<aqua>' + key + '</aqua>' + ": " + "<b>" + value + "</b>"))


def show_list_description_type(key, value_list):
    fprint(H('<coral>' + key + '</coral>'))
    for value in value_list:
        fprint(H('<blanchedalmond> |- ' + value + '</blanchedalmond>'))


def show_time_type(key, value):
    year, month, day, hour, minute, second = _decode_time_string(value)
    fprint(H('<cornflowerblue>' + key + '</cornflowerblue>' + ": " + "<b>" + day + ' ' + hour + ' ' + minute + "</b>"))


def show_data_detail(json_dict):
    if json_dict['version'] == '0.3':
        for k, v in json_dict['data'].items():
            if 'passion' in k or 'feedback' in k:
                show_choice_type(k, v)
            elif 'start_time' in k or 'end_time' in k:
                show_time_type(k, v)
            elif 'info' == k or 'steps' in k:
                show_list_description_type(k, v)
            else:
                show_description_type(k, v)


def get_choice_type(key, default_value):
    choice = prompt(
        H('<orange>' + key + '</orange>' + ": "),
        completer=completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default=default_value
    )
    return choice


def get_description_type(key, default_value):
    description = prompt(
        H('<aqua>' + key + '</aqua>' + ": "),
        completer=completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default=default_value
    )
    return description


def get_list_description_type(key, default_value_list):
    fprint(H('<coral>' + key + '</coral>'))
    text = 'None'
    data = []
    count = 0
    while text and '##' not in text:
        text = prompt(
            H('<blanchedalmond> |- ' + '</blanchedalmond>'),
            completer=completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
            default=default_value_list[count] if count < len(default_value_list) else ''
        )
        count += 1
        if text:
            data.append(text.replace('##', ''))

    return data


def get_time_type(key, default_value):
    time_ = prompt(
        H('<orange>' + key + '</orange>' + ": "),
        completer=completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default=default_value
    )
    return time_


def get_related_name():
    name = prompt(
        H('<lime>' + 'related name' + '</lime>' + ": "),
        completer=completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default=''
    )
    return name


def submit():
    block_type = None
    while block_type not in ['r', 'a', 'd']:
        block_type = prompt(
            "choose type in d / a / r: ",
            completer=completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
        )
        block_type = block_type.lower()

    if block_type == 'd':
        fm = FileManager()
        name = str(max([int(_) for _ in fm.META['name_list']] + [0]) + 1)
        title = get_description_type('title', "a program title")
        info = get_list_description_type('info', 'some information')
        add(
            data_dict={"title": title, "info": info},
            name=name,
            type_='document',
            version='0.3',
            show_flag_list='on',
            related_names=[]
        )

    if block_type == 'a':
        fm = FileManager()
        name = str(max([int(_) for _ in fm.META['name_list']] + [0]) + 1)
        goal = get_description_type('goal', "a detailed goal")
        steps = get_list_description_type('steps', ['step -> result'])
        related_name = get_related_name()
        add(
            data_dict={"goal": goal, "steps": steps},
            name=name,
            type_='action',
            version='0.3',
            show_flag_list='on',
            related_names=[related_name]
        )

    if block_type == 'r':
        fm = FileManager()
        name = str(max([int(_) for _ in fm.META['name_list']] + [0]) + 1)
        start_time = get_time_type('start_time', get_time_string_now())
        end_time = get_time_type('end_time', get_time_string_now())
        start_passion = get_choice_type('start_passion', 'good')
        end_feedback = get_choice_type('send_feedback', 'good')
        environment = get_description_type('environment', '实验室')
        add_info = get_description_type('add_info', '精神状态良好')

        related_name = get_related_name()
        add(
            data_dict={"start_time": start_time, "end_time": end_time, "start_passion": start_passion,
                       "end_feedback": end_feedback, "environment": environment, "add_info": add_info},
            name=name,
            type_='record',
            version='0.3',
            show_flag_list='on',
            related_names=[related_name]
        )


def modify():
    modify_id = prompt(
        "choose modify block id: ",
        completer=completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
    )

    json_dict = get(name=modify_id)
    # all_keys = ['name', 'data', 'submit_time', 'last_overwrite_time', 'show_flag', 'version', 'type']
    print('----------------------origi-----------------------')
    show_data_detail(json_dict)

    fprint(H('<red>--------------------overwrite------------------------</red>'))
    new_dict = json_dict['data']
    for k, v in json_dict['data'].items():
        if 'passion' in k or 'feedback' in k:
            new_dict[k] = get_choice_type(k, v)
        elif 'start_time' in k or 'end_time' in k:
            new_dict[k] = get_time_type(k, v)
        elif 'info' == k or 'steps' in k:
            new_dict[k] = get_list_description_type(k, v)
        else:
            new_dict[k] = get_description_type(k, v)

    overwrite_data(new_dict, modify_id)


def show_all():
    fm = FileManager()
    document_indexs = [index for index, type_ in enumerate(fm.META['type_list']) if type_ == 'document' and
                       fm.META['show_flag_list'][index] == 'on']
    for doc_index in document_indexs:
        fprint(H('<white>------------------------------------------------------------------------------------</white>'))
        d_name = fm.META['name_list'][doc_index]
        temp = '|' + '<style fg="ansiwhite" bg="ansiblue">D[' + d_name + ']</style> ' + \
               '<b>' + fm.DATA[d_name]['title'] + '</b>'
        fprint(H(temp))
        for action_index, connect in enumerate(fm.META["adjacency_matrix"][doc_index]):
            if connect and fm.META['type_list'][action_index] == 'action':
                time_ = 0
                to_print = []
                for record_index, connect_ in enumerate(fm.META["adjacency_matrix"][action_index]):
                    if connect_ and fm.META['type_list'][record_index] == 'record':
                        time_ += calculate_time(
                            fm.DATA[fm.META['name_list'][record_index]]['start_time'],
                            fm.DATA[fm.META['name_list'][record_index]]['end_time'],
                        )
                        year, month, day, hour, minute, second = _decode_time_string(
                            fm.DATA[fm.META['name_list'][record_index]]['start_time'])
                        temp = '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + \
                               fm.META['name_list'][record_index] + ']</style> <u>' + \
                               str(calculate_time(
                                   fm.DATA[fm.META['name_list'][record_index]]['start_time'],
                                   fm.DATA[fm.META['name_list'][record_index]]['end_time'],
                               )) + ' min</u> ' + "<b>" + day + 'day ' + hour + 'hour ' + minute + "min</b>"
                        to_print.append(temp)
                temp = '|--|' + '<style fg="ansiwhite" bg="ansiyellow">A[' + fm.META['name_list'][action_index] + \
                       ']</style> ' + "<u>{} min</u> ".format(time_) + '<b>' + fm.DATA[fm.META['name_list'][action_index]]['goal'] + '</b>'
                fprint(H(temp))
                for print_r in to_print:
                    fprint(H(print_r))


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
                          'you can input: [backup now] to backup \n -> ')
            if check == 'backup now':
                if len(os.listdir(save_path)) == 0:
                    for file in os.listdir(MAIN_WORK_DIR):
                        shutil.copy(os.path.join(MAIN_WORK_DIR, file), save_path)
                    print('Successfully backup data at --> {}'.format(save_path))
                else:
                    print('des dir is not a blank dir')


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
                        'you can input: [load and overwrite now] to load backup \n -> ')
            if out == 'load and overwrite now':
                flag = 0
                for file in os.listdir(load_path):
                    if file in [META, DATA]:
                        flag += 1

                if flag == 2:
                    for file in os.listdir(load_path):
                        if file in [META, DATA]:
                            shutil.copy(os.path.join(load_path, file), os.path.join(MAIN_WORK_DIR, file))
                    print('Successfully load data from --> {}'.format(load_path))
                else:
                    print('Incomplete files in dir: {}'.format(load_path))

