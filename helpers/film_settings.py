import yaml

def read():
    with open('settings.yaml', 'r') as file:
        settings = yaml.safe_load(file)
    
    return settings.values()

def write(sat_val, con_val, pal_val):
    settings_dict = {
        'saturation': sat_val,
        'contrast': con_val,
        'palette': pal_val
    }

    with open('settings.yaml', 'w') as file:
        yaml.dump(settings_dict, file, default_flow_style=False, sort_keys=False)