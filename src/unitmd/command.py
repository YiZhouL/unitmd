import argparse

from .parse import MarkdownParser

args_parser = argparse.ArgumentParser()
args_parser.add_argument("-i", '--input', type=argparse.FileType(mode="r", encoding="utf-8"), required=True)
args_parser.add_argument("-o", '--output', type=argparse.FileType(mode="w", encoding="utf-8"), required=True)
args_parser.add_argument("--standalone", type=bool, default=True, required=False)
args_parser.add_argument("--highlight_css", type=str, required=False, default=None)
args_parser.add_argument("--theme_css", type=str, required=False, default=None)


def parse():
    args = args_parser.parse_args()
    md_parser = MarkdownParser()
    md_parser.convert_from_stream_to_stream(args.input, theme_css=args.theme_css, highlight_css=args.highlight_css,
                                            standalone=args.standalone, output=args.output)
