import numpy as np
import pandas as pd
from pandas import read_excel
import os
from settings import ffmpeg_exec_path, org_vids_path, output_path, mat_file_path
import time
import scipy.io



def extract_m_file(numpy_array):
    #Function to read in an mat file containg the relavant video info
    file_names = []
    frames_1 = []
    frames_2 = []
    trial_1 = []
    trial_2 = []
    view = []

    for element in numpy_arr:
        file_names.append(element[0][0])
        frames_1.append(element[1][0][0])
        frames_2.append(element[1][0][1])
        view.append(element[3][0])
        trial_1.append(element[4][0][0])
        trial_2.append(element[4][0][1])
    return file_names, frames_1, frames_2, trial_1, trial_2, view


def process_file_names (file_name):
    #A function to get the name of the video in the excel file to match the video names stores in the org_videos_path where the videos are actually stored
     split_list = os.path.normpath(file_name).lstrip(os.path.sep).split(os.path.sep)
     new_name = split_list[-2]+'_'+split_list[-1]
     return new_name

#Start 
t0 = time.time()
#Loading-in the matlab file for processing
mat_file = scipy.io.loadmat(mat_file_path)
numpy_arr = mat_file['dataset'][0]
#Getting the relevant info from the files
files, frames1, frames2, trial1, trial2, view = extract_m_file(numpy_arr)
#Matches the file names with the video names 
files = list(map(process_file_names,files))

for i in range(len(files)-1):
    #Check if the videos are of the same tap
    if (trial2[i] == trial2[i+1]):
        view_short = view[i][0].capitalize()
        output_file_name = "{v}_{name}_Sess_{session}_Trial{trial_num}.mp4".format(v=view_short, name = files[i].split('.')[0], session = trial1[i], trial_num = trial2[i])
        command = '{ffmpeg} -hwaccel cuda -i "{path}\\{file1}" -i "{path}\\{file2}" -filter_complex "[0:v]trim={beg_vid1}:{end_vid1},setpts=PTS-STARTPTS[v0];[1:v]trim={beg_vid2}:{end_vid2},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[out]" -map "[out]" -c:v libx264 -pix_fmt yuv420p -preset superfast -crf 23 "{out_path}\\{out_file}"'.format(ffmpeg = ffmpeg_exec_path, path = org_vids_path, file1 = files[i], file2 = files[i+1], beg_vid1 = frames1[i]/90, end_vid1 = frames2[i]/90, beg_vid2 = frames1[i+1]/90, end_vid2 = frames2[i+1]/90, out_path = output_path, out_file = output_file_name)
        os.system(command)
    #If not then crop the video individually
    else:
        view_short = view[i][0].capitalize()
        output_file_name = "{v}_{name}_Sess_{session}_Trial{trial_num}.mp4".format(v=view_short, name = files[i].split('.')[0], session = trial1[i], trial_num = trial2[i])
        command = '{ffmpeg} -hwaccel cuda -y -i "{path}\\{file}" -ss {num1} -c:v libx264 -pix_fmt yuv420p -frames:v {num2} -preset superfast -crf 23 "{out_path}\\{out_file}"'.format(ffmpeg = ffmpeg_exec_path, path = org_vids_path, file = files[i], num1 = frames1[i]/90, num2 = frames2[i] - frames1[i], out_path = output_path, out_file = output_file_name)
        os.system(command)
t1 = time.time()
total = t1-t0
print('total processing time: {tot_time}'.format(tot_time = time.strftime("%Hh%Mm%Ss", time.gmtime(total))))

