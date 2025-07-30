from . import kbp
from . import doblontxt
from . import lrc
from . import converters
from . import __version__
import argparse
import dataclasses
import io
import os
import sys
import collections
import traceback

# Shows a usage message for the main command and all subcommands.
# Requires an attribute added_subparsers since ArgumentParser normally
# doesn't provide an API for retrieving them and would require something
# unreliable like this:
# added_subparsers = parser._subparsers._name_parser_map.values()
class _UsageAllAction(argparse.Action):
    def __init__(self,
         option_strings,
         dest=argparse.SUPPRESS,
         default=argparse.SUPPRESS,
         help=None,
         deprecated=False):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help,
            deprecated=deprecated)

    def __call__(self, parser, namespace, values, option_string=None):
        print(parser.format_usage())
        for p in parser.added_subparsers:
            print(p.format_usage())
        parser.exit()

@dataclasses.dataclass
class KBPInputOptions:
    tolerant_parsing: bool = dataclasses.field(default=False, metadata={'doc': "Automatically fix syntax errors in .kbp file if they have an unambiguous interpretation"})

@dataclasses.dataclass
class KBPCheckOptions:
    suggestions: bool = dataclasses.field(default=False, metadata={'doc': "Provide suggestions for fixing problems"})
    interactive: bool = dataclasses.field(default=False, metadata={'doc': "Start an interactive session to fix problems"})
    overwrite: bool = dataclasses.field(default=False, metadata={'doc': "Allow in-place overwriting of file in interactive mode. Not recommended!"})

def kbpcheck(source, args, dest):
    suggest = getattr(args, "suggestions", False)
    interact = getattr(args, "interactive", False)
    overwrite = getattr(args, "overwrite", False)
    if interact:
        # In interactive mode, prompts should be to stdout, but dest can be used for the file to write
        (output, dest) = (dest, sys.stdout)
    else:
        if dest and os.path.exists(dest) and os.path.samefile(dest, source.filename):
            sys.stderr.write("Not writing over kbp file! Leave destination argument blank or provide a suitable output file.\n")
            sys.exit(1)
        dest = open(dest, 'w') if dest else sys.stdout
    for fix in source.onload_modifications:
        dest.write(fix + "\n")
        if suggest or interact:
            dest.write(" - Fixed automatically by tolerant parsing option\n\n")
    for err in (errs := source.logicallyValidate()):
        dest.write(str(err) + "\n")
        if suggest or interact:
            solutions = err.propose_solutions(source)
            dest.write("Solutions:\n")
            dest.write("\n".join(f"  {n}) " + x.params["description"] for n, x in enumerate(solutions, 1)) + "\n")
        if interact:
            print(f"  {len(solutions)+1}) Take no action")
            print(f"  w) Save to {output or '<stdout>'} or specified filename and exit without resolving remaining errors")
            print("  x) Exit without saving")
            while True:
                choice = input(f"[{len(solutions)+1}]: ") or str(len(solutions)+1)
                if choice == 'x':
                    sys.exit(0)
                elif choice == 'w' or choice.startswith('w '):
                    fname = choice[2:] or output or sys.stdout
                    try:
                        source.writeFile(fname, allow_overwrite=overwrite)
                    except Exception:
                        print(traceback.format_exc())
                        print("Sorry, try another filename")
                        continue
                    sys.exit(0)
                else:
                    try:
                        i = int(choice) - 1
                        assert 0 <= i < len(solutions)+1
                    except Exception:
                        print(f"Please enter a number between 1 and {len(solutions)+1}, w [filename], x, or hit enter for the default (no action).")
                        continue
                    if i < len(solutions):
                        for param in solutions[i].free_params:
                            param_data = solutions[i].free_params[param]
                            print(f"Choose {param} to use")
                            for choice, desc in param_data:
                                print(f"  {choice}) {desc}")
                            default_choice = param_data[0][0]
                            while True:
                                try:
                                    choice = type(param_data[0][0])(input(f"[{default_choice}]: ")) or default_choice
                                    assert choice in (x for x,_ in param_data)
                                    solutions[i].params[param] = choice
                                    break
                                except Exception:
                                    print("Please choose one of the provided options")
                        if solutions[i].free_params:
                            solutions[i].free_params.clear()
                        solutions[i].run(source)

                    break
        dest.write("\n")
    if interact:
        print(f"\nDone editing file!\n")
        print(f"  w) Save to {output or '<stdout>'} or specified filename")
        print("  x) Exit without saving")
        while True:
            choice = input(f"[w]: ") or "w"
            if choice == 'x':
                sys.exit(0)
            elif choice == 'w' or choice.startswith('w '):
                fname = choice[2:] or output or sys.stdout
                try:
                    source.writeFile(fname)
                except Exception:
                    print(traceback.format_exc())
                    print("Sorry, try another filename")
                    continue
                sys.exit(0)
                
    dest.close()
    sys.exit(min(len(errs) + len(source.onload_modifications), 255))

def convert_file():
    parser = argparse.ArgumentParser(
            prog='KBPUtils',
            description="Various utilities for .kbp files",
            epilog=f"Each utility has its own help, e.g. KBPUtils kbp2ass --help",
            argument_default=argparse.SUPPRESS,
        )

    parser_data = {
        'kbp2ass': {
            'add_parser': {
                'description': 'Convert .kbp to .ass file',
                'argument_default': argparse.SUPPRESS
            },
            'input': kbp.KBPFile,
            'input_options': KBPInputOptions,
            'output': lambda source, args, dest: converters.AssConverter(source, **vars(args)).ass_document().dump_file(dest),
            'output_opts': {
                'encoding': 'utf_8_sig'
            },
            'options': converters.AssOptions
        },
        'doblontxt2kbp': {
            'add_parser': {
                'description': 'Convert Doblon full timing .txt file to .kbp',
                'argument_default': argparse.SUPPRESS
            },
            'input': doblontxt.DoblonTxt,
            'output': lambda source, args, dest: converters.DoblonTxtConverter(source, **vars(args)).kbpFile().writeFile(dest),
            'output_opts': {
                'encoding': 'utf-8',
                'newline': '\r\n'
            },
            'options': converters.DoblonTxtOptions
        },
        'lrc2kbp': {
            'add_parser': {
                'description': 'Convert Enhanced .lrc to .kbp',
                'argument_default': argparse.SUPPRESS
            },
            'input': lrc.LRC,
            'output': lambda source, args, dest: converters.LRCConverter(source, **vars(args)).kbpFile().writeFile(dest),
            'output_opts': {
                'encoding': 'utf-8',
                'newline': '\r\n'
            },
            'options': converters.LRCOptions
        },
        'kbpcheck': {
            'add_parser': {
                'description': 'Discover logic errors in kbp files',
                'argument_default': argparse.SUPPRESS
            },
            'input': kbp.KBPFile,
            'input_options': KBPInputOptions,
            'output': kbpcheck,
            'output_opts': None, # needs the filename instead of handle so it can write selectively in interactive mode
            'options': KBPCheckOptions
        },
    }

    parser.add_argument("--version", "-V", action="version", version=__version__)

    subparsers = parser.add_subparsers(dest='subparser', required=True)

    # See _UsageAllAction
    parser.added_subparsers = []
    parser.register('action', 'usage_all', _UsageAllAction)
    parser.add_argument("--usage-all", action='usage_all', help = "show usage for all subcommands and exit")

    for p in parser_data:
        cur = subparsers.add_parser(p, **parser_data[p]['add_parser'])
        parser.added_subparsers.append(cur)

        for field in (
                dataclasses.fields(parser_data[p]['options']) if 'options' in parser_data[p] else ()
            ) + (
                dataclasses.fields(parser_data[p]['input_options']) if 'input_options' in parser_data[p] else ()
            ):
            name = field.name.replace("_", "-")

            additional_params = {}
            if field.type == int | bool:
                additional_params["type"] = int_or_bool 
            elif hasattr(field.type, "__members__") and hasattr(field.type, "__getitem__"):
                # Handle enum types
                additional_params["type"] = field.type.__getitem__
                additional_params["choices"] = field.type.__members__.values()
            else:
                additional_params["type"] = field.type

            help_text = ''
            if 'doc' in field.metadata:
                help_text += field.metadata['doc']
            elif hasattr(field.type, '__name__'):
                help_text += field.type.__name__
            else:
                help_text += repr(field.type)
            help_text += f" (default: {field.default})"

            cur.add_argument(
                f"--{name}",
                gen_shortopt(p, name),
                dest = field.name,
                #help = (field.type.__name__ if hasattr(field.type, '__name__') else repr(field.type)) + f" (default: {field.default})",
                help = help_text,
                action = argparse.BooleanOptionalAction if field.type == bool else 'store',
                **additional_params,
            )

        cur.add_argument("source_file")
        cur.add_argument("dest_file", nargs='?')

    args = parser.parse_args()

    subparser = args.subparser
    input_options = {}
    if 'input_options' in parser_data[subparser]:
        for field in dataclasses.fields(parser_data[subparser]['input_options']):
            if not hasattr(args, field.name):
                continue
            input_options[field.name] = getattr(args, field.name)
            delattr(args, field.name)
    del args.subparser
    source = parser_data[subparser]['input'](sys.stdin if args.source_file == "-" else args.source_file, **input_options)
    del args.source_file
    if parser_data[subparser]['output_opts'] is None:
        dest = args.dest_file if hasattr(args, 'dest_file') else None
    else:
        dest = open(args.dest_file, 'w', **parser_data[subparser]['output_opts']) if hasattr(args, 'dest_file') else sys.stdout
    if hasattr(args, 'dest_file'):
        del args.dest_file
    parser_data[subparser]['output'](source, args, dest)

# Auto-generate short option based on field name
used_shortopts=collections.defaultdict(lambda: set("hV"))
def gen_shortopt(command, longopt):
    # Options with - likely have duplication, so use a letter from after the
    # last one
    if len(parts := longopt.split("-")) > 1:
        return gen_shortopt(command, parts[-1])
    for char in longopt:
        if char not in used_shortopts[command]:
            used_shortopts[command].add(char)
            return f"-{char}"

# Coerce a string value into a bool or int
# Accept true|false (case-insensitive), otherwise try int
def int_or_bool(strVal):
    if strVal.upper() == 'FALSE':
        return False
    elif strVal.upper() == 'TRUE':
        return True
    else:
        return int(strVal)

if __name__ == "__main__":
    convert_file()
