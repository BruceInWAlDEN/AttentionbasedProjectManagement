# -*- coding:utf-8 -*-
"""
use only methods in core. APIs
here is an example to process by cmd python command
"""
from core.APIs import *


if __name__ == "__main__":
    get_template("D")
    get_template("R")
    get_template("A")
    # submit("D", {
    #     "doc_outline": "a program for attetnionbasedProjectManagement project",
    #     "doc_file": "||file_full_path-->init||url-->init||description-->init||",
    # })
    # show_relation_tree()
    # submit("A", {
    #     "goal": "a result",
    #     "methods": "detailed",
    #     "feedback": "statement but feeling",
    #     "related_file": "||file_full_path-->init||url-->init||description-->init||",
    # }, document_id="1")
    # show_relation_tree()
    # submit("R", {
    #     "start_time": "year:2023||month:11||day:22||hour:17||minute:2||second:35",
    #     "end_time": "year:2023||month:11||day:22||hour:17||minute:2||second:35",
    #     "start_passion_score": 5,
    #     "end_feeling_score": 5,
    #     "attention_score": 5,
    #     "passion_description": "feeling and reason",
    #     "feeling_description": "feeling and reason",
    #     "attention_description": "feeling and reason",
    #     "work_env_description": "objective",
    # }, action_id="2")
    # show_relation_tree()
    # submit("R", {
    #     "start_time": "year:2023||month:11||day:22||hour:17||minute:2||second:35",
    #     "end_time": "year:2023||month:11||day:22||hour:17||minute:2||second:35",
    #     "start_passion_score": 5,
    #     "end_feeling_score": 5,
    #     "attention_score": 5,
    #     "passion_description": "feeling and reason",
    #     "feeling_description": "feeling and reason",
    #     "attention_description": "feeling and reason",
    #     "work_env_description": "objective",
    # }, document_id="1")
    show_content()


