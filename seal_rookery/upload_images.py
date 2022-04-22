import argparse
import glob
import json
import os
from pathlib import Path

import boto3
import pyvips
from boto3.s3.transfer import S3Transfer
from PIL import Image
from resizeimage import resizeimage

sizes = ["128", "256", "512", "1024", "orig"]

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR.split("/")[-1] != "seal_rookery":
    raise "Please run update from the seal_rookery directory"


def upload(file_path, aws_path, access_key, secret_key) -> None:
    """Uploads a file to an S3 bucket.

    :param file_path: File to upload
    :param aws_path: The path in the S3 bucket
    :param access_key: The access key for the S3
    :param secret_key: The secret key for the S3
    :return: None
    """
    # bucket = "dev-com-courtlistener-storage"
    bucket = "seals.free.law"
    client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    transfer = S3Transfer(client)
    if ".png" in file_path:
        content_type = "image/png"
    else:
        content_type = "image/svg+xml"
    transfer.upload_file(
        file_path,
        bucket,
        aws_path,
        extra_args={"ContentType": content_type, "ACL": "public-read"},
    )
    print(f"http://{bucket}.s3-us-west-2.amazonaws.com/{aws_path}")


def resize_image(original: str, size: str) -> str:
    """Resize an image.

    :param original: The path to the original image
    :param size: The size of the image width to resize
    :return: The path to the new resized image
    """
    new_filepath = original.replace("orig", size)
    if not os.path.exists(os.path.dirname(new_filepath)):
        os.mkdir(os.path.dirname(new_filepath))

    svg = True if "svg" in original else False
    if svg:

        image = pyvips.Image.thumbnail(original, int(size), height=int(size))
        new_filepath = new_filepath.replace(".svg", ".png")
        image.write_to_file(new_filepath)
    else:
        with open(original, "r+b") as f:
            with Image.open(f) as image:
                width, height = image.size
                if height < int(size):
                    ratio_height = (int(size) / width) * height
                    cover = resizeimage.resize_cover(
                        image, [int(size), ratio_height], validate=False
                    )
                else:
                    if width > height:
                        cover = resizeimage.resize_height(
                            image, int(size), validate=False
                        )
                    else:
                        cover = resizeimage.resize_width(
                            image, int(size), validate=False
                        )
                cover.save(new_filepath, image.format)
    return new_filepath


def validate_json() -> bool:
    """Validate the json file contains our new Seals

    :return: True if valid, else Raises an exception
    """
    with Path(ROOT_DIR, "seals", "seals.json").open() as f:
        seals = json.load(f)

    seals_in_json = [k for k, v in seals.items() if v["has_seal"]]

    seals = [
        x.split("/")[-1][:-4] for x in glob.glob(f"{ROOT_DIR}/seals/orig/*")
    ]
    missing_seals = sorted(list(set(seals_in_json) ^ set(seals)))
    if not missing_seals:
        return True

    raise Exception(f"Missing entry for: {' '.join(missing_seals)}")


def find_new_seals(access_key: str, secret_key: str) -> list:
    """Compare s3 and local to find new portraits.

    :param access_key: Access key
    :param secret_key: Secret key
    :return: List of new portraits to process
    """
    session = boto3.Session(
        aws_access_key_id=access_key, aws_secret_access_key=secret_key
    )
    s3 = session.resource("s3")
    bucket = s3.Bucket("seals.free.law")
    aws_seals = [
        x.key.split("/")[-1] for x in bucket.objects.filter(Prefix="v2/orig/")
    ]
    local_seals = [
        x.split("/")[-1] for x in glob.glob(f"{ROOT_DIR}/seals/orig/*")
    ]
    seals_to_upload = set(aws_seals) ^ set(local_seals)
    return sorted(list(seals_to_upload))


def main(access_key: str, secret_key: str) -> None:
    """Resize and upload new portraits to S3.

    :param access_key: The s3 access key
    :param secret_key: The s3 secret key
    :return: None
    """
    # Check for duplicate seals files
    validate_json()

    # Check for files we need to upload
    seals_to_upload = find_new_seals(access_key, secret_key)

    # Generate new file sizes and upload them to the server
    for seal in list(seals_to_upload):
        print(f"Seal: {seal}")
        fn = seal.split("/")[-1]
        for size in sizes:
            orig = f"{ROOT_DIR}/seals/orig/{fn}"
            fp = f"{ROOT_DIR}/seals/{size}/{fn}"
            aws_path = f"v2/{size}/{fn}"

            if size == "orig":
                print(f"Uploading to: https://seals.free.law/{aws_path}")
                upload(orig, aws_path, access_key, secret_key)
            else:
                resize_image(orig, size)
                aws_path = aws_path.replace(".svg", ".png")
                fp = fp.replace(".svg", ".png")
                print(f"Uploading to: https://seals.free.law/{aws_path}")
                upload(fp, aws_path, access_key, secret_key)


if __name__ == "__main__":
    # This is mostly meant to be called from the github action but it could be
    # called locally with the correct credentials.
    parse = argparse.ArgumentParser(description="Create a new seal")
    parse.add_argument(
        "--access-key", "-a", help="The access key", required=True
    )
    parse.add_argument(
        "--secret-key", "-s", help="The secret key", required=True
    )
    args = parse.parse_args()
    main(access_key=args.access_key, secret_key=args.secret_key)
