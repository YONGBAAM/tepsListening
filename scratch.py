import os
from os.path import join as osj
import shutil
import re
from pydub import AudioSegment
from part34 import get_empty, print_mutes
import numpy as np

def split_part34_new(sound, partfirst = False,manual_dur = False, no60_last = False, time_th = 1500, mode = None):
    #new algo
    mutes = get_empty(sound, time_th=250)

    pt_slice = [m[2] for m in mutes]
    pt_slice.insert(0, 0)
    dur_slice_all = [(pt_slice[i],pt_slice[i+1],pt_slice[i+1]-pt_slice[i]) for i in range(len(pt_slice)-1)]

    error = False
    if partfirst:
        m_coarse = get_empty(sound[20000:], time_th=1000)
        if m_coarse[0][1] < 1000:
            m_coarse = m_coarse[1:]
        tempp = [m[2] for m in mutes]
        tempp.insert(0, 0)
        tempdur = [(pt_slice[i], pt_slice[i + 1], pt_slice[i + 1] - pt_slice[i]) for i in
                   range(len(pt_slice) - 1)]

        if tempdur[2][2] > 10000:
            number_ind = 1
        else:
            number_ind = 0

        number_start = tempdur[number_ind][0]
        number_end = tempdur[number_ind][1]

    elif no60_last:
        # last_question 찾기
        last_index = -1
        for i in range(-1, -5, -1):
            if dur_slice_all[i][2] < 1000:
                last_index = i + 1
                break

        dur_slice_all = dur_slice_all[:last_index + 1]

        number_start=0
        number_end = dur_slice_all[0][1]
    else:
        # 마지막 10블록 제거
        number_start = 0
        number_end = dur_slice_all[0][1]

    bogi_start = dur_slice_all[-8][0]
    bogi_end = dur_slice_all[-1][1]
    # all 5 question should be lower
    for i in range(5):
        if not dur_slice_all[-10 + 2 * i][2] < 1000:
            print('question part detection failed')
            return None, dur_slice_all

    # all 5 question should be lower
    for i in range(5):
        if not dur_slice_all[-10 + 2 * i][2] < 1000:
            print('question part detection failed')
            return None, dur_slice_all

    # 가장 가까운거 선택
    pt_slice = [m[2] for m in mutes if m[0] >= time_th]
    pt_slice.insert(0, 0)
    dur_slice = [(pt_slice[i], pt_slice[i + 1], pt_slice[i + 1] - pt_slice[i]) for i in
                 range(len(pt_slice) - 1)]

    q_length = number_end - bogi_start
    mid = q_length / 2 + number_end
    endpoints = [d[1] for d in dur_slice]
    split = int(np.argmin(np.abs(np.array(endpoints) - mid)))

    slices = []
    slices.append(sound[number_start:dur_slice[split][1]])
    slices.append(sound[dur_slice[split][1]:bogi_start])
    slices.append(sound[bogi_start:bogi_end])



    return slices, dur_slice_all

sound = AudioSegment.from_file('./60.mp3')
mutes = get_empty(sound, time_th=400)
print_mutes(mutes)
slice = split_part34_new(sound, time_th= 1500)
#part34.part3_export(slice, dest = './', ori_name= 'test32', part4=True)