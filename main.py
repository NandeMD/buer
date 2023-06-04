from sys import argv
from sys import exit as sysexit
from time import sleep
from datetime import datetime
import json
import lzma

import shutil
from pathlib import Path

from highlight import print_err, print_init, print_info

global INTERVAL
global CONFIG

raw_interval = argv[1]

try:
    INTERVAL = float(raw_interval)
    print_init(f"Interval time set to: {INTERVAL} seconds")
except ValueError:
    print_err("Please enter a int/float as interval time!")
    sysexit(64)

try:
    with open("config.json", "r") as config_file:
        CONFIG = json.load(config_file)

    print_init(f"Destination Directory: {CONFIG['backup_dest_dir']}")
    print_init(f"Number of files/folders to backup: {len(CONFIG['files_and_folders'])}")
except json.JSONDecodeError as e:
    print_err(
        f"An error occured while reading the config file!\n"
        f"Message: {e.msg}\nPosition: {e.pos}\nLine: {e.lineno}\nColumn: {e.colno}"
    )
    sysexit(64)
except Exception as e:
    print_err(f"An error occured while reading the config file! Exception:\n{e}")
    sysexit(64)

DEST = Path(CONFIG["backup_dest_dir"])
if not DEST.exists() or not DEST.is_dir():
    print_err("Backup destination folder does not exists! Exiting!")
    sysexit()

paths = []
for p_str in CONFIG["files_and_folders"]:
    p = Path(p_str)
    if p.exists():
        paths.append(p)
    else:
        print_info(f"Path does not exits, not included to backups: {p_str}")
        print_info(f"Absolute path: {p.absolute()}")

if not paths:
    print_err("No valid backup path. Exiting.")
    sysexit(64)

while True:
    try:
        to_be_removed = []

        for p in paths:
            if p.is_dir():
                final_dest = DEST.joinpath(f"{str(p).replace('/', '-')}__{datetime.now().isoformat()}")
                shutil.make_archive(str(final_dest), "xztar", str(p.absolute()))
                print_info(f"{final_dest}.tar.xz")
            elif p.is_file():
                file_data = p.read_bytes()
                compressed_data = lzma.compress(
                    file_data,
                    lzma.FORMAT_XZ,
                    lzma.CHECK_SHA256,
                    9
                )
                final_dest = DEST.joinpath(f"{str(p.absolute()).replace('/', '-')}__{datetime.now().isoformat()}.lzma")
                final_dest.write_bytes(compressed_data)
                print_info(str(final_dest))
            else:
                print_info(f"Unsupported type for {p}. Removing from backup list.")
                to_be_removed.append(p)

        for tbr in to_be_removed:
            paths.remove(tbr)

        print_info("Sleeping...")
        sleep(INTERVAL)
    except KeyboardInterrupt:
        sysexit()
