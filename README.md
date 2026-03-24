# NDtwoPy
This repository includes an implementation of the pims_nd2 ND2 reader or the ND2 reader from the Open Science Tools for different image-iteration axes

nd2_to_array:
  The nd2_to_array function can be used to import .nd2 files into python. The files are stored into a dictionary which includes elemenets of the iteration axis as   keys and the image 2D numpy arrays as values. 
  
It uses the nd2 image reader from the pims library:
  https://pypi.org/project/pims-nd2/#:~:text=pims_nd2%20contains%20a%20reader%20for,and%20nice%20display%20in%20IPython.
Or the nd2 image reader from the Open Science Tools:
  https://github.com/Open-Science-Tools/nd2reader
  
  I have tested most of the implemented iterations from microscopy images I have acquired. If the remaining iterations do not work it should be an easy fix. Please reach out to address any exceptions.

  Cite:
    [publication](https://elifesciences.org/articles/104276#content)
    
    Nonequilibrium polysome dynamics promote chromosome segregation and its coupling to cell growth in Escherichia coli.
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    Jun 24, 2025, https://doi.org/10.7554/eLife.104276.3


This repository includes different implementations of the ND2 readers, including a script to stream image arrays and store them into .tif files: <code> stream_nd2_to_tif.py </code>. This latest script is a very memory-efficient and fast method to export ND2 files and it is highly recommended to slower GUI-dependent methods, or other functions that upload the entire set of arrays on the memory before exporting.
