# copyright crissaegrim/midinerd(c) 2024  whatever that means.

# this file is a work in progress and won't simply "just work"
# it assumes an audio directory at g:/audio (edit line 10 to change this)
# and that it is being run in DOS (dir *.pch > ... collects and outputs your .pch list)
import argparse
import io
import pathlib
import os
import sys

# currently only used/tested on win10 hence the cmd.exe and g:/ os bits lying around

# AUDIO_ROOTDIR = 'g:/audio'
AUDIO_ROOTDIR = 'patches'
filename = '%s\\g1-raw-patches.txt' % AUDIO_ROOTDIR

def make_textfile():

    # generate a list of G1 patch names, write them to a file
    os.system('dir %s\\*.pch /s /b > %s' % (AUDIO_ROOTDIR, filename))
    
    with open(filename,'r') as fh:
        patch_names = fh.readlines()

    # replace \\ with / , write back to same file in order to be compatible with MAX
    with open(filename, 'w') as fh:
        for line in patch_names:
            fh.write(line.replace('\\','/'))

    get_patch(0)

def get_patch(patch_number):

    with open(filename,'r') as fh:
        patch_names = fh.readlines()

    for line_number, line in enumerate(patch_names):
        if line_number == patch_number:
            print('\n%s' % line)
            break

def process_cmd_line():

    parser = argparse.ArgumentParser(
                        prog='g1_patches',
                        description='Makes a texfile containing the filenames of Nord Modular G1 patches.',
                        epilog='Text at the bottom of help')
    parser.add_argument('--maketext', default=False, action='store_true', help='Create a text file containing all of the Nord Modular patch names.')
    parser.add_argument('--getpatch', default=None, type=int, help='TBD')
    args = parser.parse_args()
    return args

def main():
    status = 0
    args = process_cmd_line()
    if args.maketext:
        make_textfile()
    elif args.getpatch is not None:
        patch_number = args.getpatch
        get_patch(patch_number)
    return status

if __name__ == "__main__":
    sys.exit(main())