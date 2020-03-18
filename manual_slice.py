import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import warnings
from os.path import join as osj
import msvcrt
from part34 import get_empty, make_duration
from playsound import playsound
import time


def slice_point(dur, select):
    slicepoint = [
        dur[select[0]][0],
        dur[select[1]][0],
        dur[select[2]][0],
        dur[select[3]][1]

    ]
    return slicepoint
def manual_slice(sound, fig,default = (2,4), no60 = False):
    mutes = get_empty(sound, time_th=800)
    dur = make_duration(mutes)

    lt = time.localtime()
    timechar = '%2d%2d' % (lt.tm_min, lt.tm_sec)

    sounddata = [s.max_dBFS for s in sound]

    temp_dir = './tempwav'

    temp_paths = []
    for i, d in enumerate(dur):
        temp_path = osj(temp_dir, 'temp{}'.format(i) + '_' + timechar + '.wav')
        temp_paths.append(temp_path)

        sound[d[0]:d[0] + 1000].export(temp_path, format='wav')

    ax = fig.add_subplot(111)
    ax.set_xlim(0, len(sounddata))
    ax.plot(sounddata, 'b', alpha=0.5)

    select = np.array((0, default[0],default[1], len(dur) - 1))

    slicepoint = slice_point(dur,select)
    seldot, = ax.plot(slicepoint, np.zeros(4), 'go', markersize=3)
    for i, d in enumerate(dur):

        plt.axvspan(d[0], d[0] + 20, color='red', alpha=1)
        if i % 2 == 0:
            plt.axvspan(d[0], d[1], color='yellow', alpha=0.2)
        else:
            plt.axvspan(d[0], d[1], color='green', alpha=0.2)

    # interactive plot
    Ln, = ax.plot(sounddata, 'r')
    plt.pause(0.2)

    current_i = select[1]
    d = dur[current_i]
    Ln.set_xdata(range(d[0], d[1], 1))
    Ln.set_ydata(sounddata[d[0]:d[1]])
    plt.pause(0.2)
    playsound(temp_paths[current_i])

    current_i = select[2]
    d = dur[current_i]
    Ln.set_xdata(range(d[0], d[1], 1))
    Ln.set_ydata(sounddata[d[0]:d[1]])
    plt.pause(0.2)
    playsound(temp_paths[current_i])


    end = False
    current_i = 0
    while not end:
        c = input('adrtfeh current: {} {} {} {}'.format(*select))
        imax = len(dur) - 1
        try:
            current_i = int(c)
            current_i = np.clip(current_i, 0, imax)
        except:
            if c == 'a':
                current_i = np.clip(current_i - 1, 0, imax)
            elif c == 'd':
                current_i = np.clip(current_i + 1, 0, imax)
            elif c == 'r':
                select[1] = current_i

                seldot.set_data(slice_point(dur,select), np.zeros(4))
                print('select blk {},{}'.format(select[1], select[2]))
            elif c == 't':
                select[2] = current_i

                seldot.set_data(slice_point(dur,select), np.zeros(4))
                print('select blk {},{}'.format(select[1], select[2]))

            elif c == 'f':
                select[0] = current_i

                seldot.set_data(slice_point(dur,select), np.zeros(4))
                print('first')
                # 해당블록 시작으로 지정
            elif c == 'e':
                select[3] = current_i
                seldot.set_data(slice_point(dur,select), np.zeros(4))
                print('end blk {}'.format(select[3]))

                # 해당블록 끝으로 지정
            elif c == 'h':
                playsound(temp_paths[select[1]])
                playsound(temp_paths[select[2]])

                plt.clf()
                break

        d = dur[current_i]
        Ln.set_xdata(range(d[0], d[1], 1))
        Ln.set_ydata(sounddata[d[0]:d[1]])
        plt.pause(0.2)
        playsound(temp_paths[current_i])

    slicepoint = slice_point(dur, select)
    return slicepoint


if __name__ == '__main__':
    plt.ion()
    plt.rcParams["figure.figsize"] = [20, 1.5]
    sound = AudioSegment.from_file('./60.mp3', format = 'mp3')
    fig = plt.figure()

    import pandas as pd
    import part34
    import re
    df = pd.read_csv('./errors_ 042.csv', encoding = 'cp949')
    for i in range(len(df)):
        d = df.iloc[i]
        ori = d['ori_path']
        dest = d['dest_path']
        out_name = d['out_name']

        sound = AudioSegment.from_file(ori)
        slicepoint = manual_slice(sound, fig, no60=False)

        s1 = sound[slicepoint[0]:slicepoint[1]]
        s2 = sound[slicepoint[1]:slicepoint[2]]
        s5 = sound[slicepoint[2]:slicepoint[3]]

        nos = re.compile('[0-9]+')
        no = nos.findall(out_name.split('.')[0])
        if len(no) >0:
            q_no = int(no[-1])
        else:
            q_no = 59

        if q_no <=45:
            part4 = False
            print('exporting P3 {},{}'.format(dest, out_name))

        else:
            part4 = True
            print('exporting P4 {},{}'.format(dest, out_name))

        part34.part3_export([s1,s2,s5],dest,out_name, part4=part4)