class MQuote(dict):
    UNATTRIBUTED = "__none__"

    def __init__(self, quote_dict: dict, media_title: str, media_type: str, year: int):
        super().__init__()
        self.update(quote_dict)
        self["media_title"] = media_title
        self["media_type"] = media_type
        self["year"] = year

    @property
    def characters(self) -> list[str]:
        return self["characters"]

    @property
    def lines(self) -> list[dict[str, str]]:
        lines = self["lines"]
        return lines

    @property
    def media_title(self) -> str:
        return self["media_title"]

    @property
    def media_type(self) -> str:
        return self["media_type"]

    @property
    def year(self) -> int:
        return self["year"]

    def __str__(self):
        lines = []
        for quote_dict in self.lines:
            for k, v in quote_dict.items():
                if k != self.UNATTRIBUTED:
                    line = f"{k}: {v}"
                else:
                    line = f"{v}"
                lines.append(line)
        _str = "\n".join(lines)
        return _str
