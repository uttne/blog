from .modules.blog_manager import BlogManager
import argparse

def subcommand_up(args):
    bm = BlogManager()
    bm.run(dry=args.dry)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    upParser = subparsers.add_parser("up")
    upParser.add_argument("-d", "--dry", action="store_true")
    upParser.set_defaults(handler=subcommand_up)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
