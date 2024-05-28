""" This class abstracts the details of the MIDO module, in order to make
MIDI port access easier for the user
"""

import mido


class MidiInterface:
    """ Provide simple access to the midi ports
    """
    def __init__(self, output_port_name, midi_channel) -> None:
        self.output_port_name = output_port_name
        self.input_port = None
        self.midi_channel = midi_channel
        
        try:
            # if this isn't successful, the
            self.output_port = mido.open_output(self.output_port_name)
        except OSError as exc:
            raise OSError(f"\nERROR. Unable to open MIDI Out port: '{self.output_port_name}'") from exc

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
    
    def send_note(self, note_number):
        """_summary_

        Args:
            note_number (_type_): _description_
        """
        note_msg = mido.Message('note_on', time=1, note=note_number, velocity=127)
        self.output_port.send(note_msg)

    def panic(self):
        """
        Send All Notes off on all channels
        """
        self.output_port.panic()