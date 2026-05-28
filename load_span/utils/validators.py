"""Input validation and safety bounds enforcement."""

from typing import Any, Dict, List, Optional, Tuple


def validate_input(
    value: Any,
    name: str,
    data_type: type,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    allowed_values: Optional[List] = None
) -> Tuple[bool, str]:
    """
    Validate input value against constraints.
    
    Returns:
        (is_valid, error_message)
    """
    # Check type
    if not isinstance(value, data_type):
        return False, f"Parameter '{name}' must be of type {data_type.__name__}"
    
    # Check numeric bounds
    if isinstance(value, (int, float)):
        if min_value is not None and value < min_value:
            return False, f"Parameter '{name}' = {value} < {min_value}"
        if max_value is not None and value > max_value:
            return False, f"Parameter '{name}' = {value} > {max_value}"
    
    # Check allowed values
    if allowed_values is not None and value not in allowed_values:
        return False, f"Parameter '{name}' = {value} not in {allowed_values}"
    
    return True, ""


def validate_lsii_inputs(
    beta: float,
    d_fatigue: float,
    r_struct: float,
    lambda_cr: float
) -> List[str]:
    """
    Validate inputs for LSII computation.
    
    Returns list of warning messages.
    """
    warnings = []
    
    if beta < 1.5:
        warnings.append(f"β = {beta:.2f} is critically low (< 1.5)")
    elif beta < 3.8:
        warnings.append(f"β = {beta:.2f} is below target (3.8)")
    
    if d_fatigue > 0.80:
        warnings.append(f"D_fatigue = {d_fatigue:.3f} exceeds limit (0.80)")
    if d_fatigue > 1.00:
        warnings.append(f"D_fatigue = {d_fatigue:.3f} exceeds failure criterion (1.00)")
    
    if lambda_cr < 1.5:
        warnings.append(f"λ_cr = {lambda_cr:.2f} is critically low (< 1.5)")
    elif lambda_cr < 2.0:
        warnings.append(f"λ_cr = {lambda_cr:.2f} is below target (2.0)")
    
    if r_struct < 0.50:
        warnings.append(f"R_struct = {r_struct:.2f} is critically low (< 0.5)")
    elif r_struct < 0.70:
        warnings.append(f"R_struct = {r_struct:.2f} is below target (0.7)")
    
    return warnings


def validate_sensor_config(config: Dict) -> List[str]:
    """Validate sensor configuration."""
    errors = []
    
    required_fields = ['sampling_rate', 'sensor_type', 'location']
    
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Validate sampling rate
    if 'sampling_rate' in config:
        rate = config['sampling_rate']
        if rate < 10:
            errors.append(f"Sampling rate {rate} Hz is too low (min 10 Hz)")
        if rate > 1000:
            errors.append(f"Sampling rate {rate} Hz is too high (max 1000 Hz)")
    
    return errors


def sanitize_input(data: Dict) -> Dict:
    """Remove None values and sanitize input dictionary."""
    sanitized = {}
    
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, dict):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, list):
            sanitized[key] = [v for v in value if v is not None]
        else:
            sanitized[key] = value
    
    return sanitized
