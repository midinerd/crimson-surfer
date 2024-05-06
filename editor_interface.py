"""
This module provides an interface from the Nord Modular Editor to the program
used to control it
"""

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
