###############################################################################
# -*- coding: utf-8 -*-
###############################################################################

import os
import time
import itertools
import subprocess


devices = [x for x in subprocess.check_output(["gphoto2", "--auto-detect"]).split() if "usb" in x]

###############################################################################

def get_files(d, num=0):
    files = sorted(os.listdir(d))
    ret = { 'dirname': d, 'files': []}
    if files and len(files)%2 is 0:
        if num*2 > len(files) or num is 0:
            # take all files
            num = len(files)/2
        ret['files'] = [ (files[i*2], files[i*2+1]) for i in range(num)]
    return ret

###############################################################################

def inc(fname):
    name, ext = os.path.splitext(fname)
    return '{0:03d}{1}'.format(int(name) + 2, ext)

###############################################################################

def touch(fname, times=None):
    with file(fname, 'a'):
        os.utime(fname, times)

def capture(left, right):
    for n, device in enumerate(devices):
        print n
        filename = left
        if n == 1:
            filename = right
        subprocess.call(["gphoto2", "--port", device, "--set-config", "capturetarget=card"])
        #subprocess.call(["gphoto2", "--port", device, "--capture-image-and-download"])
        subprocess.call(["gphoto2", "--port", device, "--capture-tethered"])
        os.rename("capt0000.jpg", "{}".format(filename))
    return True

###############################################################################

def delete_all_files(d):
    [os.remove(os.path.join(d, f)) for f in os.listdir(d)]

###############################################################################

def insert(d, left, right):
    data = get_files(d)
    dn = data['dirname']
    if data['files']:
        files = []
        # make list of files after insert point
        # (because maybe we will have to rename these files...)
        for i in itertools.dropwhile(
            lambda x: dn + x[0] <> left and dn + x[1] <> right, data['files']):
            files.append(i[0])
            files.append(i[1])
        # generate new names
        nl, nr = dn + inc(files[0]), dn + inc(files[1])
        files = files[2:] # skip current pair
        # if there are files to be renamed, first make sure that there is not
        # empty pair (that can happen after Delete action)
        if len(files) >= 2:
            if nl <> dn+files[0] and nr <> dn+files[1]:
                files = [] # pages are in order, nothing to rename
        [os.rename(dn+i, dn + inc(i)) for i in sorted(files, reverse=True)]
    else:
        # make initial names
        nl, nr = d + '001.jpg', d + '002.jpg'
    return capture(nl, nr)

###############################################################################

def rotate(d):
    # mogrify -rotate 90 file.jpg
    # convert -rotate 90 original_file.jpg new_file.jpg
    import Image
    data = get_files(d)
    for pair in data['files']:
        for f in pair:
            img = Image.open(d+f)
            name, ext = os.path.splitext(f)
            print(name)
            if int(name) % 2 == 1:
                img2 = img.rotate(90)
            else:
                img2 = img.rotate(-90)
            img2.save(d+f)

if __name__=='__main__':
    rotate('static/img/')