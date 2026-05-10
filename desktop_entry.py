from configparser import ConfigParser


class DesktopEntry:
    def __init__(self, path: str):
        self.path: str = path
        self.config: ConfigParser = self._make_parser()
        _ = self.config.read(path)

        entry = self.config["Desktop Entry"]
        categories = entry.get("Categories")

        self.name: str = entry["Name"]
        self.comment: str | None = entry.get("Comment")
        self.executable: str | None = entry.get("Exec")
        self.icon: str | None = entry.get("Icon")
        self.terminal: bool = entry.get("Terminal") == "true"
        self.entry_type: str = entry["Type"]
        self.categories: list[str] | None = (
            [x for x in categories.split(";") if x] if categories else None
        )
        self.hidden: bool = entry.get("NoDisplay") == "true"

    @staticmethod
    def _make_parser() -> ConfigParser:
        parser = ConfigParser(interpolation=None)
        parser.optionxform = str  # pyright: ignore[reportAttributeAccessIssue]
        return parser

    CONFIG_KEYS: dict[str, str] = {
        "name": "Name",
        "comment": "Comment",
        "executable": "Exec",
        "terminal": "Terminal",
        "hidden": "NoDisplay",
    }

    def set_field(self, attr: str, value: str | bool) -> None:
        config_key = self.CONFIG_KEYS[attr]
        if isinstance(value, bool):
            self.config["Desktop Entry"][config_key] = "true" if value else "false"
        else:
            self.config["Desktop Entry"][config_key] = value or ""
        with open(self.path, "w") as f:
            self.config.write(f)
        setattr(self, attr, value)
