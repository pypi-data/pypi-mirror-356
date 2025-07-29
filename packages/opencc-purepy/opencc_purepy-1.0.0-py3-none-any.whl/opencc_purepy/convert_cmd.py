import io
import sys
from opencc_purepy import OpenCC

def main(args):
    if args.config is None:
        print("Please specify conversion.", file=sys.stderr)
        return 1

    opencc = OpenCC(args.config)

    # Prompt only if reading from stdin, and it's interactive (i.e., not piped or redirected)
    if args.input is None and sys.stdin.isatty():
        print("Input text to convert, <Ctrl+Z> (Windows) or <Ctrl+D> (Unix) then Enter to submit:", file=sys.stderr)

    with io.open(args.input if args.input else 0, encoding=args.in_enc) as f:
        input_str = f.read()
    output_str = opencc.convert(input_str, args.punct)

    with io.open(args.output if args.output else 1, 'w', encoding=args.out_enc) as f:
        f.write(output_str)

    in_from = args.input if args.input else "<stdin>"
    out_to = args.output if args.output else "stdout"
    if sys.stderr.isatty():
        print(f"Conversion completed ({args.config}): {in_from} -> {out_to}", file=sys.stderr)

    return 0
