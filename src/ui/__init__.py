import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

# GameArea template class
@Gtk.Template(resource_path='/com/example/flippybit/ui/game_area.ui')
class GameArea(Gtk.Box):
    __gtype_name__ = 'GameArea'

    game_area = Gtk.Template.Child()
    live_hex_label = Gtk.Template.Child()
    bit_container = Gtk.Template.Child()
    status_label = Gtk.Template.Child()
    start_button = Gtk.Template.Child()

# Export the classes
__all__ = ['GameArea']
