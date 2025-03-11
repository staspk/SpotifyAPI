
from __future__ import annotations

class Color:
    def __init__(self, red: int, green: int, blue: int):
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError('color values must be between 0 and 255.')

        self.red = red
        self.green = green
        self.blue = blue
    
    @staticmethod
    def from_int(color: int) -> Color:
        red   = color & 0xFF
        green = (color >> 8) & 0xFF
        blue  = (color >> 16) & 0xFF

        return Color(red, green, blue)
    
    @staticmethod
    def from_hex(string: str) -> Color:
        if string.startswith("#"):
            string = string[1:]
            
        if len(string) != 6:
            raise ValueError("Hex string must be 6 characters long (e.g. 'FFAABB').")
        
        try:
            red = int(string[0:2], 16)
            green = int(string[2:4], 16)
            blue = int(string[4:6], 16)
        except ValueError:
            raise ValueError("Invalid hex string. Ensure it contains only hexadecimal digits.")
        
        return Color(red, green, blue)
    
    def as_int(self) -> int:
        return self.red + (self.green << 8) + (self.blue << 16)     # Note: we are shifting bits here, 1 byte

    def as_hex(self) -> str:
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"