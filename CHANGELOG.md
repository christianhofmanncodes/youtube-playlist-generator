# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Compare changes to last version]

## [0.3.0] - 2023-16-09

### Added

- You can now paste YouTube playlist URLs into to the URL or ID field
  - YouTube Playlist Generator will automatically extract the playlist items for you
- Search for YouTube videos by its title and choose the video(s) you want to add to the playlist
- Translations (switchable in settings)
  - Polski (Polish) thanks to [poduszkowiec_](https://crowdin.com/profile/poduszkowiec_)
  - Nederlands (Dutch)

### Changed

- Show generated playlist length in StatusBar instead of MessageBox

### Fixed

- Dialog info text is now correctly indented

### Security

- Remove urllib for security reasons, instead use requests

## [0.2.0] - 2022-11-30

### Added

- Import function to batch import multiple video IDs / URLs via .txt and .csv file [#2](https://github.com/christianhofmanncodes/youtube-playlist-generator/issues/2)
- Export function to export playlist items to `.csv` or `.txt` file
- Drag & Drop a `.yt-playlist` file or a `.txt` or `.csv` file onto the window
- New Video Info Dialog to display YouTube video information (title, channel, length, description, views, publish date and thumbnail)
- Display playlist duration (after playlist generated successfully)
- More language translations
- Shortcuts to Import, Export, Save as and Sort by Ascending and Descending

### Changed

- Revert to PyQt5 and make code work with Python3.6
- Open and Open recent option in menu is now grouped together
- Moving items in playlist via drag and drop copies them now (hold Ctrl/Cmd to prevent this behavior)
- Redesign of the "Keyboard Shortcuts" tab in Settings (now uses a table to display all shortcuts)

### Fixed

- Open recent file menu is now correctly translated and placed after the open file option
- Clear recent files is now directly displayed after new file was added to the recent files menu (not anymore only after restart)
- Bug if no playlist item is selected, open VideoInfoDialog with information about the video instead of displaying information QMessageBox
- Crash when playlist contains wrong video ids or video ids with not allowed characters (for example "\n")
- Bug if no language was changed in settings, no settings would be saved even though they were changed

### Security

- Fix vulnerability [CWE-22](https://cwe.mitre.org/data/definitions/22.html) "Audit url open for permitted schemes. Allowing use of "file:" or custom schemes is often unexpected.": Validate URL before opening it with urllib.

## [0.1.0] - 2022-10-30

### Added

- Darkmode & Whitemode (switchable in settings)
- Search for items in playlist (QInputDialog)
- Recent files in File menu
- "New playlist" option
- New license dialog
- Native About_Qt dialog
- Translations (switchable in settings)
  - Deutsch (German)
  - Español (Spanish)

### Changed

- Refactor code
- Redesign the settings dialog
- "Import Playlist" is now simply "Open"
- "Export Playlist" is now simply "Save"

### Fixed

- Change program language in settings
- Edit menu functions now work probably
- Settings are now loaded automatically
- Keyboard shortcuts can now be changed

### Deleted

- "Reset playlist" option (replaced by "New Playlist")
- InfoDialog (replaced by native About_Qt and new license dialog)

### Security

- Fix vulnerability sonarlint(python:S4830) - [RSPEC-4830](https://sonarsource.atlassian.net/browse/RSPEC-4830) [RSPEC-5436](https://sonarsource.atlassian.net/browse/RSPEC-5436)

## [0.0.5-alpha] - 2022-08-07

### Added

- Playlist Tools (Count items, Clear all items, Remove duplicates)
- Sort items (Ascending & Descending)
- List scrolls now to newly added item
- Tooltips
- New shortcuts for: "Count items", "Remove duplicates" and "Rename item"

### Changed

- Buttons have now icons
- UI: Playlist title is now displayed at the top
- UI: "Reset playlist" is now simply "Reset"
- UI: "Generate playlist" is now simply "Generate"
- UI: "Copy" button replaced with icon button
- UI: Switch input widgets (QTextEdit to QLineEdit)
- UI: Switch to own theme "yt-dark-red.xml"
- Shuffle mode can now be activated only when there are at least three items in the playlist (no longer two items)
- If a playlist already contains items, you will get asked if you want to create a new playlist or if you want to add the imported playlist to the existing playlist.
- To add an item to the playlist simply press Enter (instead of Alt+Enter or Option+Enter)
- Updated dependencies (requirements/base.txt)
- Change folder structure entirely to work with fbs

### Fixed

- Fix minor spelling mistakes in Code and UI
- Generated playlist URL now shows probably
- If playlist can not be generated "Copy" button stays inactive
- Generated playlist URL will be deleted after reset

### Removed

- "Playlist is being generated..." message in URL field
- print statements in code (replace with proper logging module)

## [0.0.4-alpha] - 2022-03-29

### Added

- First Windows release!
- First Linux release!
- Icon for Windows

### Fixed

- Fix crash after playlist generation if no internet connection exists
- Quit function for macOS and Windows

### Removed

- Icons from .ui files

## [0.0.3-alpha] - 2022-03-28

### Added

- Shuffle mode for playlist items
- Keyboard shortcuts
- Menubar
- App Logo to Info Dialog

### Changed

- Bigger 'Generate' button
- Rename "Clear playlist" to "Reset playlist"
- Disable "Add" button per default and only activate if URL or ID not empty
- Setting default local to "English"

### Removed

- Import & Export buttons from GUI (now lives in menu)
- About text and Settings link (now lives in menu)
- Info button from Settings Dialog (now lives in menu)

## [0.0.2-alpha] - 2022-03-26

### Added

- Reorder playlist items
- Tab support for all elements
- Check if video ids are valid (otherwise show an error message)

### Changed

- Replace AppleSystemUIFont with Roboto

### Fixed

- Output correct playlist URL not video ids URL

### Removed

- Wrong link in InfoDialog

## [0.0.1-alpha] - 2022-03-20

- This is the initial release of YouTube Playlist Generator

[Compare changes to last version]: https://github.com/christianhofmanncodes/youtube-playlist-generator/compare/v0.2.0...v0.3.0
[0.3.0]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.3.0
[0.2.0]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.2.0
[0.1.0]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.1.0
[0.0.5-alpha]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.0.5-alpha
[0.0.4-alpha]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.0.4-alpha
[0.0.3-alpha]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.0.3-alpha
[0.0.2-alpha]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.0.2-alpha
[0.0.1-alpha]: https://github.com/christianhofmanncodes/youtube-playlist-generator/releases/tag/v0.0.1-alpha
