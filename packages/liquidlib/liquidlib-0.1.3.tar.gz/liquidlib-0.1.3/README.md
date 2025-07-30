# liquidlib

A Python library for modeling and interpolating physical properties of liquids at specified temperatures. This library is particularly useful for laboratory automation and liquid handling systems.

## Features

- Temperature-based interpolation of liquid properties:
  - Vapor pressure
  - Density
  - Surface tension
  - Viscosity
- Automatic calculation of liquid handling parameters based on physical properties
- JSON serialization support
- Comprehensive test coverage
- **Opentrons robot integration** for automated liquid handling

## Installation

```bash
pip install liquidlib
```

## Usage

### Basic Usage

```python
from liquidlib import Liquid

# Create a liquid with properties at 20°C and 25°C
liquid = Liquid(
    vapor_pressure_20c=100,    # Vapor pressure at 20°C
    vapor_pressure_25c=120,    # Vapor pressure at 25°C
    density_20c=1.0,          # Density at 20°C
    density_25c=0.98,         # Density at 25°C
    surface_tension_20c=72,   # Surface tension at 20°C
    surface_tension_25c=70,   # Surface tension at 25°C
    viscosity_20c=1.0,        # Viscosity at 20°C
    viscosity_25c=0.9,        # Viscosity at 25°C
    lab_temperature=22.5      # Current lab temperature
)

# Access interpolated properties
print(f"Density at {liquid._lab_temp}°C: {liquid.density}")
print(f"Viscosity at {liquid._lab_temp}°C: {liquid.viscosity}")

# Get liquid handling parameters
print(f"Aspirate speed: {liquid.handling.aspirate_speed}")
print(f"Dispense speed: {liquid.handling.dispense_speed}")

# Export to JSON
json_data = liquid.to_json()
```

### Custom Handling Parameters

```python
from liquidlib import Liquid, LiquidHandling

# Create custom handling parameters
handling = LiquidHandling(
    trailing_air_gap=2.0,
    blowout=5.0,
    pre_wet=True,
    aspirate_speed=0.8,
    dispense_speed=0.6
)

# Create liquid with custom handling
liquid = Liquid(
    vapor_pressure_20c=100,
    vapor_pressure_25c=120,
    density_20c=1.0,
    density_25c=0.98,
    surface_tension_20c=72,
    surface_tension_25c=70,
    viscosity_20c=1.0,
    viscosity_25c=0.9,
    handling=handling
)
```

### Using Pre-defined Liquid Classes

The library comes with several pre-defined liquid classes for common laboratory liquids. These classes have carefully measured physical properties and are ready to use:

```python
from liquidlib.liquids import Water, Ethanol, Glycerin, DMSO

# Create instances with default lab temperature (22.5°C)
water = Water()
ethanol = Ethanol()

# Or specify a custom lab temperature
glycerin = Glycerin(lab_temperature=25.0)
dmso = DMSO(lab_temperature=23.5)

# Access physical properties
print(f"Water density at {water._lab_temp}°C: {water.density} g/mL")
print(f"Ethanol viscosity at {ethanol._lab_temp}°C: {ethanol.viscosity} mPa·s")

# Get optimized handling parameters
print(f"Glycerin aspirate speed: {glycerin.handling.aspirate_speed}")
print(f"DMSO dispense speed: {dmso.handling.dispense_speed}")

# Export to JSON for storage or sharing
water_json = water.to_json()
```

Available pre-defined liquids include:
- `Water`: Standard laboratory water
- `Ethanol`: 100% ethanol
- `Glycerin`: Pure glycerin
- `DMSO`: Dimethyl sulfoxide

The community is encouraged to add more!

Each pre-defined class comes with:
- Accurate physical properties at multiple temperatures
- Optimized handling parameters
- Temperature-based property interpolation
- JSON serialization support

### Opentrons Robot Integration

liquidlib includes an adapter for Opentrons pipetting robots, making it easy to handle viscous liquids with optimized parameters. The `OpentronsLiquidHandler` class provides specialized methods for aspirating and dispensing viscous liquids with robot-specific optimizations.

#### Basic Opentrons Usage

```python
from liquidlib.adapters.opentrons import OpentronsLiquidHandler
from liquidlib import Liquid, LiquidHandling

# In your Opentrons protocol
def run(protocol: protocol_api.ProtocolContext):
    # Setup your labware and instruments
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '4')
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[tiprack])
    tube_rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '5')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '6')
    
    # Initialize the liquid handler with optimized parameters
    handler = OpentronsLiquidHandler(protocol, p300, 'optimized_pipette_parameters.csv')
    
    # Create a liquid object using liquidlib
    glycerol = Liquid(
        vapor_pressure_20c=0.0001,
        vapor_pressure_25c=0.0002,
        density_20c=1.26,
        density_25c=1.25,
        surface_tension_20c=63.0,
        surface_tension_25c=62.0,
        viscosity_20c=945.0,
        viscosity_25c=800.0,
        lab_temperature=22.5
    )
    
    # Method 1: Use predefined parameters from CSV file
    handler.handle_liquid("Glycerol 90%", 75, tube_rack['A1'], plate['E5'])
    
    # Method 2: Use liquidlib-calculated parameters
    aspiration_rate = glycerol.handling.aspirate_speed * 300  # Convert to µL/s
    dispense_rate = glycerol.handling.dispense_speed * 300    # Convert to µL/s
    
    handler.aspirate_viscous(
        75, tube_rack['A1'], 
        liquid_name="Glycerol 90%",
        aspiration_rate=aspiration_rate
    )
    
    handler.dispense_viscous(
        75, plate['E5'],
        liquid_name="Glycerol 90%", 
        dispense_rate=dispense_rate
    )
```

#### Key Features

- **Optimized Parameters**: Uses CSV-based lookup tables for proven liquid/pipette combinations
- **Fallback Support**: Falls back to liquidlib-calculated parameters if CSV data isn't available
- **Flexible Override**: Allows explicit parameter overrides for fine-tuning
- **Temperature Awareness**: Integrates with liquidlib's temperature-dependent property interpolation
- **Robot-Specific**: Optimized for Opentrons pipetting robots and their specific capabilities

#### Parameter CSV Format

The `OpentronsLiquidHandler` expects a CSV file with the following columns:
- `Pipette`: Pipette model (e.g., "P300")
- `Liquid`: Liquid name (e.g., "Glycerol 90%")
- `Aspiration Rate (µL/s)`: Optimal aspiration rate
- `Aspiration Delay (s)`: Delay after aspiration
- `Aspiration Withdrawal Rate (mm/s)`: Tip withdrawal speed
- `Dispense Rate (µL/s)`: Optimal dispense rate
- `Dispense Delay (s)`: Delay after dispensing
- `Blowout Rate (µL/s)`: Blowout rate
- `Touch tip`: Whether to touch tip (Yes/No)

See the `examples/opentrons_example.py` file for a complete working example.

### Creating a Specialized Liquid Class

You can create custom liquid classes by inheriting from the `Liquid` base class. This is useful for defining specific types of liquids with predefined properties or additional functionality.

Here's an example of creating a specialized liquid class for a specific use case - Berkeley Hot Summer Glycerin, which needs to account for higher ambient temperatures:

```python
from liquidlib import Liquid

class BerkeleyHotHotSummerGlycerin(Liquid):
    def __init__(self, lab_temperature=35.0):  # Higher default temperature for hot summer
        super().__init__(
            # Physical properties at 20°C and 25°C
            vapor_pressure_20c=0.0001,    # Very low vapor pressure
            vapor_pressure_25c=0.0002,    # Still very low at higher temp
            density_20c=1.261,           # High density
            density_25c=1.258,           # Slightly lower at higher temp
            surface_tension_20c=63.4,    # High surface tension
            surface_tension_25c=62.5,    # Slightly lower at higher temp
            viscosity_20c=1412,          # Very high viscosity
            viscosity_25c=934,           # Significantly lower at higher temp
            lab_temperature=lab_temperature
        )

# Create an instance for a hot Berkeley summer day
glycerin = BerkeleyHotHotSummerGlycerin(lab_temperature=38.0)

# The liquid handling parameters automatically adapt to the physical properties
print(f"Current lab temperature: {glycerin._lab_temp}°C")
print(f"Interpolated viscosity: {glycerin.viscosity} mPa·s")
print(f"Adapted aspirate speed: {glycerin.handling.aspirate_speed}")
print(f"Adapted dispense speed: {glycerin.handling.dispense_speed}")
print(f"Adapted trailing air gap: {glycerin.handling.trailing_air_gap}")
```

The key advantage of this approach is that the `LiquidHandling` parameters automatically adapt to the physical properties of the liquid. For example:
- Higher viscosity leads to slower aspirate/dispense speeds
- Higher surface tension affects the trailing air gap
- Temperature changes automatically update all interpolated properties
- The handling parameters are optimized for the specific liquid's characteristics

## Development

To set up the development environment:

```bash
# Clone the repository
git clone https://github.com/yourusername/liquidlib.git
cd liquidlib

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.



