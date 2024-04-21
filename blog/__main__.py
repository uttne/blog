from .modules.blog_manager import BlogManager
from .modules.secret_manager import SecretManager
import argparse
import os
from dotenv import load_dotenv

load_dotenv()


def subcommand_new(args):

    filename = args.filename if args.filename else []
    title = args.title if args.title else ""
    tag = args.tag if args.tag else []

    bm = BlogManager()
    bm.new(filename=filename, title=title, tags=tag)


def subcommand_up(args):
    bm = BlogManager()
    bm.run(dry=args.dry)


def subcommand_secret(args):

    if args.encrypt and args.decrypt:
        raise Exception("--encrypt と --dexrypt は両方を設定することはできません")
    sm = SecretManager()

    secret_json_file = "./client_secret.json"
    encrypt_file = "./client_secret.json.enc"

    passphrase = os.environ.get("BLOGGER_SECRET_ENCRYPT_PASSPHRASE")

    if args.encrypt:
        sm.encrypt_file(
            input_file=secret_json_file, output_file=encrypt_file, passphrase=passphrase
        )
    elif args.decrypt:
        sm.decrypt_file(
            input_file=encrypt_file,
            output_file=secret_json_file,
            passphrase=passphrase,
        )


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

    upParser = subparsers.add_parser("secret")
    upParser.add_argument("-e", "--encrypt", action="store_true")
    upParser.add_argument("-d", "--decrypt", action="store_true")
    upParser.set_defaults(handler=subcommand_secret)

    args = parser.parse_args()
    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
