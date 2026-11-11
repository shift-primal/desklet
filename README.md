# desklet

A small PyQt6 app for managing Linux `.desktop` launcher entries. It lists every entry it finds, shows each one's icon, and lets you edit it in place.

- Edit an entry's name, comment, executable, and its terminal and hidden flags. Changes are written straight back to the `.desktop` file.
- Hide or unhide several entries at once from the right-click menu.
- Icons resolve from your current icon theme.

## Run

Requires Python 3.11+ and PyQt6.

```sh
pip install PyQt6
python app.py
```

## Config

`config.json` sets where to scan and how:

- `scan_paths.default`: `/usr/share/applications` and `~/.local/share/applications`
- `settings.test_mode`: when `true`, scans the sample entries in `testfiles/` instead, so you can try the app without touching real launchers. The repo ships with test mode on.
- `settings.scan_pattern`: glob for entry files (default `*.desktop*`)

## Layout

- `app.py`: entry point
- `main_window.py`: list and editor in a split view
- `widgets/`: entry list and entry editor
- `desktop_entry.py`: reads and writes a single `.desktop` file
- `entry_manager.py`: scans the configured paths
