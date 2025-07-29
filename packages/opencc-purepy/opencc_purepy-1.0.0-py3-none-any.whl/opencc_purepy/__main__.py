from __future__ import print_function

import argparse
import sys
from . import dictgen_cmd
from . import convert_cmd  # We'll move your current logic into convert_cmd.py

def main():
    parser = argparse.ArgumentParser(
        prog='opencc_purepy',
        description='OpenCC CLI with multiple tools',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # ---- convert subcommand ----
    parser_convert = subparsers.add_parser('convert', help='Convert text using OpenCC')
    parser_convert.add_argument('-i', '--input', metavar='<file>', help='Input file')
    parser_convert.add_argument('-o', '--output', metavar='<file>', help='Output file')
    parser_convert.add_argument('-c', '--config', metavar='<conversion>', help='Conversion configuration')
    parser_convert.add_argument('-p', '--punct', action='store_true', default=False, help='Punctuation conversion: True/False')
    parser_convert.add_argument('--in-enc', metavar='<encoding>', default='UTF-8', help='Input encoding')
    parser_convert.add_argument('--out-enc', metavar='<encoding>', default='UTF-8', help='Output encoding')
    parser_convert.set_defaults(func=convert_cmd.main)

    # ---- dictgen subcommand ----
    parser_dictgen = subparsers.add_parser('dictgen', help='Generate dictionary')
    parser_dictgen.add_argument(
        "-f", "--format",
        choices=["json"],
        default="json",
        help="Dictionary format: [json]"
    )
    parser_dictgen.add_argument(
        "-o", "--output",
        metavar="<filename>",
        help="Write generated dictionary to <filename>. If not specified, a default filename is used."
    )
    parser_dictgen.set_defaults(func=dictgen_cmd.main)

    args = parser.parse_args()
    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
