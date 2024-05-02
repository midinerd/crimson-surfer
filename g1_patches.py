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

def read_patches(filename):
    with open(filename,'r') as fh:
        patch_names = fh.readlines()
    return patch_names


def make_textfile():

    # generate a list of G1 patch names, write them to a file
    os.system('dir %s\\*.pch /s /b > %s' % (AUDIO_ROOTDIR, filename))
    
    patch_names = read_patches(filename)
    
    # replace \\ with / , write back to same file in order to be compatible with MAX
    with open(filename, 'w') as fh:
        for line in patch_names:
            fh.write(line.replace('\\','/'))

    get_patch(1)


def get_patch(patch_number):

    patch_names = read_patches(filename)
    patch_count = len(patch_names) #

    if patch_number > patch_count:
        print('\nThere are only %d patches in the file. You specified Patch # %d\n' % (patch_count, patch_number))
    else:
        for line_number, line in enumerate(patch_names, start=1):
            if line_number == patch_number:
                print('\n%s' % line)
                break


def process_cmd_line():

    parser = argparse.ArgumentParser(
                        prog='g1_patches',
                        description='Makes a texfile containing the filenames of Nord Modular G1 patches.',
                        epilog='') # shown at the bottom of the help message
    
    parser.add_argument('--maketext', default=False, action='store_true', help='Create a text file containing all of the Nord Modular patch names.')
    parser.add_argument('--showpatch', default=None, type=int, help='Show the patch name specified by the patch number.')
    args = parser.parse_args()

    # check for no arguments passed
    if len(sys.argv) == 1:
        print()
        parser.print_help()
        sys.exit(1) #exit with an error code

    return args


def main():

    status = 0
    args = process_cmd_line()
    if args.maketext:
        make_textfile()
    elif args.showpatch is not None:
        patch_number = args.showpatch
        get_patch(patch_number)
    return status

if __name__ == "__main__":
    sys.exit(main())