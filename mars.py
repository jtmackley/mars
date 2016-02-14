import os
import pygame
import time
import random
import sys

class pymars :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        found = False
        self.topic=""
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        else:
            # Check which frame buffer drivers are available
            # Start with fbcon since directfb hangs with composite output
            drivers = ['fbcon', 'directfb', 'svgalib']
            for driver in drivers:
                # Make sure that SDL_VIDEODRIVER is set
                if not os.getenv('SDL_VIDEODRIVER'):
                    os.putenv('SDL_VIDEODRIVER', driver)
                try:
                    pygame.display.init()
                except pygame.error:
                    print 'Driver: {0} failed.'.format(driver)
                    continue
                found = True
                break
    
        if found:
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print "Framebuffer size: %d x %d" % (size[0], size[1])
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            pygame.display.init()
            size = (800, 480)
            self.screen  = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        
        pygame.mouse.set_visible(0)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
 
    def displaynextimage(self):
        self.timer=time.clock()
        self.index+=1
        if (self.index+1)>len(self.images):
            self.index=0

        print "Displaying:" + self.images[self.index]
        img=pygame.image.load(self.images[self.index]) 
        self.screen.blit(img,(0,0))        
        pygame.display.update()

    def switchtopic(self,topic):
        # Load images in folder
        if topic<>self.topic:
            self.topic=topic
            self.images = []
            self.index=-1
            path=os.getenv("HOME") + "/mars/"
            for file in os.listdir(path + topic):
                if file.endswith(".jpg"):
                    self.images.append(path + topic + "/" + file)
            if len(self.images)>0:
                self.images.sort()
                self.displaynextimage()
            else:
                self.switchtopic("title")

    def engine(self):
        self.switchtopic("title")
        while True:
            topic=self.topic
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.displaynextimage()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.switchtopic("profile")
                    elif event.key == pygame.K_a:
                        self.switchtopic("moons")
                    elif event.key == pygame.K_s:
                        self.switchtopic("features")
                    elif event.key == pygame.K_d:
                        self.switchtopic("rovers")
                    elif event.key == pygame.K_f:
                        self.switchtopic("features")
                    elif event.key == pygame.K_g:
                        self.switchtopic("orbit")
                    elif event.key == pygame.K_q:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.displaynextimage()
            if time.clock()-self.timer>60:
                self.switchtopic("title")

 
# Create an instance of the PyScope class
mars = pymars()
mars.engine()
time.sleep(10)