from djitellopy import Tello
import time

tello = Tello()

tello.connect()
print()
print()

print("Battery Life Pecentage: "+ str(tello.get_battery()))

print("Tello temp is " + str(tello.get_temperature()))

print()
print()























