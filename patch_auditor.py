# copyright crissaegrim/midinerd(c) 2024  whatever that means.

import argparse
import atexit
from pathlib import Path
import sys


from patch_player import PatchPlayer

def process_cmd_line():
    """
    Create the Argument parser for the cmd line options
    Returns:
        Argparse Namespace: Namespace and values created based on the cmd line arguments passed in
    """
    parser = argparse.ArgumentParser(
                        # prog='g1_patches',
                        prog=__file__,
                        description='Creates a texfile containing the filenames of Nord Modular G1/G2 patch names.',
                        epilog='\n                            ******** This program MUST be run from a Windows command prompt with ADMINISTRATOR PRIVELEGES ********\n') # shown at the bottom of the help message
    
    parser.add_argument('--maketext', default=False, action='store_true', help='Create a text file containing the full path to the patch names.')
    parser.add_argument('--patchdir', default=None, help='The directory where the patches are located. The default directory is "patches" in the current directory.')

    parser.add_argument('--showpatch', default=None, type=int, metavar='PATCH_NUMBER', help='Show the patch name specified by the patch number. This assumes the program has been previously run with the "maketext" argument.')

    parser.add_argument('--showports', default=False, action='store_true', help='Display the Midi out ports on the system.')

    parser.add_argument('--synth_type', choices=["g1","g2"], help='Specify the G1 or G2 editor to play the patches.')

    play_group = parser.add_mutually_exclusive_group()
    play_group.add_argument('--play', default=False, action='store_true', help='Start the Nord Editor, send it a patch and some notes to play it.')
    play_group.add_argument('--allnotesoff', default=False, action='store_true', help='Turn off all notes on all channels.')

    args = parser.parse_args()

    # check for no arguments passed, print help message
    if len(sys.argv) == 1:
        args = None # tells the caller to exit
        print()
        parser.print_help() # show the help message when no arguments are passed.

    return args


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
    player = None
    
    if args is not None:
        
        synth_type = args.synth_type
        try:
            player = PatchPlayer(synth_type)
        except OSError as exc:
            status = 1
            print(f'{exc}')
        else:
            # this ensures the subprocesses are terminated if something bad happens
            atexit.register(player.terminate_process) 

            if args.patchdir is not None:
                patch_dir = args.patchdir # the user specified a patch directory on the cmd line
            else:
                patch_dir = 'patches' # default patch directory when the user doesn't specify one
            max_patchfile = str(Path(rf'{patch_dir}\{synth_type}-patches-max.txt').resolve())
            
            if args.allnotesoff:
                player.all_notes_off()
                
            if args.maketext:      
                status = player.make_textfile(patch_dir, max_patchfile)

            if args.showpatch is not None:
                patch_number = args.showpatch
                status = player.show_patch(max_patchfile, patch_number)

            if args.play:
                status = player.play_patches(max_patchfile)

            if args.showports:
                player.show_ports()

        print(f'\n\t Exiting the program with status: {status}\n\n')
    else:
        status = 1 # error
            
    return status

if __name__ == "__main__":
    sys.exit(main())
    
