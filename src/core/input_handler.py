from gi.repository import Gtk, Gdk

class InputHandler:
    def __init__(self, on_bit_flip=None):
        self.on_bit_flip = on_bit_flip
        self.controller = Gtk.EventControllerKey.new()
        self.controller.connect("key-pressed", self._on_key_pressed)


    def _on_key_pressed(self, controller, keyval, keycode, state):
        if not self.on_bit_flip:
            return Gdk.EVENT_PROPAGATE

        # Check for number keys 1-8
        if 49 <= keyval <= 56:  # Keys 1-8
            bit_index = keyval - 49
            self.on_bit_flip(bit_index)
            return Gdk.EVENT_STOP

        # Check for numpad keys 1-8
        elif 65457 <= keyval <= 65464:  # Numpad 1-8
            bit_index = keyval - 65457
            self.on_bit_flip(bit_index)
            return Gdk.EVENT_STOP

        return Gdk.EVENT_PROPAGATE
