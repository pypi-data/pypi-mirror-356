# XKCD Parser
A library/cli tool to parse all comics' json from [xkcd.com](https://xkcd.com)

## Download dump
https://aqendo.github.io/xkcd-parser/parsed.json
## Automatic deployment
You can generate JSON dump by yourself and you can download `parsed.json` file from `gh_pages` repo or directly from [Github Pages Link]
(https://aqendo.github.io/xkcd-parser/parsed.json). This repository has CI/CD configured to automatically update that file periodically.
## CLI Tool Usage
```
usage: xkcd_parser [-h] json_file

A library/cli tool to parse all comics' json from xkcd.com

positional arguments:
  json_file   The JSON file of already scraped comics' info. If exists, will be updated with new comics (if any)

options:
  -h, --help  show this help message and exit

Try not to overload xkcd.com servers by overusing this script. Please!
```
## Using it as a library
```python
import xkcd_parser

# if `is_cli` is set to True, then it will print if it didn't find any new comics
xkcd_parser.update_xkcd_comics_info("path/to/file/comics.json", is_cli=False)
```
## License
```
XKCD Parser - A library/cli tool to parse all comics' json from xkcd.com
MIT License

Copyright (c) 2025 Sergey Sitnikov

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
