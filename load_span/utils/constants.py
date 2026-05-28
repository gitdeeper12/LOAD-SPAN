"""Material properties and safety thresholds constants."""

# Material properties for common structural materials
MATERIAL_PROPERTIES = {
    'steel_S235': {
        'E': 200e9,          # Young's modulus (Pa)
        'fy': 235e6,         # Yield strength (Pa)
        'fu': 360e6,         # Ultimate strength (Pa)
        'density': 7850,     # Density (kg/m³)
        'nu': 0.3,           # Poisson's ratio
        'alpha': 12e-6,      # Thermal expansion (1/°C)
    },
    'steel_S355': {
        'E': 200e9,
        'fy': 355e6,
        'fu': 490e6,
        'density': 7850,
        'nu': 0.3,
        'alpha': 12e-6,
    },
    'steel_S460': {
        'E': 200e9,
        'fy': 460e6,
        'fu': 540e6,
        'density': 7850,
        'nu': 0.3,
        'alpha': 12e-6,
    },
    'concrete_C30': {
        'E': 33e9,           # Young's modulus (Pa)
        'fc': 30e6,          # Compressive strength (Pa)
        'density': 2400,     # Density (kg/m³)
        'nu': 0.2,           # Poisson's ratio
    },
    'cable_steel': {
        'E': 195e9,
        'fy': 1570e6,        # Breaking strength
        'density': 7850,
        'nu': 0.3,
    },
}

# Safety thresholds per LOAD-SPAN v1.0.0
SAFETY_THRESHOLDS = {
    'lsii_steady': 0.90,
    'lsii_monitoring': 0.75,
    'lsii_mitigation': 0.65,
    'lsii_critical': 0.65,
    
    'beta_target': 3.8,
    'beta_high': 4.7,
    'beta_minimum': 1.5,
    
    'lambda_cr_target': 2.0,
    'lambda_cr_minimum': 1.5,
    
    'd_fatigue_limit': 0.80,
    'd_fatigue_critical': 1.00,
    
    'r_struct_target': 0.70,
    'r_struct_minimum': 0.50,
    
    'dcr_limit': 2.0,
    'dcr_failure': 1.0,
}

# Physical constants
PHYSICAL_CONSTANTS = {
    'g': 9.81,               # Gravitational acceleration (m/s²)
    'pi': 3.141592653589793,
    'epsilon_0': 8.854e-12,  # Permittivity of free space
}

# Eurocode design values
EUROCODE_VALUES = {
    'partial_factor_steel': 1.0,
    'partial_factor_concrete': 1.5,
    'partial_factor_load': 1.35,
    'importance_factor': 1.0,
}

# IIW fatigue constants
IIW_FATIGUE_CONSTANTS = {
    'm_constant_amplitude': 3,
    'm_variable_amplitude': 5,
    'caf_factor': 0.5,  # CAFL = FAT/2 for variable amplitude
}
