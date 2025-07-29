from .dictionary_lib import DictionaryMaxlength

BLUE = "\033[1;34m"
RESET = "\033[0m"

def main(args):
    default_output = {
        "json": "dictionary_maxlength.json"
    }[args.format]

    output_file = args.output or default_output
    dictionaries = DictionaryMaxlength.from_dicts()

    if args.format == "json":
        dictionaries.serialize_to_json(output_file)
        print(f"{BLUE}Dictionary saved in JSON format at: {output_file}{RESET}")

    return 0
