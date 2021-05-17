import os
from argparse import ArgumentParser

from code_completion.client import CompletionClient

ext_to_language = {
    ".py": "Python",
    ".java": "Java",
    ".kt": "Kotlin"
}


def main(args):
    filename = args.filename
    ext = os.path.splitext(filename)[1]
    language = ext_to_language[ext]

    client = CompletionClient(language)
    with open(filename, "r") as f:
        print(client.complete(
            filename=filename,
            context=f.read(),
            prefix=args.prefix,
        ))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, required=True, help="Path to the file to complete")
    parser.add_argument("-p", "--prefix", type=str, required=False, default="", help="Prefix of the completion")
    main(parser.parse_args())
