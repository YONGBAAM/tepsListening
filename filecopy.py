import os
from os.path import join as osj
import shutil


rootdir = 'C:\\Users\\jokes\\OneDrive\\Documents\\텝스관련자료\\MP3\\구텝스'

folders = ['넥서스 텝스 1 복',
            '넥서스 텝스 2 복',
           '넥서스 기출 3 복',
            ]

indexes = []
indexes.append(1)
for i in range(6,16):
    indexes.append(i)
indexes.append(16)
for i in range(21,31):
    indexes.append(i)

# indexes.extend([38,39,40,41,42])
indexes.extend([55,56,57,59,60])

indexes = [('{}'.format(i + 10000))[-2:] for i in indexes]

print(indexes)

def inindex(name):
    result = False
    for i in indexes:
        if i in name:
            result = i
    return result

destdir = osj(rootdir, '구텝스 기출 선별본')

for folder in folders:
    subpath = osj(rootdir, folder)


    subdirs = os.listdir(subpath)

    for subdir in subdirs:
        mp3s = os.listdir(osj(subpath, subdir))
        if not os.path.exists(osj(destdir, folder)):
            os.mkdir(osj(destdir, folder))
        if not os.path.exists(osj(destdir, folder, subdir)):
            os.mkdir(osj(destdir, folder, subdir))
        copyfiles = [n for n in mp3s if inindex(n)]
        print(copyfiles)
        for f in copyfiles:
            shutil.copy(osj(subpath, subdir, f), osj(destdir, folder, subdir, f))
