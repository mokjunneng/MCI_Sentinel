from PIL import Image
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT
import time

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)
# with canvas(device) as draw:
#     draw.rectangle([0,0, 7, 7], fill='white')
im1 = Image.new('1', (2,8), color=255)
im = Image.new('1', (8,8))
im.paste(im1, (0,0))
time.sleep(100)


