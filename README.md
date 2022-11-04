![header](src/main/resources/base/header/header-light.png#gh-light-mode-only)
![header](src/main/resources/base/header/header-dark.png#gh-dark-mode-only)

# YouTube Playlist Generator

![GitHub top language](https://img.shields.io/badge/language-python-orange)
![Python Version](https://img.shields.io/badge/python-3.10.6-yellow)
![License](https://img.shields.io/badge/license-GNU%20v3.0-blue)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=bugs)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=christianhofmanncodes_youtube-playlist-generator&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=christianhofmanncodes_youtube-playlist-generator)
[![Crowdin](https://badges.crowdin.net/youtube-playlist-generator/localized.svg)](https://crowdin.com/project/youtube-playlist-generator)

Generate YouTube playlists without an account.

## Please note

This project originally contained both a CLI and a GUI version.
As of version 0.0.5, the CLI version will no longer be developed.

## Features

- Add URL or ID
- Specify playlist title
- Create new playlist (deletes all items in the playlist)
- Playlist Tools (Count items, Clear all items, Remove duplicates)
- Sort items (Ascending & Descending)
- Search for items in playlist (Find)
- Rename specific items
- Change order of playlist items (via drag and drop)
- Delete specific items
- Shuffle-mode
- Generate playlist URL
- Automatically open generated URL in default web browser
- Copy URL to clipboard
- Open .ytplaylist file
- Save .ytplaylist file
- Import a .txt file (items must be in new lines) or .csv file (items must be comma-separated)
- Export playlist items as a .txt or .csv file
- Drag & Drop a .yt-playlist file or a .txt or .csv file onto the window
- Darkmode & Whitemode (switchable in settings)
- Recent files in File menu
- Supported languages (switchable in settings)
  - English
  - Deutsch (German)
  - Español (Spanish)

## Screenshots

### First start

| Windows                                                       | Linux                                                     | macOS                                                   |
| ------------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| ![windows](src/main/resources/base/screenshot/windows/screenshot-first-start.png) | ![linux](src/main/resources/base/screenshot/linux/screenshot-first-start.png) | ![macos](src/main/resources/base/screenshot/mac/screenshot-first-start.png) |

### With items added

| Windows                                                            | Linux                                                          | macOS                                                        |
| ------------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------------------------------------------ |
| ![windows](src/main/resources/base/screenshot/windows/screenshot-with-items-added.png) | ![linux](src/main/resources/base/screenshot/linux/screenshot-with-items-added.png) | ![macos](src/main/resources/base/screenshot/mac/screenshot-with-items-added.png) |

### After YouTube Playlist generation

| Windows                                                                     | Linux                                                                   | macOS                                                                 |
| --------------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------- |
| ![windows](src/main/resources/base/screenshot/windows/screenshot-after-playlist-generation.png) | ![linux](src/main/resources/base/screenshot/linux/screenshot-after-playlist-generation.png) | ![macos](src/main/resources/base/screenshot/mac/screenshot-after-playlist-generation.png) |

## Installation

Just download and run the newest version from the Releases.
Choose your file according to the operating system (Windows, Linux or macOS) you are using.

Launch the program. Now you can either create a new playlist by adding an URL or ID to the playlist one by one, or you can open a `.ytplaylist` file. If you want to save your playlist, you can save the playlist to a `.ytplaylist` file with all its items and the playlist title. Share it with a friend if you want.

## Run Locally

Clone the project

```bash
  git clone https://github.com/christianhofmanncodes/youtube-playlist-generator.git
```

Go to the project directory

```bash
  cd youtube-playlist-generator
```

Install Python

```bash
  pip install python
```

Install dependencies

```bash
  pip install -r requirements/base.txt
```

Run the app

```bash
  fbs run
```

Note: On Linux and macOS you have to use `pip3` and `python3`.  
Pandas only needs to be installed if you want to use the CLI version.

## Security

You can check for security issues with the following commands:

```bash
  sudo chmod +x src/main/python/scanners/bandit.sh
  sudo sh src/main/python/scanners/bandit.sh
```

```bash
  safety check
```

You can also find the results of sonarcloud checks here:

[sonarcloud](https://sonarcloud.io/project/overview?id=christianhofmanncodes_youtube-playlist-generator)

## Known issues & possible fixes

If you have any issues with running the program please first check your python version.
Minimal version required is `Python 3.9.5`.

### Cannot build because libpython3.9 is missing

`sudo apt-get install libpython3.9-dev`

### /lib/x86_64-linux-gnu/libc.so.6: version \`GLIBC_2.33' not found”

```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.9
sudo apt-get upgrade libstdc++6
```

### PyQt6 cannot be installed via pip

```bash
pip3 install --upgrade pip
pip3 install PyQt6
```

### Failed to extract PyQt6/Qt6/plugins/egldeviceintegrations/libqeglfs-emu-integration.so: failed to open target file! fopen: No such file or directory

`export QT_QPA_EGLFS_FB=/dev/fbX`

### INTERNAL ERROR: cannot create temporary directory

You do not have enough space on your system.
Simply free up some space.

## Roadmap

- Fetch YouTube video information (title, channel and thumbnail)
- Display playlist duration

## FAQ

### How did you come up with this project?

A friend of mine wanted to build a YouTube playlist with me. But I had no idea how to do it because I don't have a Google account and I didn't want to create one either. So I came up with the idea to develop a neat little program that could do that.

### What types of links are supported?

The program supports both YouTube and Invidious links of any type.

```bash
https://www.youtube.com/watch?v=
https://www.youtu.be/
https://invidious.namazso.eu/watch?v=
```

### Can I batch import URLs / video IDs?

As requested in [#2](https://github.com/christianhofmanncodes/youtube-playlist-generator/issues/2) the function has been added to version 0.2.0.
Just click on "Import" in the menu and select the .txt file you want to import accordingly.

It should look something like this:

```text
Hbb5GPxXF1w
4vbDFu0PUew
Moq0aOiTUOA
qfVuRQX0ydQ
juQvizeZJFM
```

You can also use URLs:

```text
https://youtu.be/gQlMMD8auMs
https://www.youtube.com/watch?v=gQlMMD8auMs
https://www.youtube.com/watch?v=f6YDKF0LVWw
https://www.youtube.com/watch?v=UNFk6_to5_0
https://www.youtube.com/watch?v=ygJgQAYZVi0
https://www.youtube.com/watch?v=gRnuFC4Ualw
https://www.youtube.com/watch?v=k6jqx9kZgPM
```

Or you can mix them too:

```text
Hbb5GPxXF1w
4vbDFu0PUew
Moq0aOiTUOA
qfVuRQX0ydQ
juQvizeZJFM
https://youtu.be/gQlMMD8auMs
f6YDKF0LVWw
UNFk6_to5_0
ygJgQAYZVi0
https://www.youtube.com/watch?v=gRnuFC4Ualw
k6jqx9kZgPM
````

If you want to import a .csv file, just select the file extension in the file dialog.

It should look something like this:

```csv
Hbb5GPxXF1w,4vbDFu0PUew,Moq0aOiTUOA,qfVuRQX0ydQ,juQvizeZJFM
```

## Acknowledgements

- [Python](https://github.com/python/)
- [Qt6](https://doc.qt.io/qtforpython-6/index.html)
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [Qt-Material](https://github.com/UN-GCPDS/qt-material)
- [fbs](https://build-system.fman.io/)
- [pytube](https://github.com/pytube/pytube)

## Contributing

Contributions are always welcome!

See `CONTRIBUTING.md` for ways to get started.

You can report any issues and are welcome to create pull requests.
Please use the labels accordingly: `bug` for bugs, `documentation` for improvements to the documentation and `enhancement` for feature requests.

### Translations

You are always welcome to help translating this project.  
We simply use [Crowdin](https://crowdin.com/project/youtube-playlist-generator).

## License

This code is free software licensed under the [GPL v3.0](https://choosealicense.com/licenses/gpl-3.0/). See the LICENSE file for details.

## Feedback

If you have any feedback, please reach out to me at: contact@youtube-playlist-generator.com
