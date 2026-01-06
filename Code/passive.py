# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 14:26:13 2025

@author: lukas
"""

from classes import Passive_Analysis
import os

# Full path to this script
script_path = os.path.abspath(__file__)
print("Script path:", script_path)

# Folder containing this script
script_dir = os.path.dirname(script_path)
print("Script folder:", script_dir)

#parent directory
parent_directory = os.path.dirname(script_dir)
print(parent_directory)

#generate path directories
To_Process_folder = os.path.join(parent_directory, "Zu_Verarbeiten")
Finished_folder   = os.path.join(parent_directory, "Fertig")
Background_folder = os.path.join(parent_directory, "Background_Data") 
JPG_folder        = os.path.join(Background_folder, "JPG_Files")
Mask_folder        = os.path.join(Background_folder, "Mask_Files")
Position_folder        = os.path.join(Background_folder, "Position_Files")
Position_Words_folder        = os.path.join(Background_folder, "Position_Words_Files")
Text_folder        = os.path.join(Background_folder, "Text_Files")
Text_Numpy_folder        = os.path.join(Background_folder, "Text_Numpy_Files")


