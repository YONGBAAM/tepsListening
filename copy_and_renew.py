import os
from os.path import join as osj
import shutil
import re
from pydub import AudioSegment
import part34
import numpy as np

import warnings
import time
timechar = '%2d%2d'%(time.localtime().tm_hour, time.localtime().tm_min)
import pandas as pd

JUSTCOPY = False
NO60_ON = False

FORMAT = 'mp3'


rootdir = 'C:\\Users\\jokes\\OneDrive\\Documents\\텝스관련자료\\MP3\\구텝스'

folders = [
    # '넥서스 기출 1 복',
    # '넥서스 기출 2 복',
    # '넥서스 기출 3 복',
    # '해커스 기출 3 복',
    '넥서스 기출 1000L 복', #No60 off

            ]

#루트/폴더 내의 모든 파일은 스플릿이여야 함!



#인트로 추가! p12345

#파트1 6~16 파트2 21~30
#파트3 37 41 42 44 45 메인 코렉2 인퍼2
#파트4 52 56 57 59 60 메 코코 인인

indexes = [6,7,8,9,10,11,12,13,14,15,
           21,22,23,24,25,26,27,28,29,30]

indexes.extend([37,41,42,44,45])
indexes.extend([52,56,57,59,60])
indexes = [('{}'.format(i + 10000))[-2:] for i in indexes]

destdir = osj('./', '구텝스 기출 선별본')

error_list = []

for folder in folders:
    subpath = osj(rootdir, folder)
    subdirs = os.listdir(subpath)
    log_list = []
    for subdir in subdirs:
        mp3s = [n for n in os.listdir(osj(subpath, subdir)) if n[-4:] == '.mp3']

        if not os.path.exists(osj(destdir, folder)):
            os.mkdir(osj(destdir, folder))
        if not os.path.exists(osj(destdir, folder, subdir)):
            os.mkdir(osj(destdir, folder, subdir))
        copyfiles = []
        for n in mp3s:
            nos = re.compile('[0-9]+')
            no = nos.findall(n.split('.')[0])
            if no[-1] in indexes:
                copyfiles.append((n, no[-1]))

        part1_intro = False
        part2_intro = False
        part3_intro = False
        part4_intro = False
        for f in copyfiles:
            ori_name = f[0]
            out_name = '_'.join(ori_name.split('.')[:-1])
            ori_path = osj(subpath, subdir, ori_name)

            question_no = int(f[1])

            print('processing {}\\{}'.format(subdir,out_name))

            if JUSTCOPY:
                shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))
                continue

            if question_no <= 30:
                #part 12
                if question_no <=15:
                    if not part1_intro:
                        shutil.copy('./official/part1_intro_offcial.mp3', osj(destdir, folder, subdir, out_name+'_0' + '.mp3'))
                        shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name+'_1' + '.mp3'))
                        part1_intro = True
                    else:
                        shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))

                elif question_no >=16:
                    if not part2_intro:
                        part2_intro = True
                        shutil.copy('./official/part2_intro_offcial.mp3', osj(destdir, folder, subdir, out_name+'_0' + '.mp3'))
                        shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name+'_1' + '.mp3'))
                    else:
                        shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))


                # shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))

            elif int(f[1]) >= 31:
                if int(f[1]) == 60 and NO60_ON:
                    no60 = True
                else:
                    no60 = False

                if int(f[1]) >= 31 and int(f[1]) <= 45:
                    part4 = False
                    #part3 intro
                    if part3_intro == False:
                        shutil.copy('./official/part3_intro_offcial.mp3', osj(destdir, folder, subdir, out_name+'_0' + '.mp3'))
                        part3_intro = True
                else:
                    part4 = True
                    if part4_intro == False:
                        shutil.copy('./official/part4_intro_offcial.mp3', osj(destdir, folder, subdir, out_name+'_0' + '.mp3'))
                        part4_intro = True

                #processing sound
                try:
                    sound = AudioSegment.from_file(ori_path, format=FORMAT)
                except:
                    warnings.warn('sound open error {}'.format(folder + subdir + out_name))
                    # shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))
                    ed = dict(ori_path = ori_path, dest_path = osj(destdir, folder, subdir), out_name = out_name)
                    error_list.append(ed)
                    continue


                slices ,dur = part34.split_part34_new(sound, time_th=800, no60_last=no60)

                if slices is None:
                    warnings.warn('slicing error'.format(folder + subdir + out_name))
                    ed = dict(ori_path = ori_path, dest_path = osj(destdir, folder, subdir), out_name = out_name)
                    error_list.append(ed)
                    # shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))
                else:
                    diff = np.abs(len(slices[1]) - (len(slices[0])-2000))/1000
                    if diff >=5:
                        warnings.warn('duration no match {}'.format(folder + subdir + out_name))
                        ed = dict(ori_path = ori_path, dest_path = osj(destdir, folder, subdir), out_name = out_name)
                        error_list.append(ed)
                    #shutil.copy(osj(subpath, subdir, f[0]), osj(destdir, folder, subdir, out_name + '.mp3'))

                    else:
                        part34.part3_export(slices, dest=osj(destdir, folder, subdir), ori_name=out_name, part4=part4)
                        log_dict = dict(folder=subdir, no=f[1])
                        for i in range(len(slices)):
                            log_dict['sl{}'.format(i)] = len(slices[i]) / 1000

                        log_dict['dur'] = dur
                        log_dict['diff'] = diff

                        log_list.append(log_dict)



    df = pd.DataFrame(log_list)
    df.to_csv('log_' + folder + '_' + timechar + '.csv', encoding='cp949')

errordf = pd.DataFrame(error_list)
errordf.to_csv('errors' + '_' + timechar + '.csv', encoding='cp949')


