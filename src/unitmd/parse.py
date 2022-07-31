import codecs
import os
import markdown

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>{}</style>
</head>
<body>
    <div id="article"><div class="article-content">{}</div></div>
</body>
</html>
"""

DEFAULT_HIGHLIGHT_CSS_PATH = os.path.join(os.path.dirname(__file__), "highlight.css")
DEFAULT_THEME_CSS_PATH = os.path.join(os.path.dirname(__file__), "theme.css")

EXTENSIONS = [
    "markdown.extensions.meta",
    "markdown.extensions.tables",
    "markdown.extensions.codehilite",
    "markdown.extensions.toc",
    "markdown.extensions.footnotes",
    "markdown.extensions.fenced_code",
    "markdown_captions",

    "pymdownx.superfences",
    "pymdownx.inlinehilite",
    "pymdownx.highlight",
]

EXTENSIONS_CONFIG = {
    "pymdownx.highlight": {
        "css_class": "highlight",
        "pygments_style": "one-dark",
        "linenums": True,
        "linenums_style": "inline"
    },
    "markdown.extensions.codehilite": {
        "css_class": "highlight"
    }
}


def read_file_content(filename):
    if isinstance(filename, str) and os.path.exists(filename):
        input_file = codecs.open(filename, mode="r", encoding="utf-8")
        try:
            return input_file.read()
        finally:
            input_file.close()
    else:
        raise ValueError("filename need a path str, {} unexpected.".format(filename))


class MarkdownParser:
    def __init__(self, extensions=None, extension_configs=None):
        if extensions is None:
            extensions = set()
        if extension_configs is None:
            extension_configs = {}
        extensions.update(EXTENSIONS)
        extension_configs.update(EXTENSIONS_CONFIG)
        self._markdown = markdown.Markdown(extensions=extensions, extension_configs=extension_configs,
                                           output_format="html5")

    def parse_content(self, text):
        return self._markdown.convert(text)

    def convert_from_stream_to_stream(self, input, theme_css=None, highlight_css=None, output=None, standalone=True):
        try:
            content = self.parse_content(input.read())

            if standalone:
                if theme_css is None:
                    theme_css = read_file_content(DEFAULT_THEME_CSS_PATH)
                if highlight_css is None:
                    highlight_css = read_file_content(DEFAULT_HIGHLIGHT_CSS_PATH)
            else:
                theme_css = highlight_css = ""

            html = HTML_TEMPLATE.format(theme_css + highlight_css, content)

            if output:
                output.write(html)
            return html
        finally:
            input.close()
            if output:
                output.close()

    def convert_from_file(self, input, output, theme_css=DEFAULT_THEME_CSS_PATH,
                          highlight_css=DEFAULT_HIGHLIGHT_CSS_PATH, standalone=True):
        if isinstance(input, str) and isinstance(output, str):
            if os.path.exists(input):
                input_file = codecs.open(input, mode="r", encoding="utf-8")
            else:
                input_file = codecs.getreader("utf-8")(input)
            output_file = codecs.open(output, mode="w", encoding="utf-8")
            self.convert_from_stream_to_stream(input_file, theme_css, highlight_css, standalone=standalone,
                                               output=output_file)
        else:
            raise ValueError(
                "input/output need str, {} unexpected".format(type(input))
            )
