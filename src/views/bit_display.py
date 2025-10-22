from gi.repository import Gtk

class BitDisplay:
    def __init__(self, bit_container, on_bit_clicked=None):
        self.bit_container = bit_container
        self.on_bit_clicked = on_bit_clicked
        self.bits = []
        self.create_display()

    def create_display(self):
        # Clear existing bits
        for child in self.bit_container:
            self.bit_container.remove(child)
        self.bits.clear()

        # Create 8 bits
        for i in range(8):
            bit_button = Gtk.Button()
            bit_button.set_label("0")
            bit_button.set_size_request(60, 60)
            bit_button.add_css_class("pill")
            bit_button.add_css_class("osd")
            bit_button.set_tooltip_text(f"Press {i+1} to flip")

            if self.on_bit_clicked:
                bit_button.connect("clicked", self.on_bit_clicked, i)

            self.bit_container.append(bit_button)
            self.bits.append(bit_button)

    def flip_bit(self, bit_index, value=None):
        if 0 <= bit_index < len(self.bits):
            button = self.bits[bit_index]
            if value is None:
                # Toggle
                current = button.get_label()
                new_value = "1" if current == "0" else "0"
            else:
                new_value = "1" if value else "0"

            button.set_label(new_value)

            # Update style
            if new_value == "1":
                button.add_css_class("suggested-action")
            else:
                button.remove_css_class("suggested-action")

    def reset(self):
        for button in self.bits:
            button.set_label("0")
            button.remove_css_class("suggested-action")

    def get_binary_string(self):
        return "".join(button.get_label() for button in self.bits)

    def get_binary_value(self):
        return int(self.get_binary_string(), 2)
