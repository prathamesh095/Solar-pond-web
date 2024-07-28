from flask import Flask, render_template, request

app = Flask(__name__)

class SolarPond:
    SALT_PROPERTIES = {
        'NaCl': {'solubility_in_water': 35.7, 'melting_point': 801, 'boiling_point': 1413, 'density': 2.165, 'molar_mass': 58.44},
        'MgCl2': {'solubility_in_water': 54.3, 'melting_point': 714, 'boiling_point': 1412, 'density': 2.32, 'molar_mass': 95.211},
        # Add more salt types and their properties as needed
    }

    def __init__(self, surface_area, depth, salt_type, solar_radiation):
        self.surface_area = surface_area
        self.depth = depth
        self.salt_properties = self.SALT_PROPERTIES.get(salt_type, {})
        self.solar_radiation = solar_radiation

    def calculate_dimensions(self):
        length = width = self.surface_area ** 0.5
        return length, width

    def calculate_capacity(self):
        capacity = self.surface_area * self.depth
        return capacity

    def calculate_temperature(self):
        temperatures = [self.solar_radiation / (i + 1) for i in range(3)]
        return temperatures

    def calculate_salinity(self):
        if self.salt_properties:
            salinities = [self.salt_properties.get('solubility_in_water', 0) * (i + 1) for i in range(3)]
            return salinities
        return []

    def display(self):
        length, width = self.calculate_dimensions()
        capacity = self.calculate_capacity()
        temperatures = self.calculate_temperature()
        salinities = self.calculate_salinity()
        density = self.salt_properties.get('density', 0)
        molar_mass = self.salt_properties.get('molar_mass', 0)
        return length, width, capacity, temperatures, salinities, density, molar_mass

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            surface_area = float(request.form.get('surface_area'))
            depth = float(request.form.get('depth'))
            solar_radiation = float(request.form.get('solar_radiation'))

            if surface_area <= 0 or depth <= 0 or solar_radiation <= 0:
                raise ValueError("Surface area, depth, and solar radiation must be positive numbers.")
            
            salt_type = request.form.get('salt_type', 'NaCl')
            if salt_type not in SolarPond.SALT_PROPERTIES:
                raise ValueError("Invalid salt type. Please choose from: " + ', '.join(SolarPond.SALT_PROPERTIES.keys()))

            pond = SolarPond(surface_area, depth, salt_type, solar_radiation)
            length, width, capacity, temperatures, salinities, density, molar_mass = pond.display()
            return render_template('index.html', length=length, width=width, capacity=capacity, temperatures=temperatures, salinities=salinities, density=density, molar_mass=molar_mass)
        except ValueError as ve:
            error_message = str(ve)
            return render_template('index.html', error=error_message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
