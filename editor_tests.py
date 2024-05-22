import subprocess
import os
import time

# where my editor is stored:
editor_location = r"G:\audio\nord\g1_editor\Nord Modular Editor v3.03.exe"

# 2 patch paths
p1 = r"G:\audio\g1\behind-the-locked-door.pch"
p2 = r"G:\audio\g1\choke-gen-2.pch"

# iterable for cycling through the patches
patches = [p1, p2]


def load_patch(patch_location):
    patch_open_cmd = [editor_location, patch_location]
    print(f'Loading patch, cmd: {patch_open_cmd}')
    subprocess.Popen(patch_open_cmd)
    print(f'Finished loading patch: {patch_location}')


def kill_editor():
    print(f'Killing editor.. {editor_location}')
    editor_binary_name = os.path.basename(editor_location)
    kill_cmd = ['taskkill', '/im', editor_binary_name, '/f'] # TASKKILL /im (image-name) executable.exe /f (force-kill)
    subprocess.Popen(kill_cmd)
    print(f'Finished sending kill cmd: {kill_cmd}')
    os.system('dir')


def cycle_patches():
    # this is just to emulate that there's many patches being cycled through instead of the meager 2
    cycle_count = 4
    patch_cieling = len(patches)
    idx = 0
    while idx < cycle_count:
        current_patch = patches[idx%patch_cieling]
        load_patch(current_patch)
        idx += 1
        time.sleep(5)


def run_demo():
    cycle_patches()
    kill_editor()


def main():
    run_demo()


if __name__ == "__main__":
    run_demo()
