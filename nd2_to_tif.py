# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:08:07 2021

@author: Alexandros Papagiannakis, Christine Jacobs-Wagner lab, Stanford University 2022
"""


import numpy as np
from pims import ND2_Reader
# from PIL import Image
import os
from skimage import io


def nd2_to_tif(images_path, experiment, frame_range, save_path):
    """
    This function is used to export .nd2 images to tif.
    It will only work for the 'mct' iteration axis
    It does not return the metadata.
    
    Parameters
    ----------
    image_path - string: the path of the .nd2 file
    experiment - string: the experiment ID
    save_path - string/directory where the images are saved
    
    Returns
    -------

    Notes
    -----
    It only works for the 'mct' iteration axis. It works for nd2 files that were genrated
    using the ND acquisition with multiple xy positions (m), timepoints (t) and channels (c).
    For any other nd2 files the function raises a ValueError.
   
    """
    # The path of the .nd2 file 
    images = ND2_Reader(images_path)
    # "C:\Users\Alex\Anaconda3\Lib\site-packages\pims_nd2\nd2reader.py"
    # This path has been modified in lines 228 and 229 to accommodate the function.
    # print('metadata:',images.metadata)
    print('dimensions:',images.sizes)
    
    # scale = round(images.metadata['calibration_um'],3)  # μm/px scale
    # sensor = (images.sizes['x'], images.sizes['y'])
    channels = []
    if 'c' in images.sizes:
        # get the channels and frames from the .nd2 metadata
        number_of_channels = images.sizes['c']
        
        for i in range(number_of_channels):
            channels.append('c'+str(i+1))
 
    # number_of_frames = images.metadata['sequence_count']
    iteration_axis = ''
    if 'm' in images.sizes and images.sizes['m'] > 1:
        iteration_axis += 'm'
        number_of_positions = images.sizes['m']
    if 'c' in images.sizes and images.sizes['c'] > 1:
        iteration_axis += 'c'
    if 't' in images.sizes and images.sizes['t'] > 1:
        iteration_axis += 't'
        number_of_timepoints = images.sizes['t']

    def get_position_string(pos, number_of_positions):
        
        if number_of_positions>9:
            digi_n = 2
        else:
            digi_n =1
            
        position_string = 'xy'+(digi_n - len(str(pos+1)))*'0'+str(pos+1)
        
        return position_string
    
    def get_time_string(tm, number_of_timepoints):
        
        return 't'+(len(str(number_of_timepoints))-len(str(tm)))*'0'+str(tm)
    
    # def get_channel_string(ch):
        
    #     return 'c'+str(ch+1)


    # For snapshots at different channels and XY positions and timepoints
    if iteration_axis == 'mct':
        
        with images as frames:
            print(frames)
            frames.iter_axes = iteration_axis
            pos = 0
            ch = 0
            tm = 0
            position_string = get_position_string(pos, number_of_positions)
            # channel_string = get_channel_string(pos, number_of_positions)
            position_path = save_path+'/'+experiment+'_'+position_string+'_'+channels[ch]
            os.mkdir(position_path)

            time_string = get_time_string(tm, number_of_timepoints)

            for frame in frames:
                if tm < number_of_timepoints:
                    # image_to_save = Image.fromarray(np.array(frame))
                    # image_to_save.save(position_path+'/'+experiment+'_'+position_string+time_string+channels[ch]+'.tif')
                    fname = position_path+'/'+experiment+'_'+position_string+time_string+channels[ch]+'.tif'
                    if tm >= frame_range[0] and tm <= frame_range[1]:
                        io.imsave(fname, np.array(frame))
                    tm+=1
                    time_string = get_time_string(tm, number_of_timepoints)
                elif tm == number_of_timepoints:
                    tm = 0
                    time_string = get_time_string(tm, number_of_timepoints)
                    if ch < number_of_channels-1:
                        ch += 1
                        position_path = save_path+'/'+experiment+'_'+position_string+'_'+channels[ch]
                        os.mkdir(position_path)
                        # image_to_save = Image.fromarray(np.array(frame))
                        # image_to_save.save(position_path+'/'+experiment+'_'+time_string+'_'+position_string+'.tif')
                        fname = position_path+'/'+experiment+'_'+position_string+time_string+channels[ch]+'.tif'
                        if tm >= frame_range[0] and tm <= frame_range[1]:
                            io.imsave(fname, np.array(frame))
                        tm+=1
                        time_string = get_time_string(tm, number_of_timepoints)
                    elif ch == number_of_channels-1:
                        ch = 0
                        pos+=1
                        position_string = get_position_string(pos, number_of_positions)
                        position_path = save_path+'/'+experiment+'_'+position_string+'_'+channels[ch]
                        os.mkdir(position_path)
                        # image_to_save = Image.fromarray(np.array(frame))
                        # image_to_save.save(position_path+'/'+experiment+'_'+time_string+'_'+position_string+'.tif')
                        fname = position_path+'/'+experiment+'_'+position_string+time_string+channels[ch]+'.tif'
                        if tm >= frame_range[0] and tm <= frame_range[1]:
                            io.imsave(fname, np.array(frame))
                        tm+=1
                        time_string = get_time_string(tm, number_of_timepoints)
        frames.close()
    # if no channels or time points are specified there should be only one image
    
    else:
        raise ValueError('the iteration axis is not mct. Try other versions of this code.')
    

        

# nd2_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07262025_4days\07262025_CJW6723_4daysAS_recovery.nd2"
# save_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07262025_4days\20250726_timelapse_omnipose"
# experiment = '07262025_CJW6723_4daysAS_recovery'

# nd2_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07252025_3days\07252025_CJW6723_3daysAS_recovery.nd2"
# save_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07252025_3days\20250725_timelapse_omnipose"
# experiment = '07252025_CJW6723_3daysAS_recovery'

nd2_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07242025_2days\07242025_CJW6723_2daysAS_recovery.nd2"
save_path = r"D:\Shares\Data_01\Alex Papagiannakis\Microscopy\muNS\Starvation\Acute_starvation\Recovery\07222025_starvation\07242025_2days\20250724_timelapse_omnipose"
experiment = '07242025_CJW6723_2daysAS_recovery'


nd2_to_tif(nd2_path, experiment, (0,240), save_path)
