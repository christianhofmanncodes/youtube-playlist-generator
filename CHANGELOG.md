# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.0.5 - 2022-08-02

### Added

- Button with icons
- Playlist Tools (Count items, Clear all items, Remove duplicates)
- Sort items (Ascending & Descending)
- List scrolls now to newly added item
- Tooltips

### Changed

- UI: Playlist title is now displayed at the top
- UI: "Reset playlist" is now simply "Reset"
- UI: "Generate playlist" is now simply "Generate"
- UI: "Copy" button replaced with icon button
- UI: Switch input widgets (QTextEdit to QLineEdit)
- UI: Add opacity
- Fix minor spelling mistakes in Code and UI
- Shuffle mode can now be activated only when there are at least three items in the playlist (no longer two items)
- Generated playlist URL now shows probably
- If a playlist already contains items, you will get asked if you want to create a new playlist or if you want to add the imported playlist to the existing playlist.
- If playlist can not be generated "Copy" button stays inactive
- Generated playlist URL will be deleted after reset

### Removed

- "Playlist is being generated..." message in URL field
- print statements in code (replace with proper logging module)

## 0.0.4 - 2022-03-29

### Added

- First Windows release!
- First Linux release!
- Icon for Windows
- Quit function for macOS and Windows

### Changed

- Fix crash after playlist generation if no internet connection exists

### Removed

- Icons from .ui files

## 0.0.3 - 2022-03-28

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

## 0.0.2 - 2022-03-26

### Added

- Reorder playlist items
- Tab support for all elements
- Check if video ids are valid (otherwise show an error message)

### Changed

- Output correct playlist url not video ids url
- Replace AppleSystemUIFont with Roboto

### Removed

- Wrong link in InfoDialog

## 0.0.1 - 2022-03-20

- Initial release.
