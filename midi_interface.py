""" This class abstracts the details of the MIDO module, in order to make
MIDI port access easier for the user
"""

import mido
# import mido.backends.portmidi

class MidiInterface:
    """ Provide simple access to the midi ports
    """
    def __init__(self) -> None:
        self.output_port = None
        self.input_port = None
        self.midi_channel = 0

    def get_midi_output_ports(self):
        """Display the output MIDI ports, the user will choose one
        with another method.
        """
        return mido.get_output_names()

    def get_midi_input_ports(self):
        """Display the input ports, the user will use one with
        another method
        """
        return mido.get_input_ports()
