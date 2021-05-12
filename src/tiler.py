# iteration 1:
# take four images saved in local directory
# save a single tiled image in the local directory

import numpy as np
from PIL import Image

# global vars
size = 136, 136

'''
Crops given 'Image' object to the largest square possible. 
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
Opens the given image file from local directory. 
Returns as an np array of thumbnail size. 
'''
def gen_thumbnail(filename):
    with Image.open(filename) as im:
        im = im.convert("RGBA")
        print(im.size)
        im = crop_square(im)
        im.thumbnail(size)
        a = np.asarray(im)
    return a

if __name__ == "__main__":
    print("hello world!! im tilebot")
    
    # open np thumbnails
    d = gen_thumbnail("./pic/bamboo.jpg")
    a = gen_thumbnail("./pic/coconut.png")
    b = gen_thumbnail("./pic/fish.png")
    c = gen_thumbnail("./pic/shiro.jpg")
    #d = gen_thumbnail("./pic/calico-cat.png")

    lx, ly, lz = a.shape
    bx, by, bz = b.shape
    cx, cy, cz = c.shape
    print(f"A: dim x={lx}, y={ly}, z={lz}")
    print(f"B: dim x={bx}, y={by}, z={bz}")
    print(f"C: dim x={cx}, y={cy}, z={cz}")
    dx, dy, dz = d.shape
    print(f"D: dim x={dx}, y={dy}, z={dz}")
    # clearly, sometimes the dimensions are one pixel off. 

    # TESTTTTTTTT
    row = np.full((100, 20, 4), [255, 255, 255, 0], np.uint8) # must be unsigned integer to use.
    test = np.full((100, 20, 4), [255, 100, 0, 255], np.uint8)
    arr = np.concatenate((row, test, row, test))
    im = Image.fromarray(arr)
    im.save("./pic/TEST.png", "PNG")

    arr = np.concatenate((a, b, c, d))
    arr2 = np.hstack((a, c, d))

    im = Image.fromarray(arr)
    im.save("./pic/merge-thumbnail-2.png", "PNG")
    im = Image.fromarray(arr2)
    im.save("./pic/merge-thumbnail-3.png", "PNG")
