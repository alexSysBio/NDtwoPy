# NDtwoPy
This repository includes an implementation of the pims_nd2 reader for different image-iteration axes

nd2_to_array:
  The nd2_to_array function can be used to import .nd2 files into python. The files are stored into a dictionary which includes elemenets of the iteration axis as   keys and the image 2D numpy arrays as values. It uses the nd2 image reader from the pims library:
  https://pypi.org/project/pims-nd2/#:~:text=pims_nd2%20contains%20a%20reader%20for,and%20nice%20display%20in%20IPython.
  
  I have tested most of the implemented iterations from microscopy images I have acquired. If the remaining iterations do not work it should be an easy fix. Please reach out to address any exepctions.

  Cite:
    https://www.biorxiv.org/content/10.1101/2024.10.08.617237v2.full
    
    DNA/polysome phase separation and cell width confinement couple nucleoid segregation 
    to cell growth in Escherichia coli
    
    Alexandros Papagiannakis, Qiwei Yu, Sander K. Govers, Wei-Hsiang Lin,  Ned S. Wingreen, Christine Jacobs-Wagner
    
    bioRxiv, https://doi.org/10.1101/2024.10.08.617237, October 22, 2024


