# youtube-playlist-generator

A fun program based on Python to generate YouTube Playlists without an account.

![GitHub top language](https://img.shields.io/badge/language-python-orange)
![Python Version](https://img.shields.io/badge/python-3.10.2-yellow)
![License](https://img.shields.io/badge/license-GNU%20General%20Public%20License%20v3.0-blue)

---

## Navigation

- [Functions](#functions)
  - [Coming soon](#coming-soon)
  - [Support](#support)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [License](#license)

---

## Functions

- Add URL or ID
- Specify playlist title
- Clear playlist (deletes all items in playlist)
- Delete specific items
- Generate playlist URL
- Open generated URL automatically in default Web Browser
- Copy URL to clipboard
- Import .ytplaylist file
- Export to .ytplaylist file

### Coming soon

- Change order of playlist items
- Keyboard shortcuts
- Change program languge (English/Deutsch)

### Support

The program supports both YouTube and Invidious links of any instance.

```
https://www.youtube.com/watch?v=
https://www.youtu.be/
https://invidious.namazso.eu/watch?v=
```

## Getting started

Just download and run the newest version from the Releases.
Select your file accordingly to the OS (Windows, Linux or macOS) you are running.

Start the program. Now you can either create a new playlist by adding a URL or ID one by one to the playlist or you can import a `.ytplaylist` file. If you want to save your playlist you can export the playlist with all its items and playlist title to a `.ytplaylist` file. Hand it over to a friend, if you want.

### Prerequisites

If you want to deploy the program by yourself:
The client libraries are supported on Python 3.6 or later.
Tested on Python 3.10.2

### Installation

1. Clone the git repository. `git clone https://github.com/christianhofmanncodes/youtube-playlist-generator.git`
2. Install newest version of Python
3. Install pandas with `pip install pandas`
4. Install pyqt6 with `pip install pyqt6`
5. Run the file
   - If you want to use the console version: `python src/console/app.py`
   - If you want to use the GUI version: `python src/giu/app-gui.py`

Note: On Linux and macOS you need to use `pip3` and `python3`.

## License

This code is free software licensed under the GPL 3. See the LICENSE file for details.
