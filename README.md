# zoomlaunch

**zoomlaunch** is a python command line tool to launch Zoom meetings.

Meetings can either be launched by directly specifying a meeting id (and optional password), or by choosing a meeting out of a stored list.

**Important**: Because this script relies on `xdg-open`, it only works on Linux operating systems as of now.

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
```

## Installation
Just add/move the `zoomlaunch.py` script into your `PATH` and make sure its executable. Of course, you need Python 3 for this to work.

### Data File
**zoomlaunch** stores meeting data in a JSON file. An example JSON file is available (`zoomlaunch.json`). The path to the file can be specified in the beginning of the `zoomlaunch.py` script like this:
```py
DATA_FILE = '/foo/bar/zoomlaunch.json'
```
**Format:**
```json
[
  {
    "name": "Meetingname as string",
    "id": "Meetingid as string",        # Spaces dont matter
    "password": "Password as string",   # Encoded password for usage in urls
    "time": [3, "hh:mm"]                # Where 3 equals the weekday (1 = Monday)
  }
]
```
Use an absolute path so it accesses the same file independet of where it is called from.

## URL Scheme Documentation
The URL scheme had been documented on https://marketplace.zoom.us/docs/client-url-schemes. However, since external support has been discontinued, the documentation has been removed.

An outline of the functionality can be found on [this Zoom Developer Blog article](https://medium.com/zoom-developer-blog/zoom-url-schemes-748b95fd9205), which has fortunately remained online.

## License
This software is released under the MIT License. For more information, see the LICENSE file.

## Disclaimer
The author of this script is not affiliated with Zoom Video Communications, Inc. in any way. The script makes uses of an unsupported URL scheme to directly open Zoom meetings without opening a web URL first. This interface may break at any time. The author does not provide any warranty whatsoever. See the LICENSE file for more information.