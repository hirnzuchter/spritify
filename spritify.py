from PIL import Image
import numpy as np
import cv2
import random

def reduce(image, height, width=None, pad=0):
    '''
    # Image
    The image you want to reduce.
    # Height and Width
    Height will be the height of the reduced image. If a width is not provided, the reduced
    image preserves the aspect ratio of the original.
    # Pad
    Pad is how much you want to pad the right and bottom sides to reduce the full image. If
    the full image is not shown in the reduced image, gradually add padding.
    '''
    image = np.array(image)
    imgh, imgw, c = image.shape
    if width == None:
        width = int(height/imgh*imgw)
    image = np.concatenate((image, np.zeros((imgh, int(pad*imgw/imgh), c))), axis=1)
    image = np.concatenate((image, np.zeros((pad, image.shape[1], c))), axis=0)
    imgh, imgw, c = image.shape
    dy = imgh//height
    dx = imgw//width
    out = np.zeros((height, width, c)).astype(np.uint8)
    for i in range(height):
        for j in range(width):
            out[i][j] = image[i*dy][j*dx]
    out = Image.fromarray(out)
    return out

def expand(reduced, scale):
    image = np.array(reduced)
    imgh, imgw, c = image.shape
    h = scale*imgh
    w = scale*imgw
    out = np.zeros((h, w, c)).astype(np.uint8)
    for i in range(h):
        for j in range(w):
            out[i][j] = image[i//scale][j//scale]
    out = Image.fromarray(out)
    return out

def expand_to_size(reduced, size):
    size = (size, size)
    image = np.array(reduced)
    imgh, imgw, c = image.shape
    dy = size[0]//imgh
    dx = size[1]//imgw
    out = np.zeros((size[0], size[1], c)).astype(np.uint8)
    for i in range(size[0]):
        for j in range(size[1]):
            try:
                out[i][j] = image[i//dy][j//dx]
            except:
                break
    out = Image.fromarray(out)
    return out

def palette_swap_closest(image, palette):
    '''The palette argument should be a (n, 4) array'''
    palette = np.array(palette)
    image = np.array(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            mse = []
            for color in palette:
                mse.append(np.linalg.norm(image[i][j][:3]-color))
            mse = np.array(mse)
            image[i][j][:3] = palette[np.argmin(mse)]
    image = Image.fromarray(image)
    return image

def palette_swap_pair(image, color1, color2):
    image = np.array(image)
    color1 = np.array(color1)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i][j][0] == color1[0] and image[i][j][1] == color1[1] and image[i][j][2] == color1[2] and image[i][j][3] == color1[3]:
                image[i][j] = np.array(color2)
    image = Image.fromarray(image)
    return image

def pixify_video(video, size, output_size):
    '''works best for mp4 input files'''
    cap = cv2.VideoCapture(video)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60, (output_size, output_size))
    for _ in range(frames):
        frame = Image.fromarray(cap.read()[1])
        out.write(np.array(expand_to_size(reduce(frame, height=size), output_size)))
    cap.release()
    out.release()

def make_frames(video, size, output_size, dir=".", increment=1):
    '''works best for mp4 input files
    Make it so that the frames aren't randomly indexed, for animation purposes.
    '''
    cap = cv2.VideoCapture(video)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for iter in range(frames):
        if iter % increment == 0:
            frame = cap.read()[1]
            frame[:, :, [0, 2]] = frame[:, :, [2, 0]]
            frame = Image.fromarray(frame)
            frame = expand(reduce(frame, height=size), output_size)
            frame.save(f"{dir}/{random.randint(0, 999999)}.jpg")
    cap.release()

def make_frames_reduced(video, size, dir=".", increment=1):
    '''works best for mp4 input files.
    Make it so that the frames aren't randomly indexed, for animation purposes.
    '''
    cap = cv2.VideoCapture(video)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for iter in range(frames):
        if iter % increment == 0:
            frame = cap.read()[1]
            frame[:, :, [0, 2]] = frame[:, :, [2, 0]]
            frame = Image.fromarray(frame)
            frame = reduce(frame, height=size)
            frame.save(f"{dir}/{random.randint(0, 999999)}.jpg")
    cap.release()

#Example Palette
step = 40
palette = []
for i in range(0, 255, step):
    for j in range(0, 255, step):
        for k in range(0, 255, step):
            palette.append([i, j, k])