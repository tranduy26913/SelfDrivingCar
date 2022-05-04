from gpiozero import RGBLED
from time import sleep
RED = (1, 0 ,0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)
rgb_led = RGBLED(13, 19, 26, pwm = False)
while True:
rgb_led.color = RED
sleep(1)
rgb_led.color = GREEN
sleep(1)
rgb_led.color = BLUE