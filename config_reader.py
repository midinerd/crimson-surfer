from collections import namedtuple
import configparser as cfg

# putting the namedtuple definition here allows VScode to resolve the fields
EditorParams = namedtuple("Params", "editor_path midi_port midi_channel note_delay num_notes")


def read_config_file(config_file='editor_config.ini') -> EditorParams:
    """
    Read the parameters from the config file so that the program
    knows where the editor is and which midi channel to use.

    The config file is read every time the user uses the --play argument on the cmd
    line, so that the changes entered into the config file will be used during the next play session.

    Args:
        config_file (optional): _description_. Defaults to 'NordConfig.ini'.

    Returns:
        str: absolute path to the nord editor including the the editor name
        int: the midi channel to use when sending notes to the editor
    """

    config = cfg.ConfigParser()
    if not config.read(config_file):
        print(f'\nERROR occurred reading config file: {config_file}\n')
        return None


    editor_path = config['PATH']['nordeditor']
    midi_port = config['MIDI']['midi_port_name']
    midi_channel = int(config['MIDI']['midi_channel'])
    note_delay = int(config['NOTES']['note_delay'])
    num_notes  = int(config['NOTES']['num_notes'])

    params = EditorParams(editor_path, midi_port, midi_channel, note_delay, num_notes)

    return params


def write_default_config():
    """
    When a config file isn't found, write a default file so that the user
    knows what the config file entries should look like
    """
    pass
