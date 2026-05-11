from configparser import ConfigParser, SectionProxy


class DesktopEntry:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.parser: ConfigParser = self._make_parser()

        with open(path, encoding="utf-8") as f:
            self.parser.read_file(f)

        entry: SectionProxy = self.parser["Desktop Entry"]

        categories: str | None = entry.get("Categories")

        self.name: str = entry["Name"]
        self.comment: str | None = entry.get("Comment")
        self.executable: str | None = entry.get("Exec")
        self.icon: str | None = entry.get("Icon")
        self.terminal: bool = entry.get("Terminal") == "true"
        self.entry_type: str = entry["Type"]
        self.categories: list[str] | None = [x for x in categories.split(";") if x] if categories else None
        self.hidden: bool = entry.get("NoDisplay") == "true"

    DESKTOP_ENTRY_KEYS: dict[str, str] = {
        "name": "Name",
        "comment": "Comment",
        "executable": "Exec",
        "terminal": "Terminal",
        "hidden": "NoDisplay",
        "entry_type": "Type",
        "categories": "Categories",
        "icon": "Icon",
    }

    @staticmethod
    def _make_parser() -> ConfigParser:
        parser: ConfigParser = ConfigParser(interpolation=None)
        parser.optionxform = str  # pyright: ignore[reportAttributeAccessIssue]

        return parser

    def set_field(self, attr: str, value: str | bool) -> None:
        desktop_entry_key: str = self.DESKTOP_ENTRY_KEYS[attr]

        if isinstance(value, bool):
            self.parser["Desktop Entry"][desktop_entry_key] = "true" if value else "false"
        else:
            self.parser["Desktop Entry"][desktop_entry_key] = value

        with open(self.path, "w", encoding="utf-8") as f:
            self.parser.write(f)

        setattr(self, attr, value)
