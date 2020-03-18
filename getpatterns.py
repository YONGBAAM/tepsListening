import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import warnings
plt.ion()


#f = open('C:/Users/jokes/PycharmProjects/TepsListening/part3_32.mp3', 'rb').read()

sound31 = AudioSegment.from_file('part3_31.mp3', format = 'mp3')
sound32 = AudioSegment.from_file('part3_32.mp3', format = 'mp3')
sound46 = AudioSegment.from_file('part4_46.mp3', format = 'mp3')
sound47 = AudioSegment.from_file('part4_47.mp3', format = 'mp3')

def get_empty(sound, time_th = None, mag_th = 200):

    if type(sound) == type(AudioSegment.empty()):
        sounddata = [d.max for d in sound]

    ind = 0

    if time_th is None:
        time_th = 100
    results = []
    while ind < len(sounddata):
        if sounddata[ind] < mag_th:  # mute:
            start = ind
            end = ind
            for j in range(ind, len(sounddata)):
                if sounddata[j] < mag_th:
                    end = j
                else:
                    break

            ind = end + 1
            if end - start > time_th:
                results.append((end - start, start, end))
        else:
            ind = ind + 1

    return results

def split_part3(sound, partfirst = False, no60 = False):
    mutes = get_empty(sound, time_th=1000)

    #mute갯수가지고 예외처리
    if not partfirst:
        pt_ind = [0,2,4,5,6,7]
        pt_slice = [mutes[i][2] for i in pt_ind]
        pt_slice.insert(0,0)
        pt_slice.append(len(sound))
        dur_slice = [(pt_slice[i],pt_slice[i+1]) for i in range(len(pt_slice)-1)]
        #slices should be 7
    else:
        pt_ind = [-10,-9,-7,-5,-4,-3,-2]
        pt_slice = [mutes[i][2] for i in pt_ind]
        pt_slice.insert(0, 0)
        pt_slice.append(len(sound))
        dur_slice = [(pt_slice[i], pt_slice[i + 1]) for i in range(len(pt_slice) - 1)]
        # slices should be 8
    slices = [sound[s:e+1] for (s,e) in dur_slice]

    return slices

names = [11,12,13,21,22,23,24]
names = ['{}'.format(n) for n in names]

slices = split_part3(sound31, partfirst=True)
ori = '31'
names.insert(0,'00')
for i,s in enumerate(slices):
    s.export(ori + names[i] + '.mp3', format = 'mp3')


# print('total : {}'.format(len(results)))
# for r in results:
#     print('d:%.1f s:%.1f e:%.1f'%(r[0]/1000, r[1]/1000, r[2]/1000))
#
#
# plt.figure()
#
# plt.plot(x, sounddata)
# plt.show()
#
