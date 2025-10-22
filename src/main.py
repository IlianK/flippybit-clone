import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .views.main_window import FlippybitWindow  # Use relative import

class FlippybitApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.example.flippybit')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = FlippybitWindow(application=self)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

def main(version):
    app = FlippybitApplication()
    return app.run(sys.argv)
