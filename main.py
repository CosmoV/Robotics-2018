# import pyb
# import time
# import us016
# import tcs34725
# from machine import I2C, Pin
#
# i2c = I2C(scl=Pin('Y9', Pin.OUT), sda=Pin('Y10', Pin.OUT))
# rgb_sensor = tcs34725.TCS34725(i2c)
# us_sensor = us016.Ultrasonic(pyb.Pin.board.X3, pyb.Pin.board.X4, 3, 3)
#
# rgb_sensor.active(True)
# rgb_sensor.gain(60)
#
# while True:
#     print(tcs34725.html_rgb(sensor.read(True)))
#     print(us_sensor.distance())
#     pyb.delay(100)
