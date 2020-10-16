#!/usr/bin/env python -i
import argparse
import hashlib
import json
import os
import subprocess
import sys
from multiprocessing import Pool, cpu_count

from seal_rookery import seals_root, seals_data

args = None


class BadResultError(Exception):
    pass


ORIG_DIR = os.path.join(seals_root, "orig")


def get_old_hash(img):
    """Get the old hash from seals.json"""
    try:
        old_hash = seals_data[img.split(".")[0]]["hash"]
    except KeyError:
        old_hash = None
    return old_hash


def get_hash_from_file(img):
    """Get the hash from the current file"""
    with open(img, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def set_new_hash(court_id, new_hash):
    """Update the json object with new values"""
    seals_data[court_id]["hash"] = new_hash


def resize_image(orig, output, size, verbosity):
    if verbosity > 1:
        msg = "  - Making {size}x{size} image...".format(size=size)
        sys.stdout.write(msg)
    command = [
        "convert",
        orig,
        "-resize",
        "{}x{}".format(size, size),
        "-background",
        "transparent",
        output,
    ]
    rc = subprocess.run(command, shell=False)
    if verbosity > 1:
        msg = " - writing to {}".format(output)
        sys.stdout.write(msg)
    return rc


def convert_image(image, count, total):
    if args.verbose:
        sys.stdout.write(u"\nProcessing: {}".format(image))
    else:
        sys.stdout.write(u"\rUpdating seals: {} of {}".format(count, total))
        sys.stdout.flush()
    court_id = image.split(".")[0]
    final_name = "{}.png".format(court_id)
    path_to_orig = os.path.join(ORIG_DIR, image)
    current_hash = get_hash_from_file(path_to_orig)
    old_hash = get_old_hash(image)
    if current_hash != old_hash or args.forced:
        set_new_hash(court_id, current_hash)
        sizes = ["128", "256", "512", "1024"]
        resize_args = [
            (
                path_to_orig,
                os.path.join(seals_root, size, final_name),
                size,
                args.verbose,
            )
            for size in sizes
            if not os.path.exists(os.path.join(seals_root, size, final_name))
            or args.forced
        ]
        with Pool(args.numprocs) as p:
            p.starmap(resize_image, resize_args)
        return "changed", resize_args
    else:
        return "skipped", list()


def convert_images():
    """
    Convert the original seal images to their different scaled outputs for
    use either in CourtListener or another application.

    :return: tuple (number changed, number skipped)
    """
    images = os.listdir(ORIG_DIR)
    num_images = len(images)
    num_changed = 0
    num_skipped = 0
    resize_args = list()
    for index, image in enumerate(images, 1):
        result, rsargs = convert_image(image, index, num_images)
        if result == "changed":
            num_changed += 1
        elif result == "skipped":
            if args.verbose:
                msg = " - Unchanged hash, moving on."
                sys.stdout.write(msg)
            num_skipped += 1
        else:
            raise BadResultError("bad result {}".format(result))
        resize_args += rsargs
    if args.verbose:
        sys.stdout.write("\n")
    # with Pool(args.numprocs) as p:
    #    p.starmap(resize_image, resize_args)
    if not args.verbose:
        msg = "\nDone:\n  {} seals updated\n  {} seals skipped\n"
        sys.stdout.write(msg.format(num_changed, num_skipped))
    return num_changed, num_skipped


def save_new_json():
    """Update the JSON object on disk."""
    json.dump(
        seals_data,
        open(os.path.join(seals_root, "seals.json"), "w"),
        sort_keys=True,
        indent=4,
    )


def main(argv=None):
    """
    Main function and entry point for console script
    :param argv: list of command line args, probably from sys.argv
    :return: tuple (number of changed images, number of skipped images)
    """
    # when running as a console_script via setuptools, no args are passed,
    # so we need to try grabbing sys.argv
    parser = argparse.ArgumentParser(prog="update-seals")
    parser.add_argument(
        "-f",
        dest="forced",
        default=False,
        action="store_true",
        help="force seal update or regeneration",
    )
    parser.add_argument(
        "-v",
        dest="verbose",
        default=0,
        action="count",
        help="turn on verbose seal generation messages",
    )
    parser.add_argument(
        "-j",
        dest="numprocs",
        type=int,
        default=cpu_count(),
        help="Use multiple processes to convert images.",
    )
    global args
    args = parser.parse_args(argv)
    try:
        changed, skipped = convert_images()
        save_new_json()
    except Exception as error:
        # Note: will not catch SystemExit from parser.parse_args
        print("Failed to update seals!")
        print(str(error))
        return 1
    return 0


if __name__ == "__main__":
    main(sys.argv)
