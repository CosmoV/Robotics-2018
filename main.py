# import pyb
# import time
# import us016
# import tcs34725
# import vl53l0x
# from machine import Pin, I2C
#
# i2c = I2C(scl=Pin('Y9', Pin.OUT), sda=Pin('Y10', Pin.OUT), freq=400000)
# laser_sensor = vl53l0x.VL53L0X(i2c, 0x29)
# laser_sensor.start_continuous(0)
#
# rgb_sensor = tcs34725.TCS34725(i2c)
# us_sensor = us016.US016(pyb.Pin.board.X3, pyb.Pin.board.X4, 3, 3)
#
# rgb_sensor.active(True)
# rgb_sensor.gain(60)
#
# while True:
    # print(tcs34725.html_rgb(sensor.read(True)))
    # print(us_sensor.distance())
    # print(laser_sensor.read_range_continuous_mm())
    