#!/usr/bin/env python3
import sys
import os

# Register handlers
from yay import core
from yay import http
from yay import files
from yay import script
from yay import input
from yay import xl_cli

from yay.util import *

def main():

    variables = {}

    # Load default variables
    defaultValuesFile = os.path.join(os.path.expanduser('~'), '.yay/default-variables.yaml')
    add_from_yaml_file(defaultValuesFile, variables)

    try:
        # Make sure we can find the file
        filename = get_file(sys.argv[1])

        # Parse arguments into values
        for argument in sys.argv[2:]:
            key, value = argument.split('=')
            variables[key] = value

        # Read YAML script
        tasks = read_yaml_files(filename)

        # Process all
        result = core.process_tasks(tasks, variables)

    except Exception as exception:
        # import traceback
        # traceback.print_exc()
        print(exception)


def get_file(filename):
    if os.path.isfile(filename):
        return filename

    yayFile = filename + ".yay"
    if os.path.isfile(yayFile):
        return yayFile

    yamlFile = filename + ".yaml"
    if os.path.isfile(yamlFile):
        return yamlFile

    raise YayException(f"Could not find file: {filename}")


# Execute script
if __name__ == '__main__':
    main()
