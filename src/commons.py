from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / 'data'
CONFIG_PATH = DATA_PATH / 'configs'
INPUT_PATH = DATA_PATH / 'input'
OUTPUT_PATH = DATA_PATH / 'output'
IMAGES_PATH = Path(__file__).parent.parent / 'images'


quantiles = (.1, .25, .5, .75, .9)
