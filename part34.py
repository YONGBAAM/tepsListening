import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import warnings
from os.path import join as osj


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

def print_mutes(results):
    for r in results:
        print('d:%.1f s:%.1f e:%.1f' % (r[0] / 1000, r[1] / 1000, r[2] / 1000))

def make_duration(mutes):
    pt_slice = [m[2] for m in mutes]
    pt_slice.insert(0, 0)
    dur_slice_all = [(pt_slice[i],pt_slice[i+1],pt_slice[i+1]-pt_slice[i]) for i in range(len(pt_slice)-1)]
    return dur_slice_all


def split_part34_new(sound, partfirst = False,manual_dur = False, no60_last = False, time_th = 1500, mode = None):
    #new algo
    mutes = get_empty(sound, time_th=250)
    dur_slice_all = make_duration(mutes)

    error = False
    if partfirst:
        m_coarse = get_empty(sound[20000:], time_th=1000)
        if m_coarse[0][1] < 1000:
            m_coarse = m_coarse[1:]
        tempdur = make_duration(m_coarse)

        if tempdur[2][2] > 10000:
            number_ind = 1
        else:
            number_ind = 0

        number_start = tempdur[number_ind][0]
        number_end = tempdur[number_ind][1]

    elif no60_last:
        # last_question 찾기
        for i in range(-2, -6, -1):
            if dur_slice_all[i][2] < 2000:
                last_index = i + 1
                dur_slice_all = dur_slice_all[:last_index + 1]
                break

        number_start=0
        number_end = dur_slice_all[0][1]
    else:
        # 마지막 10블록 제거
        number_start = 0
        number_end = dur_slice_all[0][1]

    bogi_start = dur_slice_all[-8][0]
    bogi_end = dur_slice_all[-1][1]
    # all 4 question should be lower
    for i in range(4):
        if not dur_slice_all[-8 + 2 * i][2] < 2000:
            print('question part detection failed')
            return None, dur_slice_all

    # 가장 가까운거 선택
    dur_slice = make_duration(get_empty(sound, time_th=time_th))
    q_length = bogi_start - number_end
    mid = q_length / 2 + number_end
    endpoints = [d[1] for d in dur_slice]
    split = int(np.argmin(np.abs(np.array(endpoints) - mid)))
    split_pt = dur_slice[split][1]
    print('diff error:{}sec'.format((split_pt - mid)/1000))
    slices = []
    slices.append(sound[number_start:split_pt])
    slices.append(sound[split_pt:bogi_start])
    slices.append(sound[bogi_start:bogi_end])



    return slices, dur_slice_all

#slice all
#def slices_merge(slices, )

def part3_export(slices, dest, ori_name, part4 = False):

    _o = ori_name.split('.')
    format_s = 'mp3'
    ori_name = _o[0]
    out_path1 = osj(dest, ori_name + '_1' + '.' + format_s)
    out_path5 = osj(dest, ori_name + '_5' + '.' + format_s)

    slices[0].export(out_path1, format = format_s)
    slices[2].export(out_path5, format = format_s)


    if part4:
        out_path2 = osj(dest, ori_name + '_2' + '.' + format_s)
        slices[1].export(out_path2, format=format_s)