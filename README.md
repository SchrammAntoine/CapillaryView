# CapillaryView
Data vizualization GUI for capillary electrophoresis data

# Conda env

```bash
conda env create -f environment.yml
conda activate CapillaryProcessing
```

# Running 

```bash
python3 main.py
```

# GUI Description 

The interface is composed of three elements, organized on an horizontal layout.

## Tree 

On the left side, a folder tree allow you to navigate in your file system and select the files you're interested in.
Selection of files that cannot be parsed by the program are ignored.
Multiple selection are unable, mediated by mouse click whle keeping `ctrl` or `Shift` pressed. Selection behavior follow `ctrl` and `Shift` standards.
The root directory can be changed manually by clicking onto the `Select Root Directory` button

## Plot

The center is dedicated to data vizualization. It integrates the matplotlib GUI.
Sequencing data are usually composed of 4 distinct fluorescence intensity array, refered to as channels. Those channels can be disabled/unabled by selecting the corresponding buttons located top right.

## Processing

This is not a processing unit properly speaking. Instead, the processing tools included here are made for enhancing data vizualization performances. To this date, two parameters are proposed :
* region of interest : used to get focus on a region of interest across various files. This prevent the plot to unzoom back to full view upon loading a new data serie.
* median scaling : usefull for comparing two series that scale fluorescence intensities differently.
