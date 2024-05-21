"""
This module provides an interface from the Nord Modular Editor to the program
used to control it
"""
from pathlib import Path
import subprocess as sub

class EditorInterface:
    """
    Provides the methods to control the Nord Modular Editor from
    another Python module
    """
    def __init__(self, editor_path ):
        self.editor_path = editor_path
        self.process = None


    def send_patch(self, absolute_path_to_patch):
        """
        Send a patch to the Nord editor 

        Args:
             (str): A string containing the absolute path to a G1 patch file
        """
        status = 0
        try:
            args = [self.editor_path, absolute_path_to_patch.strip()]
            self.process = sub.Popen(args, universal_newlines=True, shell=False)
            # self.editor.stdin.write(absolute_path_to_patch) # writing to stdin doesn't work
        except FileNotFoundError:
            status = 1
            print(f"\nERROR: File Not Found: {self.editor_path}\n")
        except sub.SubprocessError as exc:
            status = 1
            print(f'\nERROR occurred sending {Path(absolute_path_to_patch).name} to the Nord Editor: {exc}\n\n')


        return status

    def terminate_process(self):
        """Provide a method to the caller to terminate the subprocess so as not to leave
        any zombies running.
        """
        status = 0
        if self.process is not None:
            print(f"\nTerminating subprocess ID: {self.process.pid}")
            self.process.terminate() # it looks like the editor was terminated, but can still be seen running in Task Manager
            self.process.wait(45)
        else:
            print("\nSubprocess is not running, so nothing to terminate.")
            
        return status