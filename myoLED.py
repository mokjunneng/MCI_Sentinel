from luma.core.interface.serial import spi,noop
from luma.core.reader import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT

def myoLED(n, block_orientation, rotate):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    print("Created device")

    with canvas(virtual) as draw:
        text(draw, (0.0), '10', fill="white")

    time.sleep(100)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description= 'myoLED testing', 
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

    args = parser.parse_args()

    try:
        myoLED(args.cascaded, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        pass