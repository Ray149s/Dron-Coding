import pygame

## This is what opens up the console window
def init():
    pygame.init()
    win= pygame.display.set_mode((400, 400))

## function calling from a different script in keyName is a paramiter that will be filled in the other script it could be the up arrow, a, d, e whatever
def getKey(keyName):
    ## by default the value for getKey will be false if such as when the button is not selected, but will be true when a button is pressed
    ans = False
    ## for loop that checks even keys but not necisarly doing anything with tem
    for eve in pygame.event.get(): pass
    ## 
    keyInput = pygame.key.get_pressed()
    ## to check true or false we need a particular format which is the 'K_{}'.format(keyName)
    myKey = getattr(pygame, 'K_{}'.format(keyName))
    ##
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

#def main():
    


if __name__ == '__main__':
    init()
