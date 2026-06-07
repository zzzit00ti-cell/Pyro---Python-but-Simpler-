import argparse
import sys
import subprocess
from pathlib import Path
from .compiler import compile_file

def main():
    parser = argparse.ArgumentParser(description="Pyro compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="Compile .pyro to .py")
    compile_parser.add_argument("input", help=".pyro source file")
    compile_parser.add_argument("-o", "--output", help="output .py file")
    compile_parser.add_argument("--fast", action="store_true", help="Enable Mojo-like performance optimizations mapped to numba/functools")
    compile_parser.add_argument("--target", choices=["py", "js", "mcu"], default="py", help="Compilation target platform")

    run_parser = subparsers.add_parser("run", help="Compile and run")
    run_parser.add_argument("input", help=".pyro source file")

    args = parser.parse_args()

    if args.command == "compile":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: file {input_path} not found", file=sys.stderr)
            sys.exit(1)
        output_path = args.output if args.output else input_path.with_suffix(".py")
        try:
            compile_file(input_path, output_path, fast_mode=args.fast)
            if args.target == "js":
                print(f"✨ Compiled {input_path} -> {output_path} ✨")
                print("💡 RapydScript/Brython Target: Ready for Transcrypt!")
                print(f"   Run: python -m transcrypt -b -m -n {output_path}")
            elif args.target == "mcu":
                print(f"✨ Compiled {input_path} -> {output_path} ✨")
                print("💡 MicroPython Target: Ready for MCU flashing!")
                print(f"   Run: mpremote cp {output_path} :main.py")
            else:
                print(f"Compiled {input_path} -> {output_path}")
        except SyntaxError as e:
            print(f"SyntaxError: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "run":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: file {input_path} not found", file=sys.stderr)
            sys.exit(1)
        try:
            py_code = compile_file(input_path, None)
            # Execute with a shared namespace so recursive functions work
            exec_globals = {"__builtins__": __builtins__}
            exec(py_code, exec_globals)
        except SyntaxError as e:
            print(f"SyntaxError: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
