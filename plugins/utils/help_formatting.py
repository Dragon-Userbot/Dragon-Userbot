import re
from .utils import prefix


def help_formatting(module_help, help_type, module_name):
    if help_type == 'all_mods':
        ready_string = f"• <b>{module_help.split(':')[0].strip()}: </b> <code>{module_help.split(':')[1].strip()}</code>\n"
        return ready_string
    elif help_type == 'one_mod':
        s = f'<b>Help for |{module_name}|\nUsage:</b>\n'
        try:
            for i in module_help.split(','):
                command = i.split('-')[0]
                command = re.sub(r"^\s+|\s+$", "", command)
                description = i.split('-')[1]
                description = re.sub(r"^\s+|\s+$", "", description)
                s += f'<code>{prefix}{command}</code>\n<b>[{description}]</b>\n'
            return s
        except IndexError:
            return module_help