#!/usr/bin/env python3
# XKCD Parser - A library/cli tool to parse all comics' json from xkcd.com
# MIT License
#
# Copyright (c) 2025 Sergey Sitnikov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import json
import multiprocessing

import requests

AMOUNT_POOL = 50


def check_path_result_data(path: str) -> None:
    f = open(path, "a+")
    f.close()


def get_latest_comic_num() -> int:
    req = requests.get("https://xkcd.com/info.0.json")
    try:
        json_data = req.json()
        if "num" not in json_data or not isinstance(json_data["num"], int):
            print(
                f"ERROR: could not receive adequeate json data from xkcd! Received: {json.dumps(json_data)}"
            )
            exit(1)
        return json_data["num"]
    except Exception as e:
        print(f"ERROR: could not get lastest comic number! {e}")
        exit(1)


def save_to_file(path: str, data: list) -> None:
    with open(path, "w+") as f:
        json.dump(data, f)


def get_json(num: int) -> dict | list:
    req = requests.get(f"https://xkcd.com/{num}/info.0.json")
    json_answer = req.json()
    if "num" not in json_answer:
        print(f"WARNING: no parameter `num` in {num}'s comic JSON! Skipping.")
        return []
    print(f"INFO: Successfully parsed {num} comic", flush=True)
    return json_answer


def update_xkcd_comics_json(json_file: str, /, is_cli: bool = False) -> None:
    try:
        with open(json_file, "r") as f:
            json_text = f.read()
    except FileNotFoundError:
        json_text = "[]"
    try:
        json_data = json.loads(json_text)
        if not isinstance(json_data, list):
            print("WARNING: Wrong JSON file passed. Fallbacked to an empty list.")
            json_data = []
    except json.decoder.JSONDecodeError:
        print("WARNING: Wrong JSON file passed. Fallbacked to an empty list.")
        json_data = []
    check_path_result_data(json_file)
    already = set()
    for i in json_data:
        already.add(i["num"])
    latest_comic_num = get_latest_comic_num()
    if latest_comic_num in already and len(already) == latest_comic_num - 1:
        if is_cli:
            print("No new comics added")
        save_to_file(json_file, json_data)
        return
    need_to_parse = [
        i for i in range(1, latest_comic_num + 1) if i != 404 and i not in already
    ]
    print("New comics amount:", len(need_to_parse))
    with multiprocessing.Pool(AMOUNT_POOL) as p:
        results = p.map(get_json, need_to_parse)
        json_data += [i for i in results if isinstance(i, dict)]
    json_data.sort(key=lambda x: x["num"])
    save_to_file(json_file, json_data)


def cli():
    parser = argparse.ArgumentParser(
        prog="xkcd_parser",
        description="A library/cli tool to parse all comics' json from xkcd.com",
        epilog="Try not to overload xkcd.com servers by overusing this script. Please!",
    )
    parser.add_argument(
        "json_file",
        help="The JSON file of already scraped comics' info. If exists, will be updated with new comics (if any)",
    )
    args = parser.parse_args()
    update_xkcd_comics_json(args.json_file, is_cli=True)


if __name__ == "__main__":
    cli()
