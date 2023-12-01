# -*- coding:utf-8 -*-
from CLI.cli_apis import *
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import print_formatted_text as fprint
from prompt_toolkit import HTML as H


if __name__ == "__main__":
    fprint(H('\n<i>Welcome to attention based project management system !</i>'))
    fprint(H('<i>** remember to be a productive person ! **</i>\n\n'))
    command_completer = WordCompleter(apis, ignore_case=True)
    while True:
        command = prompt(
            "Bruce@APM>>",
            completer=command_completer,
            complete_style=CompleteStyle.MULTI_COLUMN,
        )
        if command in apis:
            try:
                eval(command + '()')
            except KeyboardInterrupt:
                pass
