# crimson-surfer

Tested on Windows 10:

Crimson Surfer is a collection of technologies that take a G1 Nord Modular and Windows10 PC with python & Max/MSP into an automated patch-file demonstrator.

At the time of commit its behavior is:

 - Recurse from a given root folder and discover all .pch files
 - generate a .txt file of the paths of those .pch files
 - the .maxpat will, on a timed interval, step through the lines of the patchfile bank and envoke the G1 Editor to open the .pch filepath
 - Max sends 1 note-on to octave 0 for 8 seconds followed by a note-off, then the same to octave 1, ... up to octave 10
 - Then max will increment the line# of patch filepath to load and repeat this process
 - The user may press shift+spacebar to log the given filepath & note-number if they like what they hear.

# Requirements:

- Max/MSP
- Python 3
- `shell` External from Cycling'74 repo: [releases] (https://github.com/jeremybernstein/shell/releases)
- - add `shell` to max/msp's external paths
- The G1 Editor
- A Nord Modular G1
- The Max/MSP patcher will need its midi output port set to the port of your Nord Modular G1


