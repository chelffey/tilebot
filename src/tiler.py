# iteration 1:
# take four images saved in local directory
# save a single tiled image in the local directory

import os
import numpy as np
from PIL import Image
import urllib.request
import validators

# global vars
SIZE = 136, 136
DIFF = 10
ROWSIZE = 4
EMPTY = "empty"

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
    if (ax < side): # not tall enough. add row of (padx x y).
        padx = side - ax
        x1 = padx // 2
        x2 = x1 + padx % 2
        row1 = np.full((x1, ay, 4), [255, 255, 255, 0], np.uint8) 
        row2 = np.full((x2, ay, 4), [255, 255, 255, 0], np.uint8) 
        a = np.concatenate((row1, a, row2))
    elif (ax > side): # too tall, crop. 
        cutoff = side - ax
        a = a[:cutoff]
    if (ay < side): # not wide enough. add col of (pady x side)
        pady = side - ay
        y1 = pady // 2
        y2 = y1 + pady % 2
        col1 = np.full((side, y1, 4), [255, 255, 255, 0], np.uint8) 
        col2 = np.full((side, y2, 4), [255, 255, 255, 0], np.uint8) 
        a = np.hstack((col1, a, col2))
    elif (ay > side): # too wide, crop. 
        cutoff = side - ay
        a = a[:, :cutoff]
    return a


'''
Opens image file from local directory. 
Returns as an np array of thumbnail SIZE, in 4dim RGBA format. 
'''
def gen_thumbnail(filename, default):
    if (filename == EMPTY):
        return default
    
    # save from web into folder if url. 
    if (validators.url(filename)):
        try:
            urllib.request.urlretrieve(filename, ".temp_web_images/temp_image")
            filename = ".temp_web_images/temp_image"
        except:
            return default # if image can't be retrieved. 

    with Image.open(filename) as im:
        im = im.convert("RGBA") # add transparency

        x, y = im.size # scale down to thumbnail.
        tsize = int(SIZE[0] * (max(x, y) / min(x, y)))
        im.thumbnail((tsize, tsize), Image.ANTIALIAS) 

        im = crop_square(im) # THIS LINE: toggle to change whether square or original aspect ratio.
        
        a = np.asarray(im) # create np array from values.
        a = pad_thumbnail(a, SIZE[0]) # for robustness. 
    
    # delete temp saved image
    if (filename == ".temp_web_images/temp_image"):
        os.remove(".temp_web_images/temp_image")
    
    return a


'''
Main functionality. Converts list of filenames into a tiled grid of thumbnails.
Returns as Image object. 
'''
def tile_images(files):
    # initialise transparent padding
    row_space = np.full((DIFF, SIZE[0], 4), [255, 255, 255, 0], np.uint8) 
    col_space = np.full((SIZE[0], DIFF, 4), [255, 255, 255, 0], np.uint8) 
    square = np.full((SIZE[0], SIZE[0], 4), [255, 255, 255, 0], np.uint8)
    row_div = np.full((DIFF, SIZE[0]*ROWSIZE + DIFF*(ROWSIZE-1), 4), [255, 255, 255, 0], np.uint8)

    # initialise folder to save web images into 
    if not os.path.exists('.temp_web_images'):
        os.makedirs('.temp_web_images')

    # reshape 1D file list into 2D structured grid of row length ROWSIZE
    to_add = ROWSIZE - (len(files) % ROWSIZE)
    if to_add != ROWSIZE:
        files.extend([EMPTY]*to_add)
    arr = np.array(files)
    newFiles = arr.reshape(len(files) // ROWSIZE, ROWSIZE)

    # create each row array and add to list.
    rowList = []
    for row in newFiles:
        thisRow = []
        for file in row:
            thisRow.extend([gen_thumbnail(file, square), col_space])
        rowArr = np.hstack([np.array(i) for i in thisRow[:-1]])
        rowList.extend([rowArr, row_div])

    # concat row arrays into a single grid array
    arr = np.concatenate([np.array(i) for i in rowList[:-1]]) # elegant numpy approach: from https://stackoverflow.com/questions/10346336/list-of-lists-into-numpy-array
    im = Image.fromarray(arr)
    return im
    



if __name__ == "__main__":
    print("hello world!! im tilebot")

    files = [
        "./pic/bamboo.jpg",
        "./pic/coconut.png",
        "./pic/fish.png",
        "./pic/shiro.jpg",
        "./pic/calico-cat.png",
        "./pic/ghost.png",
        "./pic/field.jpg",
        "./pic/blue.gif",
        "./pic/boy.jpg"
    ]

    urls = [
        "https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/10/30/8caac9de-1a82-11eb-8f67-a484f6db61a1_image_hires_175647.jpg?itok=T-dFsg-A&v=1604051814",
        "https://www.nme.com/wp-content/uploads/2021/03/Genshin-Impact-miHoYo.jpg",
        "https://www.indiewire.com/wp-content/uploads/2020/12/genshin1.jpg",
        "https://blog.playstation.com/tachyon/2020/11/Featured-Image-Genshin-Impact-update-out-tomorrow.jpg?fit=1024,720",
        "https://cdn.vox-cdn.com/thumbor/pot2y4VQxXpzedEZ8eDMrFR2wLg=/0x308:7680x4320/1200x800/filters:focal(3413x728:4641x1956)/cdn.vox-cdn.com/uploads/chorus_image/image/67716030/ba84dbaad79d15323968a64863c1e069.0.jpg",
        "https://gamerbraves.sgp1.cdn.digitaloceanspaces.com/2020/01/arknights-feature-c.jpg",
        "https://webusstatic.yo-star.com/uy0news/ae/19c9d44c8cf7d7bc770ee588b52dc2e0.png"
    ]

    disc_urls = [
        ""
    ]

    im = tile_images(files)
    im.save("./pic/merge-GRID.png", "PNG")

    im = tile_images(urls)
    im.save("./pic/url_merged_2.png", "PNG")
