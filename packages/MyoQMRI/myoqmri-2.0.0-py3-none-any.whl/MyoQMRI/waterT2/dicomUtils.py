#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 09:26:07 2015

@author: francesco
"""

from __future__ import print_function

import numpy as np
try:
    import pydicom as dicom
    import pydicom.uid as UID
except:
    import dicom
    import dicom.UID as UID
import os
import os.path
import sys
import copy
from progress.bar import Bar

def load3dDicom(path):
    allowed_ext = ['.dcm', '.ima']
    basepath = os.path.abspath(path)
    threeDData = None
    info = []
    l = os.listdir(basepath)
    bar = Bar('Loading Dicom', max=len(l))
    threeDlist = []
    for f in sorted(l):
        if os.path.basename(f).startswith('.'): continue
        fname, ext = os.path.splitext(f)
        if ext.lower() in allowed_ext:
            try:
                dFile = dicom.read_file(os.path.join(basepath, f))
                pixelIma = dFile.pixel_array
                threeDlist.append(np.copy(pixelIma.astype('float32')))
                dFile.PixelData = ""
                info.append(dFile)
            except:
                pass
        bar.next()
    bar.finish()
    threeDData = np.stack(threeDlist, axis = 2)
            
    return (threeDData, info)

def save3dDicom(volume, info, path, newSeriesNumber = None, newSeriesDescription = None, newImageComment = None, startImageNumber = 1):
    try:
        os.mkdir(path)
    except:
        pass
    if newSeriesNumber is None:
        newSeriesNumber = info[0].SeriesNumber
        newSeriesUID = info[0].SeriesInstanceUID
    else:
        newSeriesUID = UID.generate_uid()
    
    if newSeriesDescription is None:
        newSeriesDescription = info[0].SeriesDescription
    
    if len(info) == 1:
        dataArray = volume[:,:,0]
        dicomFileData = copy.deepcopy(info[0]) # create a copy of object
        if dataArray.dtype == 'uint16': # check correct format
            dicomFileData.PixelData = dataArray.tostring()
        else:
            dicomFileData.PixelData = dataArray.round().astype('uint16').tostring()
        dicomFileData.SeriesNumber = newSeriesNumber
        dicomFileData.SeriesInstanceUID = newSeriesUID
        dicomFileData.SOPInstanceUID = UID.generate_uid()
        if newImageComment is not None:
            dicomFileData.ImageComment = newImageComment
        
        fName = os.path.join(path, "image0001.dcm") # if one wants to save a part of a dataset
        dicom.write_file(fName, dicomFileData)
    else:
        bar = Bar('Saving Dicom', max=len(info))
        for sl in range(len(info)):
            dataArray = volume[...,sl]
            dicomFileData = copy.deepcopy(info[sl]) # create a copy of object
            if dataArray.dtype == 'uint16': # check correct format
                dicomFileData.PixelData = dataArray.tostring()
            else:
                dicomFileData.PixelData = dataArray.round().astype('uint16').tostring()
            dicomFileData.SeriesNumber = newSeriesNumber
            dicomFileData.SeriesInstanceUID = newSeriesUID
            dicomFileData.SOPInstanceUID = UID.generate_uid()
            if newImageComment is not None:
                dicomFileData.ImageComment = newImageComment
            
            fName = os.path.join(path, "image%04d.dcm" % (sl+startImageNumber)) # if one wants to save a part of a dataset
            dicom.write_file(fName, dicomFileData)
            bar.next()
        bar.finish()