# zoomlaunch

**zoomlaunch** is a python command line tool to launch Zoom meetings.

Meetings can either be launched by directly specifying a meeting id (and optional password), or by choosing a meeting out of a stored list.

**Important**: Please read the disclaimer at the end of this README before using the software.

## Usage
```bash
# show all stored meetings
zoomlaunch.py
zoomlaunch.py show
# show stored meeting
zoomlaunch.py show 1

# launch meeting with index (from list)
zoomlaunch.py launch 1
# launch meeting with id
zoomlaunch.py launch "123 456 7890"
# launch meeting with id and password
zoomlaunch.py launch "987654321" "abcdefghijklmnop"
# launch meeting with zoom url
zoomlaunch.py launch "https://www.zoom.us/j/1234567890?pwd=abcdefghijklmnop"

# launch next meeting according to "time" property
zoomlaunch.py next
```

## Installation
**zoomlaunch** is compatible with Linux, Mac and Windows (untested). For Linux and Mac, just add/move the `zoomlaunch.py` script into your `PATH` and make sure its executable. Of course, you need Python 3 for this to work.

### Data File
**zoomlaunch** stores meeting data in a JSON file. An example JSON file is available (`zoomlaunch.json`). The format is as follows:
```jsonc
[
  {
    "name": "Meeting 1",         // only used for display
    "id": "123 456 7890",        // spaces are ignored
    "password": "abcdefghijkl",  // optional
    "time": [3, "hh:mm"]         // optional, 3 is the weekday (monday: 1)
  }
]
```

The path to the file can be specified in the beginning of the `zoomlaunch.py` script like this (either absolute (preferred) or relative to script directory):
```py
DATA_FILE = '/foo/bar/zoomlaunch.json'
```

## URL Scheme Documentation
The URL scheme had been documented on https://marketplace.zoom.us/docs/client-url-schemes. However, since external support has been discontinued, the documentation has been removed.

An outline of the functionality can be found on [this Zoom Developer Blog article](https://medium.com/zoom-developer-blog/zoom-url-schemes-748b95fd9205), which has fortunately remained online.

## License
This software is released under the MIT License. For more information, see the LICENSE file.

## Disclaimer
The author of this script is not affiliated with Zoom Video Communications, Inc. in any way. The script makes uses of an unsupported URL scheme to directly open Zoom meetings without opening a web URL first. This interface may break at any time. The author does not provide any warranty whatsoever. See the LICENSE file for more information.