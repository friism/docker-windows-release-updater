#!/usr/bin/env python

import argparse
from datetime import datetime
import email.utils
import hashlib
import json

import requests

DEFAULT_URL = (
    "https://download.docker.com/components/engine/windows-server/index.json"
)

DEFAULT_NOTES = (
    "Docker for Windows Server 2016"
)


def grab_file(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Unable to get {url}")
    return resp


def rfc1123_to_iso(date_str):
    return datetime(*email.utils.parsedate(date_str)[:6]).isoformat()


def generate_sha256(content):
    shagen = hashlib.sha256()
    shagen.update(content)
    return shagen.hexdigest()


def main(args):
    index_resp = grab_file(DEFAULT_URL)
    index = json.loads(index_resp.content)
    if index["versions"].get(args.release_name):
        print(f"Release {args.release_name} already exists!")
        exit(1)
    download_resp = grab_file(args.release_url)
    index["versions"][args.release_name] = {
        "date": rfc1123_to_iso(download_resp.headers["Last-Modified"]),
        "url": args.release_url,
        "size": len(download_resp.content),
        "sha256": generate_sha256(download_resp.content),
        "notes": DEFAULT_NOTES
    }
    index["channels"][args.release_name] = {
        "version": args.release_name
    }
    if args.release_channel != args.release_name:
        index["channels"][args.release_channel] = {
            "alias": args.release_name
        }
    # TODO: This will eventually upload this json dump to S3
    print(json.dumps(index, indent=4, sort_keys=True))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Add a release to download.docker.com for windows")
    parser.add_argument(
        "release_name",
        type=str,
        help="Name of the release"
    )
    parser.add_argument(
        "release_channel",
        type=str,
        help="Channel where the release will be located"
    )
    parser.add_argument(
        "release_url",
        type=str,
        help="URL where release is located"
    )
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_arguments())
