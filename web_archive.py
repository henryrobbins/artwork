import os
import json
import dmtools
from dmtools import transform
import argparse
from pathlib import Path
from shutil import copyfile

JPEG_QUALITY = 75

def archive_series(series: str):
    """Archive [series] in the web_archive directory."""
    # make subdirectory of archive
    os.makedirs("web_archive" / Path(series), exist_ok=True)
    lbl_json = json.load(open(f"{series}/label.json"))

    # include label.json and description.md in the archive
    lbl_path = Path(series) / "label.json"
    copyfile(lbl_path, "web_archive" / lbl_path)
    description_path = Path(series) / "description.md"
    copyfile(description_path, "web_archive" / description_path)

    # include all works
    for work in lbl_json["works"]:
        from_path = Path(f"{series}/output/{work}")
        to_path = Path(f"{series}/{work}")
        if not from_path.is_file():
            from_path = to_path
        file_extension = from_path.suffix
        if file_extension in [".png", ".pbm", ".pgm", ".ppm"]:
            image = dmtools.read(str(from_path))
            h, w, *_ = image.shape
            max_dim = max(w,h)
            if max_dim < 1028:
                image = transform.rescale(image, k=(1028 / max_dim))
            if max_dim > 2048:
                image = transform.rescale(image, k=(2048 / max_dim))
            to_path = "web_archive" / to_path.with_suffix(".png")
            dmtools.write_png(image, str(to_path))
            jpg_path = to_path.with_suffix(".jpeg")
            # convert to JPEG
            os.system(f"magick '{to_path}' -quality {JPEG_QUALITY} '{jpg_path}'")
            os.system(f"rm '{to_path}'")

        elif file_extension == ".mp4":
            assert work in lbl_json["vimeo"]
        else:
            raise ValueError("Unknown file extension.")


def main(series: str = None):
    """Create a web archive for [series] or all series if [None]."""
    if series is not None:
        archive_series(series)
    else:
        os.makedirs("web_archive", exist_ok=True)
        for series in json.load(open("series.json"))["series"]:
            archive_series(series)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--series", help="Name of series.")
    args = parser.parse_args()
    main(series=args.series)
