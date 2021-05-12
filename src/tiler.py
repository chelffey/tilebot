# iteration 1:
# take four images saved in local directory
# save a single tiled image in the local directory

import numpy as np
from PIL import Image

# global vars
size = 136, 136

'''
crops to maximum size square, like 'cover'. 
'''
def crop_square(im):
    # crops to square, based on smallest length.
    width, height = im.size
    side_length = min(width, height)
    width_pad = (width - side_length) // 2
    height_pad = (height - side_length) // 2
    left = width_pad
    top = height_pad
    right = width - width_pad
    bottom = height - height_pad 
    return im.crop((left, top, right, bottom))
    # print(f"cropped to width {left}..{right}, height {top}..{bottom}.")
    # print(f"side length: {side_length}")

'''
Crops image to a square. 
Then returns as an np array thumbnail.
'''
def gen_thumbnail(filename):
    with Image.open(filename) as im:
        im = crop_square(im)
        im.thumbnail(size)
        a = np.asarray(im)
    return a

if __name__ == "__main__":
    print("hello world!! im tilebot")
    
    # open np thumbnails
    a = gen_thumbnail("./pic/coconut.png")
    b = gen_thumbnail("./pic/fish.png")


    lx, ly, lz = a.shape
    print(f"dim x={lx}, y={ly}, z={lz}")

    arr = np.concatenate((a, b))
    # arr = np.hstack((a, b), axis=1)

    im = Image.fromarray(arr)
    im.save("./pic/merge-thumbnail-2.png", "PNG")
