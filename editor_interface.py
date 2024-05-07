"""
This module provides an interface from the Nord Modular Editor to the program
used to control it
"""
import subprocess as sub

class EditorInterface:
    """
    Provides the methods to control the Nord Modular Editor from
    another Python module
    """
    def __init__(self, path, midi_channel, note_delay, num_notes):
        self.editor_path = path
        self.midi_channel = midi_channel
        self.note_delay = note_delay
        self.num_notes = num_notes
        self.editor = None


    def send_patch(self, absolute_path_to_patch):
        """
        Send a patch to the Nord editor 

        Args:
             (str): A string containing the absolute path to a G1 patch file
        """
        status = 0
        try:
            args = [self.editor_path, absolute_path_to_patch.strip()]
            self.editor = sub.Popen(args, universal_newlines=True, shell=False)
            # self.editor.stdin.write(absolute_path_to_patch) # writing to stdin doesn't work
        except FileNotFoundError:
            status = 1
            print(f"\nERROR: File Not Found: {self.editor_path}\n")

        return status
    
    def play_patches(self, patch_file):
        """
        Loop over all of the patches in patch_file. When playing all of the patches is done,
        should this function terminate the editor ????

        This function will handle all exception handling so that the user doesn't need to
        
        Args:
            patch_file (_type_): _description_
        """
        pass
