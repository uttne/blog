from .modules.blog_manager import BlogManager
import argparse


def subcommand_new(args):

    filename = args.filename if args.filename else []
    title = args.title if args.title else ""
    tag = args.tag if args.tag else []

    bm = BlogManager()
    bm.new(filename=filename, title=title, tags=tag)


def subcommand_up(args):
    bm = BlogManager()
    bm.run(dry=args.dry)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    newParser = subparsers.add_parser("new")
    newParser.add_argument("-n", "--filename", type=str, nargs="*")
    newParser.add_argument("-t", "--title", type=str)
    newParser.add_argument("-l", "--tag", type=str, nargs="*")
    newParser.set_defaults(handler=subcommand_new)

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
