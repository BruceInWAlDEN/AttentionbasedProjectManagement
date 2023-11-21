# -*- coding:utf-8 -*-
"""
file
    data_relation_matrix.json
    data_name_list.json
    block_data.json
    meta.json

class
    BasicBlock
    DOCUMENT
    ACTION
    RECORD
    BasicFile
    BasicTime

def
    get_block(type, id, name, year, month, day)
    overwrite_block(type, id, json_dict)
    write_record(json_dict, document_id, action_id)
    write_action(json_dict, document_id)
    write_document(json_dict)
    delete_block(type, id)
    delete_block_on_device(type, id)
"""