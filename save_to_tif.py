# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 15:08:07 2021

@author: Alexandros Papagiannakis, Christine Jacobs-Wagner lab, Sarafan ChEM-H, Stanford University 2021
Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024
"""

import os
from skimage import io
import nd2_to_array as ndtwo


def get_position_string(position_int):
    """
    Parameters
    ----------
    position_int : integer
        The position integer starting from 0 for position XY01

    Returns
    -------
    str
        A string description of the XY position. e.g. XY03 for position 2.

    """
    position_int+=1
    return 'xy'+(2-len(str(position_int)))*'0'+str(position_int)



def get_time_string(timepoint_int):
    """
    Parameters
    ----------
    timepoint_int : integer
        The timepoint integer starting from 0 for the first image in a timelapse

    Returns
    -------
    str
        A string description of the timepoint. e.g. t0003 for timepoint 3.

    """
    return 't'+(4-len(str(timepoint_int)))*'0'+str(timepoint_int)



def store_images_to_tif(image_arrays, iteration_axis, save_path, experiment_id, channel_selection='none'):
    """
    

    Parameters
    ----------
    image_arrays : dictionary of 2D numpy arrays
        A dictionary that contains the XY positiosn, channels 
        and timepoints as keys and 2D numpy arrays as values.
    iteration_axis : string
        The axis of image iteration where 'm' stands for XY positions, 
        'c' for channels, and 't' for timepoints.
    save_path : string
        The path where the TIFF images will be saved.
    experiment_id : string
        An ID that will be included in the name of the saved image.
    channel_selection : 'none' or list of strings, optional
        The default is 'none'. Otherwise include 
        a list of channels that you will use to selectively save images 
        from the included channels: e.g., ['Phase', 'FITC'].

    Returns
    -------
    Saves the selected TIFF images

    """
    if iteration_axis == 'mct':
        for pos in image_arrays:
            position_string = get_position_string(pos)
            os.mkdir(save_path+'/'+position_string)
            for ch in image_arrays[pos]:
                if channel_selection == 'none' or ch in channel_selection:
                    os.mkdir(save_path+'/'+position_string+'/'+ch)
                    for tm in image_arrays[pos][ch]:
                        time_string = get_time_string(tm)
                        id_string = experiment_id+'_'+position_string+'_'+ch+'_'+time_string+'.tif'
                        io.imsave(save_path+'/'+position_string+'/'+ch+'/'+id_string, image_arrays[pos][ch][tm])

    elif iteration_axis == 'mt':
        for pos in image_arrays:
            position_string = get_position_string(pos)
            os.mkdir(save_path+'/'+position_string)
            for tm in image_arrays[pos]:
                time_string = get_time_string(tm)
                id_string = experiment_id+'_'+position_string+'_'+time_string+'.tif'
                io.imsave(save_path+'/'+position_string+'/'+id_string, image_arrays[pos][tm])
                
    elif iteration_axis == 'mc':
        for pos in image_arrays:
            position_string = get_position_string(pos)
            for ch in image_arrays[pos]:
                if channel_selection == 'none' or ch in channel_selection:
                    id_string = experiment_id+'_'+position_string+'_'+ch+'.tif'
                    io.imsave(save_path+'/'+id_string, image_arrays[pos][ch])
            

def save_multiple_tif_files_for_cell_segmentation(images_path, save_path, channel_selection):
    image_files= os.listdir(images_path)
    image_files = [f for f in image_files if '.nd2' in f]
    
    for imgfl in image_files:
        images = ndtwo.nd2_to_array(images_path+'/'+imgfl)
        print(images[0])
        print(images[1])
        print(images[3])
        store_images_to_tif(images[2], 
                            images[0], 
                            save_path, 
                            imgfl[:-4], 
                            channel_selection=channel_selection)
        
                
                
                