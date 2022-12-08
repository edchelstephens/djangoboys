class StringToHTMLParserMixin:
    """String to html compatible string parser mixin."""

    def parse_to_html(self, string: str) -> str:
        """Parse string to compatible html version.*

        * The characters
        `&` get's transformed to `&amp`

        https://developer.mozilla.org/en-US/docs/Glossary/Entity#reserved_characters
        """

        string = string.replace("&", "&amp;")
        return string
