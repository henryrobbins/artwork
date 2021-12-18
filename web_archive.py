import os
import json
import dmtools
from dmtools import transform
from pathlib import Path
from shutil import copyfile


os.makedirs('web_archive', exist_ok=True)
for series in json.load(open("series.json"))["series"]:
    # create subdirectory of archive
    os.makedirs('web_archive' / Path(series), exist_ok=True)
    lbl_json = json.load(open("%s/label.json" % series))

    # include label.json and description.md in the archive
    lbl_path = Path(series) / 'label.json'
    copyfile(lbl_path, 'web_archive' / lbl_path)
    description_path = Path(series) / 'description.md'
    copyfile(description_path, 'web_archive' / description_path)

    # include all works
    for work in lbl_json['works']:
        from_path = Path('%s/output/%s' % (series, work))
        to_path = Path('%s/%s' % (series, work))
        if not from_path.is_file():
            from_path = to_path
        file_extension = from_path.suffix
        if file_extension == '.png':
            copyfile(from_path, 'web_archive' / to_path)
        elif file_extension == '.mp4':
            assert work in lbl_json['vimeo']
        elif file_extension in ['.pbm', '.pgm', '.ppm']:
            image = dmtools.read_netpbm(str(from_path))
            h, w, *_ = image.shape
            max_dim = max(w,h)
            if max_dim < 1000:
                image = transform.rescale(image, int(1000 / max_dim))
            to_path = 'web_archive' / to_path.with_suffix('.png')
            dmtools.write_png(image, str(to_path))
        else:
            raise ValueError('Unknown file extension.')
