import json
import yaml
import os

from jsonpath_rw import jsonpath, parse
from yay import YayException

def get_json_path(data, path):
    if not path:
        return data

    jsonpath_expr = parse(path)
    part = [match.value for match in jsonpath_expr.find(data)]
    if len(part) == 0:
        return None
    if len(part) == 1:
        part = part[0]
    return part

def format_json(dict):
    return json.dumps(dict, indent=2, sort_keys=True)

def print_as_json(dict):
    print(format_json(dict))

def format_yaml(dict):
    return yaml.dump(dict, default_flow_style=False)

def print_as_yaml(dict):
    print(format_yaml(dict))

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def read_yaml_file(fileArgument, data = []):
    with open(fileArgument, 'r') as stream:
        for fileData in yaml.load_all(stream):
            data.append(fileData)
    return data

def add_from_yaml_file(fileArgument, data):
    if not os.path.isfile(fileArgument):
        return

    with open(fileArgument, 'r') as stream:
        for fileData in yaml.load_all(stream):
            data.update(fileData)

    return data

def read_yaml_files(fileArgument, data = []):

    if os.path.isdir(fileArgument):
        for root, subdirs, files in os.walk(fileArgument):
            for file in files:
                if file.endswith('.yaml'):
                    read_yaml_file(format(os.path.join(root, file)), data)
    else:
        # Read all items from one file
        read_yaml_file(fileArgument, data)

    return data

def is_dict(item):
    return type(item) is dict

def is_list(item):
    return isinstance(item, list)

def is_scalar(item):
    return type(item) is str

def is_empty(item):
    if item is None: return True
    if is_scalar(item):
        if not item: return False
    return True

def as_list(item):
    if not is_list(item):
        return [item]
    return item

def get_parameter(data, name, default = None):
    parameter = data.get(name)
    if parameter is None:
        parameter = default
    if parameter is None:
        raise YayException("Missing parameter '{}' in:\n{}".format(name, yaml.dump(data, default_flow_style=False)))
    return parameter

class AnyContent():
    def __str__(self):
        return "!any"
    def __eq__(self, other):
        return True
    def __ne__(self, other):
        return False


def yaml_any_content(loader, node):
    return AnyContent()

yaml.add_constructor('!any', yaml_any_content)