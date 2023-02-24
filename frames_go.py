from sys import argv
import av


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

for frame in container.decode(video=0):
    if frame.index in numframes:
        frame.to_image().save('frame_%d.jpg' % frame.index)
        numframes.remove(frame.index)
        print("Кадр %d успешно сохранен." % frame.index)

if len(numframes) != 0:
    for frame in numframes:
        print("Кадр %d не был сохранен!" %frame)
