# copyright crissaegrim/midinerd(c) 2024  whatever that means.

import argparse
from pathlib import Path
import sys


def generate_patch_file(patch_dir):
    """
    generate a list of G1 patch names, return them to the caller as a Python list, for simple iteration.
    """
    
    print(f"\nMaking catalog of G1 patches found in directory: {patch_dir}")
    return list(Path(patch_dir).rglob('*.pch', case_sensitive=None))
    # return Path(patch_dir).rglob('*.zaxd')


def make_textfile(patch_dir, max_patch_file):
    """
    Iterate over a list of patch names, replace the \\ be changed to / to be comptible with MAX/Msp
    """
    status = 0

    patch_names = generate_patch_file(patch_dir)
    if patch_names:
        with open(max_patch_file, 'w', encoding="utf-8") as fh_out:
            # loop over the raw patch names, write them to the file that will be used by MAX
            patch_count = 0
            for patch in patch_names:
                # replace \\ with / , write back to same file in order to be compatible with MAX
                fh_out.write(f"{str(patch.absolute()).replace('\\','/')}\n")
                patch_count += 1

        print(f"\n{patch_count:,} patches were found and written to {max_patch_file}.\n")
    else:
        status = 1
        print("\nERROR. No patch names were found at {patch_dir}.\n\n")

    return status


def read_patches(max_patchfile):
    """

    Args:
        max_patchfile (string): a filename containing the patch names to be read

    Returns:
        list: absolute paths of G1 patch names read from max_patchfile
    """

    patches = []
    with open(max_patchfile, 'r', encoding="utf-8") as fh_in:
        patches = fh_in.readlines()

    return patches


def show_patch(max_patchfile, patch_number):
    """
    Display the patch name specified by the patch number that is passed on the command line
    """

    status = 0 # success
    if Path(max_patchfile).exists():
        patch_names = read_patches(max_patchfile)
        if patch_names:
            patch_count = len(patch_names)

            if patch_number > patch_count:
                print(f'\nYou specified Patch # {patch_number}, but there are only {patch_count} patches in {max_patchfile}.\n')
            else:
                for line_number, line in enumerate(patch_names, start=1):
                    if line_number == patch_number:
                        print(f'\n\tPatch #{patch_number}: {line}')
                        break
        else:
            status = 1
            print("\nERROR. No patch names were found at {AUDIO_ROOTDIR}.\n\n")
    else:
        status = 1
        print(f'\n\n\t{max_patchfile} was not found. You must run the program with the --maketext argument first.')

    return status


def process_cmd_line():
    """
    Create the Argumnet parser for the cmd line options
    Returns:
        Argparse Namespace: Namespace and values created based on the cmd line arguments passed in
    """
    parser = argparse.ArgumentParser(
                        prog='g1_patches',
                        description='Creates a texfile containing the filenames of Nord Modular G1 patches.',
                        epilog='') # shown at the bottom of the help message
    
    parser.add_argument('--maketext', default=False, action='store_true', help='Create a text file containing all of the Nord Modular patch names.')
    parser.add_argument('--showpatch', default=None, type=int, metavar='PATCH_NUMBER', help='Show the patch name specified by the patch number. This assumes the program has been previously run with the "maketext" argument.')
    parser.add_argument('--patchdir', default=None, help='The directory where the patches are located. The default directory is "patches" in the current directory.')
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
    """
    Entry point for the program

    Returns:
        int: status value indicating if the program was successful or not. 0 = success, non-zero is error/failure
    """


    status = 0
    args = process_cmd_line()

    if args.patchdir is not None:
        patch_dir = args.patchdir # the user specified a directory on the cmd line
    else:
        patch_dir = 'patches' # default patch directory when the user doesn't specify one
    max_patchfile = rf'{patch_dir}\g1-patches-max.txt'

    if args.maketext:
        status = make_textfile(patch_dir, max_patchfile)
    elif args.showpatch is not None:
        patch_number = args.showpatch
        status = show_patch(max_patchfile, patch_number)

    return status

if __name__ == "__main__":
    sys.exit(main())
