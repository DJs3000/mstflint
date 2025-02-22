# Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software is available to you under a choice of one of two
# licenses.  You may choose to be licensed under the terms of the GNU
# General Public License (GPL) Version 2, available from the file
# COPYING in the main directory of this source tree, or the
# OpenIB.org BSD license below:
#
#     Redistribution and use in source and binary forms, with or
#     without modification, are permitted provided that the following
#     conditions are met:
#
#      - Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      - Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials
#        provided with the distribution.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


#######################################################
#
# resourceparse.py
# Python implementation of the Class ResourceParse
# Generated by Enterprise Architect
# Created on:      16-Dec-2019 14:11:58 AM
# Original author: talve
#
#######################################################
import tools_version
import sys
import os

if sys.version_info[0] < 3:
    print("Error: This tool supports python 3.x only. Exiting...")
    exit(1)

import argparse
from resourceparse_lib.utils import constants as cs
from resourceparse_lib.utils.common_functions import valid_path_arg_type
from resourceparse_lib.ResourceParseManager import ResourceParseManager
from resourceparse_lib.utils.Exceptions import ResourceParseException
from resourceparse_lib.parsers.ResourceParser import PARSER_CLASSES, parser_type

sys.path.append(os.path.join("common"))


class ResourceParse:
    """This class is responsible for the resource dump UI by handling the user inputs and
       and running the right command.
    """

    _arg_parser = None
    _common_usage = None
    _common_help = None

    @classmethod
    def _init_arg_parser(cls, prog=None):
        tool_name = prog if prog else os.path.basename(__file__).split('.')[0]

        description = \
            """Description:
    This tool parses and formats the output of "resourcedump" tool.
    There are several methods of parsing (see --parser).
""" if not prog else None

        cls._arg_parser = argparse.ArgumentParser(prog=tool_name, description=description, add_help=False)

        required_args = cls._arg_parser.add_argument_group('required arguments')
        optional_args = cls._arg_parser.add_argument_group('optional arguments')
        optional_args.add_argument("-p", "--parser", dest="resource_parser", type=parser_type, nargs="?", const=PARSER_CLASSES["adb"], default=PARSER_CLASSES["adb"] if not prog else PARSER_CLASSES["raw"], help="Available options: {}. Default: 'adb'. see (Parsing methods) ".format(list(PARSER_CLASSES.keys())))
        optional_args.add_argument("-o", "--out", help='Location of the output file')

        # Only args that added up until here will be included in the resourcedump help menu

        cls._common_usage = cls._arg_parser.format_usage().rstrip() + " [PARSE_METHOD_ARGUMENTS]\n"

        parse_methods_help = "Parse Methods:\n    The parse method can be chosen by the common --parser option. Below the description of each parse method and its arguments.\n\n"
        parse_methods_help += "\n".join(['Parse Method - "{}":\n'.format(parser_name) + parser_class.get_arg_parser(cls._arg_parser.prog).format_help() for parser_name, parser_class in PARSER_CLASSES.items()])

        cls._common_help = "\n".join(cls._arg_parser.format_help().split("\n")[1:]) + "\n" + parse_methods_help

        input_named = required_args.add_mutually_exclusive_group(required=True)
        input_named.add_argument("-d", "--dump-file", type=valid_path_arg_type, help='Location of the dump file used for parsing')
        input_named.add_argument("--segments_provided", action="store_true", help=argparse.SUPPRESS)

        optional_args.add_argument('--version', action='version', help="Shows the tool's version and exit", version=tools_version.GetVersionString(tool_name, None))
        optional_args.add_argument("-v", help='Verbosity notice', dest="verbose", default=0, action='count')
        optional_args.add_argument("-h", "--help", action="help", help="show this help message and exit")

        standalone_usage = cls._arg_parser.format_usage().rstrip() + " [PARSE_METHOD_ARGUMENTS]\n"
        standalone_help_body = "\n".join(cls._arg_parser.format_help().split("\n")[1:]) + "\n" + parse_methods_help
        standalone_help = standalone_usage + standalone_help_body

        cls._arg_parser.format_help = lambda: standalone_help

    @classmethod
    def get_help(cls, prog):
        if not cls._arg_parser:
            cls._init_arg_parser(prog)
        return cls._common_help, cls._common_usage

    @classmethod
    def run_arg_parse(cls, argv=None, prog=None):
        """This method run the arg parse and return the arguments from the UI.
        """
        if not cls._arg_parser:
            cls._init_arg_parser(prog)

        manager_args, remaining = cls._arg_parser.parse_known_args(argv)
        parsing_method_arg_parser = manager_args.resource_parser.get_arg_parser(cls._arg_parser.prog)

        parser_args = parsing_method_arg_parser.parse_args(remaining) if parsing_method_arg_parser else argparse.Namespace

        return manager_args, parser_args

    def run(self, argv=None, segments=None):
        """This method run the parser with the needed arguments
        """
        manager_args, parser_args = self.run_arg_parse(argv)
        creator = ResourceParseManager(manager_args, parser_args, segments)
        creator.parse()


if __name__ == '__main__':
    try:
        ResourceParse().run()
    except ResourceParseException as rpe:
        print("ResourceParse failed!\n{0}.\nExiting...".format(rpe))
        sys.exit(1)
    except Exception as e:
        print("FATAL ERROR!\n{0}.\nExiting...".format(e))
        sys.exit(1)
