"""
实现交互输入过程
prompt实现block的提交
用ptpython实现block显示面板，只读
"""
from core.DataStructure import *
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit import print_formatted_text as fprint
from prompt_toolkit import HTML as H


apis = [
    'create',
    'show_all',
    'modify',
    'show'
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
    for k, v in block.__dict__.items():
        re = prompt(
            "{}: ".format(k),
            completer=block_completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
            default=v if isinstance(v, str) else str(v)
        )
        json_dict[k] = re if 'score' not in k else int(re)

    print('----------------------------------{}----------------------------------'.format(block_type.upper()))
    for k, v in json_dict.items():
        if 'file' in k:
            print(k, ":")
            for vv in decoder_file_string(v):
                print('  //->', vv)
        else:
            print(k + ":", v)
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
    out_keys = ['block_type', 'block_id', 'submit_time', 'last_overwrite_time']
    json_dict = {k: v for k, v in json_dict.items() if k not in out_keys}

    print('----------------------------------{}----------------------------------'.format(block_type))
    for k, v in json_dict.items():
        if 'file' in k:
            print(k, ":")
            for vv in decoder_file_string(v):
                print('  //->', vv)
        else:
            print(k + ":", v)
    print('')

    new_json_dict = {}
    for k, v in json_dict.items():
        re = prompt(
            "{}: ".format(k),
            completer=block_completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
            default=v if isinstance(v, str) else str(v)
        )
        new_json_dict[k] = re if 'score' not in k else int(re)

    print('----------------------------------{}----------------------------------'.format(block_type.upper()))
    for k, v in new_json_dict.items():
        if 'file' in k:
            print(k, ":")
            for vv in decoder_file_string(v):
                print('  //->', vv)
        else:
            print(k + ":", v)
    print('')

    y_or_n = prompt(
        "if you want to modify: yes or no: ",
        completer=block_completer,
        complete_style=CompleteStyle.MULTI_COLUMN,
        default='yes'
    )

    if y_or_n.lower() == 'yes' or y_or_n.lower() == 'y':
        overwrite_block(block_type=block_type, block_id=modify_id, json_dict=new_json_dict)


def show_all():
    fm = FileManager()
    document_ids = fm.FILE_META['submit_type_id_statistic']['DOCUMENT']
    for document_id in document_ids:
        fprint(H('<b>---------------------------------------------------------------------------------------</b>'))
        temp = '|' + '<style fg="ansiwhite" bg="ansiblue">D[' + document_id + ']</style> ' + fm.FILE_BLOCK_DATA[document_id]['doc_outline']
        fprint(H(temp))
        index = fm.FILE_DATA_ID_LIST['id_list'].index(document_id)

        for block_index, connect in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][index]):
            if connect and block_index != 0:
                temp = '|--|' + '<style fg="ansiwhite" bg="ansiyellow">A[' + fm.FILE_DATA_ID_LIST['id_list'][block_index] + ']</style> ' + \
                      fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['goal']
                fprint(H(temp))

                for block_index_, connect_ in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][block_index]):
                    if connect_ and block_index_ != block_index and block_index_ != index:
                        temp = '|-----|' + '<style fg="ansiwhite" bg="ansigreen">R[' + fm.FILE_DATA_ID_LIST['id_list'][block_index_] + ']</style> ' + \
                              str(calculate_time(
                                  fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time'],
                                  fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['end_time']
                              )) + ' minutes ' + \
                              fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time']
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
                fprint(H('  //->' + "<b>" + vv + "</b>"))
        else:
            v = v if isinstance(v, str) else str(v)
            fprint(H('<style fg="ansiwhite" bg="ansicyan">' + k + '</style>' + ": " + "<b>" + v + "</b>"))
    print('')
