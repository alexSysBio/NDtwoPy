# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:20:05 2026
@author: Alexandros Papagiannakis, Christine Jacobs-Wagner lab, Sarafan ChEM-H, Stanford University 2026 

Memory-efficient ND2 to TIF converter.
Original author: Alexandros Papagiannakis, Christine Jacobs-Wagner lab, Sarafan ChEM-H, Stanford University
Refactored for memory efficiency.

This script processes ND2 files frame-by-frame ("streaming") to avoid loading the
entire file into RAM. It iterates through the ND2 file, saves each frame as a
TIFF image, and then discards the frame from memory before loading the next one.
"""

import os
from pims import ND2_Reader
from skimage import io


def get_position_string(position_int):
    """Generates a formatted string for the XY position index."""
    position_int += 1
    return 'xy' + str(position_int).zfill(2)

def get_time_string(timepoint_int, time_string_length=3):
    """Generates a formatted string for the timepoint index."""
    return 't' + str(timepoint_int).zfill(time_string_length)

def get_imaging_channels(images):
    """Extracts channel names and count from ND2 metadata."""
    channels = []
    if 'c' in images.sizes:
        number_of_channels = images.sizes['c']
        for i in range(number_of_channels):
            ch = images.metadata['plane_' + str(i)]['name']
            if ch in channels:
                # Handle cases where the same channel name is used multiple times
                channels.append(ch + '_2') 
            else:
                channels.append(ch)
    else:
        number_of_channels = 1 # Even with no 'c' axis, there's at least one channel
    return channels, number_of_channels

def get_iteration_axes_and_dims(images):
    """Determines the iteration order and dimension sizes from ND2 metadata."""
    sizes = images.sizes
    iteration_axis = ''
    
    # Nikon NIS-Elements can use 'v' or 'm' for multipoint positions.
    if 'v' in sizes and sizes['v'] > 1:
        iteration_axis += 'm'
        num_positions = sizes['v']
    elif 'm' in sizes and sizes['m'] > 1:
        iteration_axis += 'm'
        num_positions = sizes['m']
    else:
        num_positions = 1
        
    if 'c' in sizes and sizes['c'] > 1:
        iteration_axis += 'c'
        
    if 't' in sizes and sizes['t'] > 1:
        iteration_axis += 't'
        num_timepoints = sizes['t']
    else:
        num_timepoints = 1
        
    return iteration_axis, num_positions, num_timepoints



def stream_nd2_to_tif(nd2_path, experiment_id, channel_selection='none'):
    """
    Reads an ND2 file frame-by-frame and saves each frame as a TIFF file.

    This function avoids loading the entire file into memory by processing it
    as a stream. It is suitable for very large ND2 files.

    Parameters
    ----------
    nd2_path : str
        Path to the input .nd2 file.
    save_path : str
        Root directory where TIFF images and subfolders will be saved.
    experiment_id : str
        An ID included in the name of each saved image.
    channel_selection : list of str, optional
        A list of channel names to selectively save (e.g., ['Phase', 'FITC']).
        If 'none' (default), all channels are saved.
    """
    print(f"Processing {experiment_id}...")
    
    with ND2_Reader(nd2_path) as images:
        # 1. Get metadata without loading image data
        channels, num_channels = get_imaging_channels(images)
        iteration_axis, num_positions, num_timepoints = get_iteration_axes_and_dims(images)
        
        # pims iterates over the last specified axis first.
        # For 'mct', the iteration order is t, then c, then m.
        images.iter_axes = iteration_axis
        
        print(f"  Layout: {images.sizes}, Iteration axis: '{iteration_axis}'")
        print(f"  Positions: {num_positions}, Timepoints: {num_timepoints}, Channels: {num_channels}")

        # 2. Iterate through frames one by one
        for i, frame in enumerate(images):
            # This is the only point where a single frame's data is in RAM
            
            # 3. Calculate current position, channel, and timepoint from the flat index 'i'
            # The logic depends on the iteration order (defined by axis string length and content)
            
            pos, ch_idx, tm = 0, 0, 0
            
            if 't' in iteration_axis:
                tm = i % num_timepoints
                
            if 'c' in iteration_axis:
                ch_idx = (i // num_timepoints) % num_channels
                
            if 'm' in iteration_axis:
                pos = (i // (num_timepoints * num_channels)) % num_positions

            # For simpler cases without all three axes
            if iteration_axis == 'mc':
                ch_idx = i % num_channels
                pos = i // num_channels
            elif iteration_axis == 'mt':
                tm = i % num_timepoints
                pos = i // num_timepoints
            elif iteration_axis == 'ct':
                tm = i % num_timepoints
                ch_idx = i // num_timepoints
            elif iteration_axis == 'm':
                pos = i
            elif iteration_axis == 'c':
                ch_idx = i
            elif iteration_axis == 't':
                tm = i
            
            # 4. Get string names and check against selection
            ch_name = channels[ch_idx] if channels else 'default'
            
            if channel_selection != 'none' and ch_name not in channel_selection:
                continue # Skip this frame if it's not in the selected channels

            # 5. Construct filename and path
            position_str = get_position_string(pos)
            time_str = get_time_string(tm)
            
            # Create a structured output path: save_path/xy01/Phase/experiment_xy01_Phase_t0000.tif
            # This structure is based on your 'mct' iteration logic.
            # We use os.path.join for cross-platform compatibility.
            save_path = nd2_path[:-4]+'_timelapse_phase'
            os.makedirs(save_path, exist_ok=True) # `exist_ok=True` prevents errors if dir exists
            output_dir = os.path.join(save_path, position_str)
            os.makedirs(output_dir, exist_ok=True) # `exist_ok=True` prevents errors if dir exists
            
            if ch_name != 'default':
                id_string = f"{experiment_id}_{position_str}_{ch_name}_{time_str}.tif"
            else:
                id_string = f"{experiment_id}_{position_str}_{time_str}.tif"
            output_filepath = os.path.join(output_dir, id_string)
            
            # 6. Save the current frame to a TIF file
            # frame is a numpy array at this point
            io.imsave(output_filepath, frame, check_contrast=False)
            
    print(f"Finished processing {experiment_id}.")


def iterate_and_stream(experiment_path):
    """
    Finds all .nd2 files in a directory and converts them to TIFFs using the
    memory-efficient streaming method.
    """
    for exp in os.listdir(experiment_path):
        exp_path = os.path.join(experiment_path, exp)
        image_file = [f for f in os.listdir(exp_path) if f.lower().endswith('.nd2')][0]
        nd2_path = os.path.join(exp_path, image_file)
        experiment_id = image_file[:-4]
        print(nd2_path, experiment_id)
        stream_nd2_to_tif(nd2_path, experiment_id)

