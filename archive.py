import os
import dmtools
from dmtools import transform
from pathlib import Path
from shutil import copyfile

# VIMEO ID for all .mp4 files
VIMEO_ID = {
    "format.mp4" : "543896900",
    "faces_mod_animation.mp4" : "544012195",
    "water_cup_mod_animation.mp4" : "544012231",
    "stewart_pinches_chaos.mp4" : "544260565",
    "stewart_rgb_chaos.mp4" : "544260549",
    "stewart_clip.mp4" : "544260538",
    "stewart_mod.mp4" : "544260328",
    "stewart_film.mp4" : "544732299",
    "node_conway_animation.mp4" : "544390242",
    "node_reverse_conway_animation.mp4" : "544390256",
    "rhizomes_conway_animation.mp4" : "544645491",
    "rhizomes_reverse_conway_animation.mp4" : "544649676"
}

os.makedirs('archive', exist_ok=True)
for root, _, files in os.walk('.'):
    if "works.txt" in files:
        with open("%s/works.txt" % root, 'r') as works_file:
            # Include README.md in the archive
            os.makedirs('archive' / Path(root), exist_ok=True)
            readme_path = Path(root) / 'README.md'
            copyfile(readme_path, 'archive' / readme_path)

            # Include vimeo.txt file in the archive
            videos = []
            vimeo_path = Path(root) / 'vimeo.txt'
            if vimeo_path.exists():
                copyfile(vimeo_path, 'archive' / vimeo_path)
                with open(vimeo_path, 'r') as f:
                    videos = [line.split("=")[0] for line in f.readlines()]

            # Include the .png and .mp4 format of all works
            works = works_file.read().split("\n")
            works = list(filter(lambda x: x != "", works))
            for work in works:
                path = Path('%s/%s' % (root, work))
                file_extension = path.suffix
                if file_extension == '.png':
                    copyfile(path, 'archive' / path)
                elif file_extension == '.mp4':
                    assert work in videos
                elif file_extension in ['.pbm', '.pgm', '.ppm']:
                    image = dmtools.read_netpbm(path)
                    h, w, *_ = image.shape
                    max_dim = max(w,h)
                    if max_dim < 1000:
                        image = transform.rescale(image, int(1000 / max_dim))
                    path = 'archive' / path.with_suffix('.png')
                    dmtools.write_png(image, path)
                else:
                    raise ValueError('Unknown file extension.')
