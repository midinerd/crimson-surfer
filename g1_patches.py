# copyright crissaegrim/midinerd(c) 2024  whatever that means.

# this file is a work in progress and won't simply "just work"
# it assumes an audio directory at g:/audio (edit line 10 to change this)
# and that it is being run in DOS (dir *.pch > ... collects and outputs your .pch list)
import argparse
import os
from pathlib import Path
import sys


def generate_patch_file(patch_dir):
    # generate a list of G1 patch names, return them to the caller as a Python list, for simple iteration.
    print(f"\nMaking catalog of G1 patches found in directory: {patch_dir}")
    return list(Path(patch_dir).rglob('*.pch'))


def make_textfile(patch_dir, max_patch_file):
    """
    Iterate over a list of patch names, replace the \\ be changed to / to be comptible with MAX/Msp
    """

    patch_names = generate_patch_file(patch_dir)
    if patch_names:
        with open(max_patch_file, 'w') as fh_out:
            # loop over the raw patch names, write them to the file that will be used by MAX
            for patch in patch_names:
                # replace \\ with / , write back to same file in order to be compatible with MAX
                fh_out.write(f"{str(patch.absolute()).replace('\\','/')}\n")

        print(f"\n{len(patch_names)} patches were found and written to {patch_dir}\\{max_patch_file}.\n")
    else:
        print("\nERROR. No patch names were found at {patch_dir}.\n\n")


def read_patches(max_patchfile):

    patches = []
    with open(max_patchfile, 'r') as fh_in:
        patches = fh_in.readlines()

    return patches


def show_patch(max_patchfile, patch_number):
    """
    Display the patch name specified by the patch number that is passed on the command line
    """

    if Path(max_patchfile).exists():
        patch_names = read_patches(max_patchfile)
        if patch_names:
            patch_count = len(patch_names)

            if patch_number > patch_count:
                print('\nThere are only %d patches in the file. You specified Patch # %d\n' % (patch_count, patch_number))
            else:
                for line_number, line in enumerate(patch_names, start=1):
                    if line_number == patch_number:
                        print(f'\n\tPatch #{patch_number}: {line}')
                        break
        else:
            print("\nERROR. No patch names were found at {AUDIO_ROOTDIR}.\n\n")
    else:
        print(f'\n\n\t{max_patchfile} was not found. You must run the program with the --maketext argument first.')

def process_cmd_line():

    parser = argparse.ArgumentParser(
                        prog='g1_patches',
                        description='Creates a texfile containing the filenames of Nord Modular G1 patches.',
                        epilog='') # shown at the bottom of the help message
    
    parser.add_argument('--maketext', default=False, action='store_true', help='Create a text file containing all of the Nord Modular patch names.')
    parser.add_argument('--showpatch', default=None, type=int, metavar='PATCH_NUMBER', help='Show the patch name specified by the patch number. This assumes the program has been previously run with the "maketext" argument.')
    parser.add_argument('--patchdir', default='patches', help='The directory where the patches are located. The default directory is "patches" in the current directory.')
    # parser.add_argument('--patchdir', default='patches', help='The directory where the patches are located. The default directory is "patches" in the current directory.')
    # parser.add_argument('--patchdir', default='patches', help='The directory where the patches are located. The default directory is "patches" in the current directory.')


    args = parser.parse_args()

    # check for no arguments passed, print help message
    if len(sys.argv) == 1:
        print()
        parser.print_help()
        sys.exit(1) #exit with an error code

    return args


def main():

    # raw_patchnames = f'{AUDIO_ROOTDIR}\\g1-raw-patches.txt'
    # max_patchnames = 'g1-patches-max.txt'

    status = 0
    args = process_cmd_line()

    if args.patchdir:
        patch_dir = args.patchdir
        # raw_patchnames = rf'{patch_dir}\g1-raw-patches.txt'
        max_patchfile = rf'{patch_dir}\g1-patches-max.txt'
    else:
        #raw_patchnames = r'patches\g1-raw-patches.txt'
        patch_dir = 'patches'
        max_patchfile = r'g1-patches-max.txt'

    if args.maketext:
        make_textfile(patch_dir, max_patchfile)
    elif args.showpatch is not None:
        patch_number = args.showpatch
        show_patch(max_patchfile, patch_number)

    return status

if __name__ == "__main__":
    sys.exit(main())