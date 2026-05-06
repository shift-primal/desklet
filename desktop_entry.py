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

    def set_name(self, name: str) -> None:
        self.config["Desktop Entry"]["Name"] = name if name else ""
        with open(self.path, "w") as f:
            self.config.write(f)
        self.name = name

    def set_comment(self, name: str) -> None:
        self.config["Desktop Entry"]["Comment"] = name if name else ""
        with open(self.path, "w") as f:
            self.config.write(f)
        self.comment = name

    def set_executable(self, name: str) -> None:
        self.config["Desktop Entry"]["Exec"] = name if name else ""
        with open(self.path, "w") as f:
            self.config.write(f)
        self.executable = name

    def set_terminal(self, terminal: bool) -> None:
        self.config["Desktop Entry"]["NoDisplay"] = "true" if terminal else "false"
        with open(self.path, "w") as f:
            self.config.write(f)
        self.terminal = terminal

    def set_hidden(self, hidden: bool) -> None:
        self.config["Desktop Entry"]["NoDisplay"] = "true" if hidden else "false"
        with open(self.path, "w") as f:
            self.config.write(f)
        self.hidden = hidden
