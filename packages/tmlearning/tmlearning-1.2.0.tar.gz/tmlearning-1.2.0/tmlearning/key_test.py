import keyboard

# FUNCTIONS

def wasd_key_test():
    print("Press some WASD keys.")
    while True:
        if keyboard.is_pressed("w"):
            print("W pressed")
        if keyboard.is_pressed("a"):
            print("A pressed")
        if keyboard.is_pressed("s"):
            print("S pressed")
        if keyboard.is_pressed("d"):
            print("D pressed")

def arrow_key_test():
    print("Press some arrow keys.")
    while True:
        if keyboard.is_pressed("up"):
            print("up pressed")
        if keyboard.is_pressed("left"):
            print("left pressed")
        if keyboard.is_pressed("right"):
            print("right pressed")
        if keyboard.is_pressed("down"):
            print("down pressed")