def get_drivers_laps_path(drivers_laps_range: dict) -> str:
    """Build path for drivers and laps comparison"""
    drivers_path = "compare"
    keys_list = list(drivers_laps_range.keys())
    for driver in keys_list:
        lap_range = drivers_laps_range[driver]
        drivers_path += f"/{driver}"
        for lap in lap_range:
            drivers_path += f"/{lap}"
        if keys_list.index(driver) < len(keys_list) - 1:
            drivers_path += "/vs"
    return drivers_path

def get_full_path(params: list) -> str:
    """Build full API path from parameters"""
    full_path = ""
    for param in params:
        if isinstance(param, dict): 
            param = get_drivers_laps_path(param)
        full_path += "/"+param if isinstance(param, str) else "/"+str(param)
    return full_path