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
        self.terminal: str | None = entry.get("Terminal")
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

    def set_hidden(self, hidden: bool) -> None:
        self.config["Desktop Entry"]["NoDisplay"] = "true" if hidden else "false"
        with open(self.path, "w") as f:
            self.config.write(f)
        self.hidden = hidden
