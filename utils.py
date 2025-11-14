from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

gu = GalacticUnicorn()
gu.set_brightness(0.3)
graphics = PicoGraphics(DISPLAY)

## Helper function to check if file exists
## Not currently used
def file_exists_try_except(file_path):
    try:
        with open(file_path, 'r'):
            return True
    except OSError:
        return False