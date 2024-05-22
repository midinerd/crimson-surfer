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
        self.processes = []


    def send_patch(self, absolute_path_to_patch):
        """
        Send a patch to the Nord editor 

        Args:
             (str): A string containing the absolute path to a G1 patch file
        """
        status = 0
        try:
            args = [self.editor_path, absolute_path_to_patch.strip()]
            self.processes.append(sub.Popen(args, universal_newlines=True, shell=False))
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

        # gotta be an admin for this
        # result = sub.run(["taskkill", "/im", Path(self.editor_path).name, "/f", "/t"], timeout=10)
        term_proc = sub.Popen(["taskkill", "/im", Path(self.editor_path).name, "/f", "/t"])
        print(f"\nReturn code from termination: {term_proc.returncode}")            
        #status = term_proc.returncode
        
        # this seems to work- gotta be an admin
        # for proc in self.processes:
        #     print(f"\nTerminating subprocess ID: {proc.pid}")
        #     # proc.kill()
        #     # proc.terminate() # it looks like the editor was terminated, but can still be seen running in Task Manager
        #     # self.process.wait(45)
        return status