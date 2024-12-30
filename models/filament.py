class Filament:
    def __init__(self, id=None, manufacturer=None, filament_type=None, color_name=None, custom_name=None):
        self.id = id
        self.manufacturer = manufacturer
        self.type = filament_type
        self.color_name = color_name
        self.custom_name = custom_name

    def __str__(self):
        return f"Filament.py(id={self.id}, manufacturer='{self.manufacturer}', type='{self.type}', color_name='{self.color_name}')"

