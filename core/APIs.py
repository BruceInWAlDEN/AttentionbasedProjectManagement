# -*- coding:utf-8 -*-
from core.DataStructure import *

"""
a test version of APIs
"""


def get_template(block_type=None):
    if block_type == 'R':
        block_type = 'RECORD'
    if block_type == 'A':
        block_type = 'ACTION'
    if block_type == 'D':
        block_type = 'DOCUMENT'

    if block_type in ['RECORD', 'ACTION', 'DOCUMENT']:
        block = eval(block_type + "()")
        template = block.get_template()

        return template
    
    else:
        print('wrong block type: ', block_type)


def show_relation_tree():
    fm = FileManager()
    document_ids = fm.FILE_META['submit_type_id_statistic']['DOCUMENT']
    for document_id in document_ids:
        print('---------------------------------------------------------------------------------------')
        print('|', 'D[' + document_id + ']', fm.FILE_BLOCK_DATA[document_id]['doc_outline'])
        index = fm.FILE_DATA_ID_LIST['id_list'].index(document_id)
        for block_index, connect in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][index]):
            if connect and block_index != 0:
                print('|--|', 'A[' + fm.FILE_DATA_ID_LIST['id_list'][block_index] + ']',
                      fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index]]['goal'])
                for block_index_, connect_ in enumerate(fm.FILE_DATA_RELATION_MATRIX["relation_matrix"][block_index]):
                    if connect_ and block_index_ != block_index and block_index_ != index:
                        print('|-----|', 'R[' + fm.FILE_DATA_ID_LIST['id_list'][block_index_] + ']',
                              calculate_time(
                                  fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time'],
                                  fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['end_time']
                              ), 'minutes',
                              fm.FILE_BLOCK_DATA[fm.FILE_DATA_ID_LIST['id_list'][block_index_]]['start_time']
                              )


def show_content(key: str = '', block_type=None, block_id=None, year=None, month=None, day=None):
    if block_type == 'R':
        block_type = 'RECORD'
    if block_type == 'A':
        block_type = 'ACTION'
    if block_type == 'D':
        block_type = 'DOCUMENT'

    if key:
        if key[0] == 'i':
            block_id = key[1:]
        if key[0] == 't':
            if key[1:] == 'R':
                block_type = 'RECORD'
            if key[1:] == 'A':
                block_type = 'ACTION'
            if key[1:] == 'D':
                block_type = 'DOCUMENT'

    json_dicts = get_block(block_type, block_id, year, month, day)

    for json_dict in json_dicts:
        print('----------------------------------{}----------------------------------'.format(json_dict['block_type']))
        for k, v in json_dict.items():
            if 'file' in k:
                print(k, ":")
                for vv in decoder_file_string(v):
                    print('  //->', vv)
            else:
                print(k + ":", v)
        print('')


def get_file_strings(*file_strings):
    file_list = []
    for file_string in file_strings:
        if "https:/" in file_string or 'http:/' in file_string:
            file_list.append(get_file_string('url', file_string))
        elif "C:\\" in file_string:
            file_list.append(get_file_string('file_full_path', file_string))
        else:
            file_list.append(get_file_string('description', file_string))

    return get_file_string_list(file_list)


def create(block_type=None, json_dict=None, document_id=None, action_id=None):
    if block_type == 'R' or block_type == 'RECORD':
        write_record(json_dict, document_id, action_id)
    if block_type == 'A' or block_type == 'ACTION':
        write_action(json_dict, document_id)
    if block_type == 'D' or block_type == 'DOCUMENT':
        write_document(json_dict)


def get_content(key: str = '', block_type=None, block_id=None, year=None, month=None, day=None):
    if block_type == 'R':
        block_type = 'RECORD'
    if block_type == 'A':
        block_type = 'ACTION'
    if block_type == 'D':
        block_type = 'DOCUMENT'

    if key:
        if key[0] == 'i':
            block_id = key[1:]
        if key[0] == 't':
            if key[1:] == 'R':
                block_type = 'RECORD'
            if key[1:] == 'A':
                block_type = 'ACTION'
            if key[1:] == 'D':
                block_type = 'DOCUMENT'

    json_dicts = get_block(block_type, block_id, year, month, day)
    out_keys = ['block_type', 'block_id', 'submit_time', 'last_overwrite_time']
    json_dicts = [{k: v for k, v in _.items() if k not in out_keys} for _ in json_dicts]

    return json_dicts


def overwrite(key: str = '', block_type=None, json_dict=None, block_id=None):
    if key:
        block_type = key[0].upper()
        block_id = key[1:]
    if block_type == 'R':
        block_type = 'RECORD'
    if block_type == 'A':
        block_type = 'ACTION'
    if block_type == 'D':
        block_type = 'DOCUMENT'

    overwrite_block(block_type, json_dict, block_id)

