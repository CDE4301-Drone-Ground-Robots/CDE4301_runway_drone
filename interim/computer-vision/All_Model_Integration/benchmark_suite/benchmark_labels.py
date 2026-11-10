"""Display names; raw run identifiers remain stable for provenance."""
DISPLAY_NAMES={'sequential2': 'Sequential 1 (runs both models)', 'sequential': 'Sequential 2 (skips crack on FOD detection)', 'parallel': 'Parallel'}
def display_name(config):
    return DISPLAY_NAMES.get(config,config)
