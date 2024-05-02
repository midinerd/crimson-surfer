# copyright crissaegrim/midinerd(c) 2024  whatever that means.

# this file is a work in progress and won't simply "just work"
# it assumes an audio directory at g:/audio (edit line 10 to change this)
# and that it is being run in DOS (dir *.pch > ... collects and outputs your .pch list)
import io
import os
import sys

# currently only used/tested on win10 hence the cmd.exe and g:/ os bits lying around

AUDIO_ROOTDIR = 'g:/audio'
AUDIO_ROOTDIR = 'patches'

def make_textfile():
    filename = 'g1-raw-patches.txt'
    os.chdir(AUDIO_ROOTDIR)
    os.system('dir *.pch /s /b > g1-raw-patches.txt')
    txt = io.open(filename, 'r', encoding='utf8', errors='ignore')
    final_text = io.open(os.path.join(AUDIO_ROOTDIR, 'g1-patches.txt', 'w'))
    # convert path slashes for readability in max/msp \ -> /
    idx = 0
    for line in txt.readlines():
        line = line.replace('\\','/')
        final_text.write(line)
        idx += 1
    txt.close()
    final_text.close()
    get_patch(0)

def get_patch(patch_number):
    patch_number = int(patch_number)
    txt = io.open(os.path.join(AUDIO_ROOTDIR, 'g1-patches.txt'),mode='r', encoding='utf-8', errors='ignore')
    idx = 0
    for line in txt.readlines():
        if idx != patch_number:
            idx += 1
            continue
        if idx == patch_number:
            print(line)
            break

if __name__ == "__main__":
    # searches the filesystem at line:10 (i.e. g:/audio) and produces a text of any .pch files
    # adjusts the textfile to have any backslashes as forwardslashes \ -> /
    # dumps the file as g1-patches.txt
    # usage:
    # ex: python g1_patcher.py maketext
    if sys.argv[1] == "maketext":
        make_textfile()
    # ex: python g1_patcher.py 1   # prints index 1 (line#2 within the generated g1-patches.txt)
    # expects that maketext (line 37) has already been run once and can be used
    # to just output other lines in the text file.
    if sys.argv[1] == "get-patch":
        get_patch(sys.argv[2])
