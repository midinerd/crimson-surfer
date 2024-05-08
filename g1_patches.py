# copyright crissaegrim/midinerd(c) 2024  whatever that means.

import argparse
from collections import namedtuple
import configparser as cfg
from pathlib import Path
import sys
import time


from editor_interface import EditorInterface

# putting the namedtuple definition here allows VScode to resolve the fields
EditorParams = namedtuple("Params", "editor_path midi_channel note_delay num_notes")


def read_config_file(config_file='editor_config.ini') -> EditorParams:
    """
    Read the parameters from the config file so that the program
    knows where the editor is and which midi channel to use.

    The config file is read every time the user uses the --play argument on the cmd
    line, so that the changes entered into the config file will be used during the next play session.

    Args:
        config_file (optional): _description_. Defaults to 'NordConfig.ini'.

    Returns:
        str: absolute path to the nord editor including the the editor name
        int: the midi channel to use when sending notes to the editor
    """

    config = cfg.ConfigParser()
    if not config.read(config_file):
        print(f'\nERROR occurred reading config file: {config_file}\n')
        return None


    editor_path = config['PATH']['nordeditor']
    midi_channel = int(config['MIDI']['midi_channel'])
    note_delay = int(config['NOTES']['note_delay'])
    num_notes  = int(config['NOTES']['num_notes'])

    #EditorParams = namedtuple("Params", "editor_path midi_channel note_delay num_notes")
    params = EditorParams(editor_path, midi_channel, note_delay, num_notes)

    return params


def write_default_config():
    """
    When a config file isn't found, write a default file so that the user
    knows what the config file entries should look like
    """
    pass


def generate_patch_file(patch_dir):
    """
    Return a generator object of G1 patch names, return them to the caller as a Python list, for simple iteration.
    """
    
    print(f"\nMaking catalog of G1 patches found in directory: {patch_dir}")
    # return list(Path(patch_dir).rglob('*.pch', case_sensitive=None))
    return Path(patch_dir).rglob('*.pch', case_sensitive=None)


def make_textfile(patch_dir, max_patch_file):
    """
    Iterate over a list of patch names, replace the \\ be changed to / to be comptible with MAX/Msp
    """
    status = 0

    patch_names = generate_patch_file(patch_dir)
    if patch_names is not None:
        try:
            with open(max_patch_file, 'w', encoding="utf-8") as fh_out:
                # loop over the raw patch names, write them to the file that will be used by MAX
                patch_count = 0
                for patch in patch_names:
                    # replace \\ with / , write back to same file in order to be compatible with MAX
                    fh_out.write(f"{str(patch.resolve()).replace('\\','/')}\n")
                    patch_count += 1
                print(f"\n{patch_count:,} patches were found and written to {max_patch_file}.\n")
        except FileNotFoundError:
            status = 1
            print(f"\nERROR: The '{patch_dir}' directory does not exist.\n")
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
    if Path(max_patchfile).exists():
        with open(max_patchfile, 'r', encoding="utf-8") as fh_in:
            # patches = fh_in.readlines()
            patches = fh_in.read().splitlines() # gets rid of the newline at the end
    else:
        print(f"\nERROR: {max_patchfile} does not exist. You must run the program with the --maketext argument, FIRST.\n")
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
    parser.add_argument('--play', default=False, action='store_true', help='Start the Nord Editor, send it a patch and some notes to play it.')

    args = parser.parse_args()

    # check for no arguments passed, print help message
    if len(sys.argv) == 1:
        print()
        parser.print_help()
        sys.exit(1) #exit with an error code

    return args


def play_patches(editor_params: EditorParams, patch_file):
    """
    Instantiate the NM editor in a subprocess and start sending patches to it.
    """

    # create an instance of the editor inteface so that this program can send patches to the editor
    editor = EditorInterface(editor_params.editor_path, editor_params.midi_channel, editor_params.note_delay, editor_params.num_notes)

    patch_names = read_patches(patch_file)
    if patch_names:
        print()

        status = 0
        try:
            for patch_num, this_patch in enumerate(patch_names, start=1):
                print(f"\t{patch_num:5} SENDING: '{this_patch}'")
                status = editor.send_patch(this_patch)
                if status:
                    print(f'\n\nAn error occurred while sending "{Path(this_patch).name}" to the editor.')
                    break
                time.sleep(editor_params.note_delay)
        except KeyboardInterrupt:
            print("\n\tUSER ABORT\n\n")
    else:
        status = 1

    return status


# https://github.com/jeremybernstein/shell/releases
# the MAX shell object - binaries
def main():
    """
    Entry point for the program

    Returns:
        int: status value indicating if the program was successful or not. 0 = success, non-zero is error/failure
    """


    status = 0
    args = process_cmd_line()

    if args.patchdir is not None:
        patch_dir = args.patchdir # the user specified a patch directory on the cmd line
    else:
        patch_dir = 'patches' # default patch directory when the user doesn't specify one
    max_patchfile = str(Path(rf'{patch_dir}\g1-patches-max.txt').resolve())
    
    if args.maketext:      
        status = make_textfile(patch_dir, max_patchfile)

    if args.showpatch is not None:
        patch_number = args.showpatch
        status = show_patch(max_patchfile, patch_number)

    if args.play:
        editor_params = read_config_file()
        if editor_params is not None:
            status = play_patches(editor_params, max_patchfile)
        else:
            status = 1
    print(f'\n\t Exiting the program with status: {status}\n\n')
    return status

if __name__ == "__main__":
    sys.exit(main())
    
