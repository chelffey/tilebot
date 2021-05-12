# iteration 1:
# take four images saved in local directory
# save a single tiled image in the local directory

import numpy as np
from PIL import Image

# global vars
SIZE = 136, 136
DIFF = 20

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


'''
Purpose: transparent-pads images to precisely correct size. Robustness for images that are too small, or one pixel off the correct size. 
Input: a = a numpy array representing thumbnail. 
    Assumption: thumbnail x, y dim are NO GREATER than size. 
side = desired side length. 
Returns thumbnail of precisely (SIZE x SIZE x 4).
Padding will CENTRE the thumbnail. 
'''
def pad_thumbnail(a, side):
    ax, ay, az = a.shape   
    if (ax != side): # not tall enough. add row of (padx x y).
        padx = side - ax
        x1 = padx // 2
        x2 = x1 + padx % 2
        row1 = np.full((x1, ay, 4), [255, 255, 255, 0], np.uint8) 
        row2 = np.full((x2, ay, 4), [255, 255, 255, 0], np.uint8) 
        a = np.concatenate((row1, a, row2))
    if (ay != side): # not wide enough. add col of (pady x side)
        pady = side - ay
        y1 = pady // 2
        y2 = y1 + pady % 2
        col1 = np.full((side, y1, 4), [255, 255, 255, 0], np.uint8) 
        col2 = np.full((side, y2, 4), [255, 255, 255, 0], np.uint8) 
        a = np.hstack((col1, a, col2))
    return a


'''
Opens image file from local directory. 
Returns as an np array of thumbnail SIZE, in 4dim RGBA format. 
'''
def gen_thumbnail(filename):
    with Image.open(filename) as im:
        im = im.convert("RGBA") # add transparency
        # THIS LINE: toggle to change whether square or original aspect ratio.
        # im = crop_square(im) # crop to square, 'cover'. 
        im.thumbnail(SIZE) # scale down to thumbnail.
        a = np.asarray(im) # create np array from values.
        a = pad_thumbnail(a, SIZE[0]) # for robustness. 
    return a




if __name__ == "__main__":
    print("hello world!! im tilebot")
    
    # initialise transparent padding 
    row = np.full((DIFF, SIZE[0], 4), [255, 255, 255, 0], np.uint8) 
    col = np.full((SIZE[0], DIFF, 4), [255, 255, 255, 0], np.uint8) 
    square = np.full((SIZE[0], SIZE[0], 4), [255, 255, 255, 0], np.uint8)

    files = [
        "./pic/bamboo.jpg",
        "./pic/coconut.png",
        "./pic/fish.png",
        "./pic/shiro.jpg",
        "./pic/calico-cat.png",
        "./pic/ghost.png"
    ]

    # open files, create thumbnail album, save. 
    # arr = None
    # for file in files:
    #     a = gen_thumbnail(file)
    #     print(f"dim {a.shape}")
    #     if arr is None:
    #         arr = a
    #     else:
    #         arr = np.concatenate((arr, row, a))
    # im = Image.fromarray(arr)
    # im.save("./pic/merge-auto.png", "PNG")

    # same, but save in ROWS OF GIVEN LENGTH
    ROWSIZE = 4
    EMPTY = "empty"

    # transform file list into structured grid of row length ROWSIZE
    to_add = ROWSIZE - (len(files) % ROWSIZE)
    if to_add != ROWSIZE:
        files.extend([EMPTY]*to_add)
    arr = np.array(files)
    newFiles = arr.reshape(len(files) // ROWSIZE, ROWSIZE)
    print(newFiles)

    # # run. 
    # arr = None
    # for file in files:
    #     a = gen_thumbnail(file)
    #     print(f"dim {a.shape}")
    #     if arr is None:
    #         arr = a
    #     else:
    #         arr = np.concatenate((arr, row, a))
    # im = Image.fromarray(arr)
    # im.save("./pic/merge-auto.png", "PNG")

    # OLD----
    # arr = np.concatenate((a, row, b, row, c, row, d, row, e, row, f))
    # arr2 = np.hstack((a, col, b, col, c, col, d, col, e, col, f))

    # im = Image.fromarray(arr)
    # im.save("./pic/merge-thumbnail-2.png", "PNG")
    # im = Image.fromarray(arr2)
    # im.save("./pic/merge-thumbnail-3.png", "PNG")
