# Purpose: takes a list of filenames AND/OR publically accessible urls. 
# Returns a tiled image file of tiles SIZExSIZE, separated by spaces of width 
# DIFF, in rows if length ROWSIZE. 
# files that can't be retrieved are returned blank. 

import os
import numpy as np
from PIL import Image
import urllib.request
import validators

# global vars
EMPTY = "empty"

'''
Crops given 'Image' object to the largest square possible. 
Centers the image. 
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
def gen_thumbnail(filename, tileSize, default):
    if (filename == EMPTY):
        return default
    
    # save from web into folder if url. 
    if (validators.url(filename)):
        try:
            urllib.request.urlretrieve(filename, ".temp_web_images/temp_image")
            filename = ".temp_web_images/temp_image"
        except:
            print("error: url could not be retrieved.")
            return default # if image can't be retrieved. 

    with Image.open(filename) as im:
        im = im.convert("RGBA") # add transparency

        x, y = im.size # scale down to thumbnail.
        tsize = int(tileSize * (max(x, y) / min(x, y)))
        im.thumbnail((tsize, tsize), Image.ANTIALIAS) 

        im = crop_square(im) # THIS LINE: toggle to change whether square or original aspect ratio.
        
        a = np.asarray(im) # create np array from values.
        a = pad_thumbnail(a, tileSize) # for robustness. 
    
    # delete temp saved image
    if (filename == ".temp_web_images/temp_image"):
        os.remove(".temp_web_images/temp_image")
    
    return a


'''
Main functionality. Converts list of filenames into a tiled grid of thumbnails.
Returns as Image object. 
'''
def tile_images(files, tileSize, rowLength, space):
    # initialise transparent padding
    row_space = np.full((space, tileSize, 4), [255, 255, 255, 0], np.uint8) 
    col_space = np.full((tileSize, space, 4), [255, 255, 255, 0], np.uint8) 
    square = np.full((tileSize, tileSize, 4), [255, 255, 255, 0], np.uint8)
    row_div = np.full((space, tileSize*rowLength + space*(rowLength-1), 4), [255, 255, 255, 0], np.uint8)

    # initialise folder to save web images into 
    if not os.path.exists('.temp_web_images'):
        os.makedirs('.temp_web_images')

    # reshape 1D file list into 2D structured grid of row length rowLength
    to_add = rowLength - (len(files) % rowLength)
    if to_add != rowLength:
        files.extend([EMPTY]*to_add)
    arr = np.array(files)
    newFiles = arr.reshape(len(files) // rowLength, rowLength)

    # create each row array and add to list.
    rowList = []
    for row in newFiles:
        thisRow = []
        for file in row:
            thisRow.extend([gen_thumbnail(file, tileSize, square), col_space])
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
        "./pic/bamboo.jpg",
        "./pic/coconut.png",
        "./pic/fish.png",
        "./pic/shiro.jpg",
        "https://cdn.i-scmp.com/sites/default/files/styles/1200x800/public/d8/images/methode/2020/10/30/8caac9de-1a82-11eb-8f67-a484f6db61a1_image_hires_175647.jpg?itok=T-dFsg-A&v=1604051814",
        "https://www.nme.com/wp-content/uploads/2021/03/Genshin-Impact-miHoYo.jpg",
        "https://www.indiewire.com/wp-content/uploads/2020/12/genshin1.jpg",
        "./pic/calico-cat.png",
        "./pic/ghost.png",
        "./pic/field.jpg",
        "./pic/blue.gif",
        "./pic/boy.jpg",
        "https://blog.playstation.com/tachyon/2020/11/Featured-Image-Genshin-Impact-update-out-tomorrow.jpg?fit=1024,720",
        "https://cdn.vox-cdn.com/thumbor/pot2y4VQxXpzedEZ8eDMrFR2wLg=/0x308:7680x4320/1200x800/filters:focal(3413x728:4641x1956)/cdn.vox-cdn.com/uploads/chorus_image/image/67716030/ba84dbaad79d15323968a64863c1e069.0.jpg",
        "https://gamerbraves.sgp1.cdn.digitaloceanspaces.com/2020/01/arknights-feature-c.jpg",
        "https://webusstatic.yo-star.com/uy0news/ae/19c9d44c8cf7d7bc770ee588b52dc2e0.png"
    ]

    # doesn't work - these urls aren't publically accessible. 
    disc_urls = [
        "https://cdn.discordapp.com/attachments/841255574330408981/841266535376486460/EzFyC5ZVcAA1-_m.jpg",
        "https://cdn.discordapp.com/attachments/841255574330408981/841266037214806046/Elu0GiWVkAEzrHm.png",
        "https://cdn.discordapp.com/attachments/841255574330408981/841265455237824512/tumblr_nayd2yGcBC1rscimho1_500.png"
    ]

    tilesize = 136
    rowlength = 6
    spacing = 4

    im = tile_images(files, tilesize, rowlength, spacing)
    im.save("./pic/merge-GRID.png", "PNG")

    im = tile_images(urls, tilesize, rowlength, spacing)
    im.save("./pic/url_merged_2.png", "PNG")
