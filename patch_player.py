
"""Provides an object that handles all of the details of playing the patches from
a text file

"""
from pathlib import Path
import time

from midi_interface import MidiInterface
from editor_interface import EditorInterface

# from config_reader import EditorParams
from config_reader import read_config_file
from config_reader import EditorParams


class PatchPlayer:
    """Provides an object that handles all of the details of playing the patches from
    a text file

    """

    def __init__(self):
        self.editor_params = read_config_file()
        self.midi_interface = MidiInterface(self.editor_params.midi_port, self.editor_params.midi_channel)

        # create an instance of the editor interface so that this program can send patches to the editor
        self.editor = EditorInterface(self.editor_params.editor_path)


    def play_patches(self, patch_file):
        """
        Sending patches to the NM editor, then send some midi notes based on the parameters
        in the config file.
        """

        patch_names = self.read_patches(patch_file)
        if patch_names:
            print()

            status = 0
            try:
                for patch_num, this_patch in enumerate(patch_names, start=1):
                    print(f"\t{patch_num:5} SENDING: '{this_patch}'")
                    status = self.editor.send_patch(this_patch)
                    if status:
                        print(f'\n\nAn error occurred while sending "{Path(this_patch).name}" to the editor.')
                        break
                    else:
                        self.send_notes()
                    time.sleep(4)
            except KeyboardInterrupt:
                print("\n\tUSER ABORT\n\n")
        else:
            status = 1
        return status

    def send_notes(self):
        """_summary_
        """
        # params = EditorParams(editor_path, midi_port, midi_channel, note_delay, midi_notes)

        midi_notes = self.editor_params.midi_notes
        for this_note in midi_notes:
            self.midi_interface.send_note(this_note)
            time.sleep(2) #
            self.midi_interface.panic() # turn notes off before going to the next patch

    def read_patches(self, max_patchfile):
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


    def show_patch(self, max_patchfile, patch_number):
        """
        Display the patch name specified by the patch number that is passed on the command line
        """

        status = 0 # success
        if Path(max_patchfile).exists():
            patch_names = self.read_patches(max_patchfile)
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


    def generate_patch_file(self, patch_dir):
        """
        Return a generator object of G1 patch names, return them to the caller as a Python list, for simple iteration.
        """
        
        print(f"\nMaking catalog of G1 patches found in directory: {patch_dir}")
        # return list(Path(patch_dir).rglob('*.pch', case_sensitive=None))
        return Path(patch_dir).rglob('*.pch', case_sensitive=None)


    def make_textfile(self, patch_dir, max_patch_file):
        """
        Iterate over a list of patch names, replace the \\ be changed to / to be comptible with MAX/Msp
        """
        status = 0

        patch_names = self.generate_patch_file(patch_dir)
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


    def show_ports(self):
        """Display the MIDI out ports so the user can choose which one to use
        """
        print("\nMidi Out Ports available to this program.\n")
        for enum, port in enumerate(self.midi_interface.get_midi_output_ports()):
            print(f'Port # {enum}  {port}')
