from sys import argv
import av
import os 
from glob import glob
import cv2 
import numpy as np
from PIL import Image


def sort_files(source):
    paths = dict.fromkeys(source)
    val = []
    f1 = 0
    f2 = 0
    for i in range(len(source)):
        for j in range(len(source[i])):
            if source[i][j-5] + source[i][j-4] + source[i][j-3] + source[i][j-2] + source[i][j-1] + source[i][j] == 'frame_':
                f1 = j 
            if source[i][j] + source[i][j+1] == '.j':
                f2 = j
                break
        val.append(int(source[i][f1+1:f2]))
    for i in range(len(val)):
        paths[list(paths.keys())[i]] = val[i]
    sorted_paths = {}
    sorted_paths = sorted(paths, key=paths.get) 
    sorted_files = list(sorted_paths)
    return sorted_files



numframes = []
flag = False
source = ""
for i in argv:
    if (str(i)[1:8] == "frames=") and flag != True:
        numframes = str(i)[8:].split(',')
        flag = True
    if str(i) == "-i":
        for n in range(len(argv)):
            if str(argv[n]) == "-i":
                source = argv[n+1]
                if flag == True: 
                    break   

numframes = [int(frame) for frame in numframes]
print(numframes)
container = av.open(source)

if not os.path.exists('./frames'):
    os.system('mkdir frames')


for frame in container.decode(video=0):
    if frame.index in numframes:
        frame.to_image().save('./frames/frame_%d.jpg' % frame.index)
        numframes.remove(frame.index)
        print("Кадр %d успешно сохранен." % frame.index)

if len(numframes) != 0:
    for frame in numframes:
        print("Кадр %d не был сохранен!" %frame)

for filename in glob('./frames/*.jpg'):
    os.system('python3 ~/Documents/YOLOX/tools/demo.py image -n yolox-s -c ~/Downloads/yolox_s.pth --path %s \
              --conf 0.25 --nms 0.45 --tsize 640 --save_result --device [cpu/gpu]' % filename)
    

frameSize = (1920, 1080) 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_video.mp4', fourcc, 30, frameSize) 


frames = glob('./YOLOX_outputs/*/*/*/*.jpg')
frames_s = sort_files(frames)

for filename in frames_s: 
    img = cv2.imread(filename) 
    out.write(img) 
    
out.release()

