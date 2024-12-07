import os
import numpy as np
import dmtools
import imageio
from typing import List

def change(video:List[np.ndarray]) -> np.ndarray:
    output_video = []
    diffs = np.zeros(video[0].shape[0:2])
    for i in range(1,len(video)):
        diff = np.invert(np.all(np.isclose(video[i-1], video[i], atol=0.1), axis=2)).astype(int)
        # diff_3 = np.repeat(diff[:, :, np.newaxis], 3, axis=2)
        diffs = np.clip(diffs + diff, 0, 1)
        diff_3 = np.repeat(diffs[:, :, np.newaxis], 3, axis=2)
        next_frame = (diff_3) * video[-i] # + diffs[:,:,np.newaxis] * np.array([1,0,0])
        output_video.append(dmtools.colorspace.RGB_to_gray(next_frame))
        print(f"{i}/{len(video)}")
    return output_video

pieces = [('nyc', 45),('water1', 15),('water2', 15)]

os.makedirs('output', exist_ok=True)
for name, fps in pieces:
    video = imageio.get_reader(f"input/{name}.mp4",  'ffmpeg')
    video = [video.get_data(i) / 255 for i in range(900)]
    video = change(video)
    dmtools.animation.to_mp4(video, f"output/{name}_change.mp4", fps=fps)
