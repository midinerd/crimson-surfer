# crimson-surfer


## Overview
Crimson_surfer is an idea originally conceived by crissaegrim/midinerd in order to make it easy to listen to directories full of patch files
for the Clavia Nord Modular (G1) virtual modular synthesizer.

The "original implementation" was a clever combination of a Python program which feeds a list of G1 patch names into Max/MSP. Max would "send" the patch file
to the Nord Modular Editor program, followed by a series of MIDI notes to the Nord Modular synthesizer. This makes it very easy to listen to many patches without the drudgery of having to load each one manually.

Later modifications by Reddy Kilowatt (Tony Cappellini) removed the need for Max/MSP to
send the MIDI notes to the synthesizer. A pure-python implementation is the result, thanks to the MIDO Python library.




## System Requirements
* A PC with Windows 10 (The professional version was used for development, other versions have not been tested but are expected to work as well.)
* Python 3 (if you want to run crimson_surfer from source, otherwise a stand-alone version will be available for those who don't have Python installed.)
* The Nord Modular (G1) Editor or
* The Nord Modular (G2) Editor or
* The Nord Modular (G2) Demo Editor (no hardware synthesizer is required.)



## Hardware Requirements
* A MIDI interface.
* A Nord Modular G1 Synthesizer or
* A Nord Modular G2 Synthesizer



ORIGINAL DESCRIPTION: to be deleted and added above.
Tested on Windows 10:

Crimson Surfer is a collection of technologies that take a G1 Nord Modular and Windows10 PC with python & Max/MSP into an automated patch-file demonstrator.

At the time of commit its behavior is:

 - Recurse from a given root folder and discover all .pch files
 - generate a .txt file of the paths of those .pch files
 - the .maxpat will, on a timed interval, step through the lines of the patchfile bank and envoke the G1 Editor to open the .pch filepath
 - Max sends 1 note-on to octave 0 for 8 seconds followed by a note-off, then the same to octave 1, ... up to octave 10
 - Then max will increment the line# of patch filepath to load and repeat this process
 - The user may press shift+spacebar to log the given filepath & note-number if they like what they hear.



