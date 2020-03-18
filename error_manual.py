import os
from os.path import join as osj
import shutil
import re
from pydub import AudioSegment
import part34

JUSTCOPY = False
FORMAT = 'mp3'

TIME_TH = 800

rootdir = 'C:\\Users\\jokes\\OneDrive\\Documents\\텝스관련자료\\MP3\\구텝스'

folders = ['넥서스 텝스 1 복',
            '넥서스 텝스 2 복',
           '넥서스 기출 3 복',
            ]

#루트/폴더 내의 모든 파일은 스플릿이여야 함!



#인트로 추가! p12345

#파트1 6~16 파트2 21~30
#파트3 37 41 42 44 45 메인 코렉2 인퍼2
#파트4 52 56 57 59 60 메 코코 인인




indexes = []
# for i in range(6,16):
#     indexes.append(i)
# for i in range(21,31):
#     indexes.append(i)

indexes.extend([37,41,42,44,45])
indexes.extend([52,56,57,59,60])

indexes = [('{}'.format(i + 10000))[-2:] for i in indexes]
def inindex(name):
    result = False
    for i in indexes:
        if i in name:
            result = i
    return result

destdir = osj('./', '구텝스 기출 선별본')

log_list= []

nos = re.compile('[0-9]+')
import warnings
for folder in folders:
    subpath = osj(rootdir, folder)


    subdirs = os.listdir(subpath)

    for subdir in subdirs:
        mp3s = os.listdir(osj(subpath, subdir))
        if not os.path.exists(osj(destdir, folder)):
            os.mkdir(osj(destdir, folder))
        if not os.path.exists(osj(destdir, folder, subdir)):
            os.mkdir(osj(destdir, folder, subdir))
        copyfiles = []
        for n in mp3s:
            no = nos.findall(n.split('.')[0])
            if no[-1] in indexes:
                copyfiles.append((n, no[-1]))

        #validate
        if not len(copyfiles) == 30:
            for f in copyfiles:
                print(f[0])
            warnings.warn('len is not 30 : it is {} in dir {}'.format(len(copyfiles),subdir))


        for f in copyfiles:
            out_name = subdir + '_' + f[1]
            ori_path = osj(subpath, subdir, f[0])

            print('processing {}\\{}'.format(subdir,out_name))

            if JUSTCOPY:
                shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))
                continue

            if int(f[1]) <= 30:
                #part 12
                shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))
            elif int(f[1]) >= 31 and int(f[1]) <= 45:
                #part3
                sound = AudioSegment.from_file(ori_path, format = FORMAT)
                slices = part34.split_part34(sound, time_th=TIME_TH)
                part34.part3_export(slices, dest=osj(destdir, folder, subdir), ori_name=out_name)
            elif int(f[1]) >= 46:
                if int(f[1]) == 60:
                    no60 = True
                else:
                    no60 = False
                #part4
                sound = AudioSegment.from_file(ori_path, format = FORMAT)
                slices = part34.split_part34(sound, time_th = TIME_TH, no60_last=no60)
                part34.part3_export(slices, dest=osj(destdir, folder, subdir), ori_name=out_name, part4= True)
            log_dict = dict(folder = subdir, )