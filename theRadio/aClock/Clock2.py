#!/usr/bin/python3
# A clock by Tim Howlett 1st May 2013, based on TrigClock by Al Sweigart
# Written in Python (www.python.org) Does not work with Python 2.7, does with 3.2 
# Requires the Pygame module (www.pygame.org) and the Pyaudio module (http://people.csail.mit.edu/hubert/pyaudio/)
# sudo apt-get install libzbar-dev libzbar0 python-all-dev portaudio19-dev
# sudo apt-get install python-pyaudio python3-pyaudio
# sudo python3 -m pip --no-cache-dir install --verbose --force-reinstall -I pyaudio
# sudo pip3 --no-cache-dir install --verbose --force-reinstall -I pyaudio
# 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Tools\MSVC\14.22.27905\bin\HostX86\x64\cl.exe' failed with exit status 2
# 'C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Tools\MSVC\14.22.27905\bin\Hostx86\x64\cl.exe'
# sudo pip3 install --index-url=https://people.csail.mit.edu/hubert/git/pyaudio.git
# git clone https://people.csail.mit.edu/hubert/git/pyaudio.git

import sys, pygame, time, math, os, pyaudio, wave, audioop
from pygame.locals import *

# Uncomment the line below if you get the error "pygame.error: No available video device"
os.environ['SDL_VIDEODRIVER']='windib'
# Uncomment the two lines below to set the position if you've set display = noframe
#position = 1024, 0
#os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])

# Set up some constants for the clock
HOURHANDCOLOR = (0, 0, 0)
MINUTEHANDCOLOR = (0, 0, 0)
SECONDHANDCOLOR = (255, 255, 255)
CLOCKFACECOLOR = (255, 64, 64) #(64, 192, 32)
BGCOLOR = (0, 0, 0)
WINDOWWIDTH = 1024 # width of the program's window, in pixels
WINDOWHEIGHT = 768 # height of the program's window, in pixels
WIN_CENTERX = 412 
WIN_CENTERY = 384
CLOCKSIZE = 330 # general size of the clock
# And for the VU meter
PeakL = 0
PeakR = 0
Phazerror = 0
Phazerror_Previous = 0
Silence = 0
Silence_Previous = 0
old_second = 0

# Stretch is the size of the 'circle' 
def getTickPosition(tick, stretch=1.0):
    tick = tick % 60
    x = (math.sin(2 * math.pi * (tick / 60.0)) * stretch) + WIN_CENTERX
    y = (-1 * math.cos(2 * math.pi * (tick / 60.0)) * stretch) + WIN_CENTERY
    return x, y

# Standard pygame setup code
pygame.init()
pygame.display.init()
pygame.mixer.quit() # stops unwanted audio output on some computers
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.NOFRAME)
#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE, 24)
CLOCKSURF = DISPLAYSURF.subsurface(0, 0, 820, 768)
VUSURF = DISPLAYSURF.subsurface(820, 40, 160, 600)
vurect = pygame.Rect(820, 40, 160, 600)
#pygame.mouse.set_visible(False)
pygame.display.set_caption('Clock with VU meter')
fontObj = pygame.font.Font('freesansbold.ttf', 72)
fontBig = pygame.font.Font('freesansbold.ttf', 40)
fontMed = pygame.font.Font('freesansbold.ttf', 30)
fontSmall = pygame.font.Font('freesansbold.ttf', 12)

pa = pyaudio.PyAudio()

info = pa.get_default_input_device_info()
RATE = int(info['defaultSampleRate'])
FORMAT = pa.get_format_from_width(2)

# Open audio stream 
stream = pa.open(format = FORMAT,
            channels = 2,
            rate = RATE,
            #input_device_index = 1,
            input = True,
            start = True,
            frames_per_buffer = 1024)

# Clock ... 
# Render the Surface objects that have the clock numbers written on them
clockNumSurfs = [fontObj.render('%s' % (i), True, (0, 0, 0), CLOCKFACECOLOR)
                 for i in [12] + list(range(1, 12))] # Put 12 at the front of the list since clocks start at 12, not 1.

while True: # Main application loop
    # Event handling loop for quit events
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Fill the screen to draw from a blank state and draw the clock face
    CLOCKSURF.fill(BGCOLOR)
    pygame.draw.circle(CLOCKSURF, CLOCKFACECOLOR, (WIN_CENTERX, WIN_CENTERY), (CLOCKSIZE + 15), 0)

    # Put the logo above the center
    logo = pygame.image.load('logo.png') #For Windows
    # logo = pygame.image.load('/home/pi/Desktop/logo.png') #For RasPi 
    logo = logo.convert_alpha()
    logo, logo.get_rect()
    CLOCKSURF.blit(logo, (WIN_CENTERX - 110, 130))

    # Draw the numbers of the clock
    for i in range(12):
        clockNumRect = clockNumSurfs[i].get_rect()
        clockNumRect.center = getTickPosition(i * 5, (CLOCKSIZE * 0.8))
        CLOCKSURF.blit(clockNumSurfs[i], clockNumRect)

    # Get the current time
    now = time.localtime()
    now_hour = now[3] % 12 # now[3] ranges from 0 to 23, so mod 12.
    now_hour24 = now[3] # used for writing the time.
    now_minute = now[4]
    now_second = now[5] # + (time.time() % 1) # add the fraction of a second we get from time.time() to make a smooth-moving seconds hand
    
    # Draw the 'background' ticks
    for i in range(now_second, 60):
        x = int((math.sin(2 * math.pi * (i / 60.0))) * CLOCKSIZE)
        y = int((-1 * math.cos(2 * math.pi * (i / 60.0))) * CLOCKSIZE)
        if i % 5 == 0:
            pygame.draw.circle(CLOCKSURF, (255, 255, 255), ((x+ WIN_CENTERX), (y+ WIN_CENTERY)), 10, 0)
        else:
            pygame.draw.aaline(CLOCKSURF, (255, 255, 255), ((((x * 0.98) + WIN_CENTERX)), ((y * 0.98) + WIN_CENTERY)), (((x * 1.02)+ WIN_CENTERX), ((y * 1.02) + WIN_CENTERY)), 1)

    # Draw the tick circles
    for i in range(now_second):
        x = int((math.sin(2 * math.pi * (i / 60.0))) * CLOCKSIZE)
        y = int((-1 * math.cos(2 * math.pi * (i / 60.0))) * CLOCKSIZE)
        if i % 5 == 0:
            pygame.draw.circle(CLOCKSURF, (255, 255, 255), ((x+ WIN_CENTERX), (y+ WIN_CENTERY)), 15, 0)
        else:
            pygame.draw.circle(CLOCKSURF, (128, 0, 0), ((x+ WIN_CENTERX), (y+ WIN_CENTERY)), 15, 0) #(128, 188, 128)

    # Draw the tick circle for the second hand
    x = int((math.sin(2 * math.pi * (now_second / 60.0))) * CLOCKSIZE)
    y = int((-1 * math.cos(2 * math.pi * (now_second / 60.0))) * CLOCKSIZE)
    pygame.draw.circle(CLOCKSURF, SECONDHANDCOLOR, ((x+ WIN_CENTERX), (y+ WIN_CENTERY)), 15, 0)

    # Write the time - adding 0 before values below 10
    # First get the width of the text with seconds as 00
    if now_second <= 9 and now_minute <= 9:
        text = fontObj.render(str(now_hour24) + ":0" + str(now_minute) + ":00", 1, (255, 255, 255))
    elif now_second <= 9 and now_minute >= 10:
        text = fontObj.render(str(now_hour24) + ":" + str(now_minute) + ":00", 1, (255, 255, 255))  
    elif now_second >= 10 and now_minute <= 9:
        text = fontObj.render(str(now_hour24) + ":0" + str(now_minute) + ":00", 1, (255, 255, 255))  
    else:
        text = fontObj.render(str(now_hour24) + ":" + str(now_minute) + ":00", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = CLOCKSURF.get_rect(). centerx 
    textpos.centery = CLOCKSURF.get_rect(). centery + 120
    # Then write the text proper
    if now_second <= 9 and now_minute <= 9:
        text = fontObj.render(str(now_hour24) + ":0" + str(now_minute) + ":0" + str(now_second), 1, (255, 255, 255))
    elif now_second <= 9 and now_minute >= 10:
        text = fontObj.render(str(now_hour24) + ":" + str(now_minute) + ":0" + str(now_second), 1, (255, 255, 255))  
    elif now_second >= 10 and now_minute <= 9:
        text = fontObj.render(str(now_hour24) + ":0" + str(now_minute) + ":" + str(now_second), 1, (255, 255, 255))  
    else:
        text = fontObj.render(str(now_hour24) + ":" + str(now_minute) + ":" + str(now_second), 1, (255, 255, 255))
    CLOCKSURF.blit(text, textpos)

    # Write the day of the week and the date
    text = fontBig.render(time.strftime("%a %d %b", time.localtime()), 1, (128, 128, 128))
    textpos = text.get_rect()
    DISPLAYSURF.blit(text, (690, 690))

    # Draw the hour hand
    x, y = getTickPosition(now_hour * 5 + (now_minute * 5 / 60.0), CLOCKSIZE * 0.5)
    for i in range (-10, 10):
        tick = now_hour * 5 + (now_minute * 5 / 60.0)
        v = (math.sin(2 * math.pi * ((tick - 15) / 60.0)) * i) 
        w = (-1 * math.cos(2 * math.pi * ((tick - 15) / 60.0)) * i)
        pygame.draw.aaline(CLOCKSURF, HOURHANDCOLOR, (WIN_CENTERX + v, WIN_CENTERY + w), (x + v, y + w), 0)
    
    # Draw the minute hand
    x, y = getTickPosition(now_minute + (now_second / 60.0), CLOCKSIZE * 0.7)
    for i in range (-6, 6):
        v = (math.sin(2 * math.pi * ((now_minute - 15)/ 60.0)) * i) 
        w = (-1 * math.cos(2 * math.pi * ((now_minute - 15)/ 60.0)) * i)
        pygame.draw.aaline(CLOCKSURF, HOURHANDCOLOR, (WIN_CENTERX + v, WIN_CENTERY + w), (x + v, y + w), 0)
    # And draw it's centre circle
    pygame.draw.circle(CLOCKSURF, MINUTEHANDCOLOR, (WIN_CENTERX, WIN_CENTERY), 20, 0)

    # Draw the second hand
    x, y = getTickPosition(now_second, CLOCKSIZE * 0.9)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX +1, WIN_CENTERY), (x, y), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX -1, WIN_CENTERY), (x, y), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX, WIN_CENTERY +1), (x, y), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX, WIN_CENTERY -1), (x, y), 1)
    # Draw the second hand's part that sticks out behind
    x, y = getTickPosition(now_second, CLOCKSIZE * -0.2) # negative stretch makes it go in the opposite direction
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX +1, WIN_CENTERY), (x +1, y), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX -1, WIN_CENTERY), (x -1, y), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX, WIN_CENTERY +1), (x, y +1), 1)
    pygame.draw.aaline(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX, WIN_CENTERY -1), (x, y -1), 1)
    # And draw it's centre circle
    pygame.draw.circle(CLOCKSURF, SECONDHANDCOLOR, (WIN_CENTERX, WIN_CENTERY), 12, 0)

    old_second = now_second
    
    # VU meter ...
    # Draw the VU meter until the second changes before redrawing the clock

    # Event handling loop for quit events
    while old_second == now_second:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
        VUSURF.fill(BGCOLOR)
        # Read the data and calcualte the left and right levels
        data = stream.read(1024)
        ldata = audioop.tomono(data, 2, 1, 0)
        rdata = audioop.tomono(data, 2, 0, 1)
        amplitudel = ((audioop.rms(ldata, 2))/32767)
        LevelL = int (41+(20*(math.log10(amplitudel+(1e-40)))))
        amplituder = ((audioop.rms(rdata, 2))/32767) 
        LevelR = int (41+(20*(math.log10(amplituder+(1e-40)))))

        # Use the levels to set the peaks
        if LevelL > PeakL:  PeakL = LevelL
        elif PeakL > 0 and LevelL < PeakL - 5: PeakL = PeakL - 0.2
        if LevelR > PeakR: PeakR = LevelR
        elif PeakR > 0 and LevelR < PeakR - 5: PeakR = PeakR - 0.2
        
        # Write the scale and draw in the lines
        for dB in range (0, 44, 4):
            number = str(dB)
            text = fontSmall.render("-"+number, 1, (255, 255, 255))
            textpos = text.get_rect()
            VUSURF.blit(text, (70, 100+(12*dB)))
            pygame.draw.line(VUSURF, (128, 128, 128), (20,104+(12*dB)), (59,104+(12*dB)), 1)
            pygame.draw.line(VUSURF, (128, 128, 128), (100,104+(12*dB)), (139,104+(12*dB)), 1)
        #pygame.draw.line(VUSURF, (255, 128, 0), (0,0), (159,0))
        pygame.draw.line(VUSURF, (128, 188, 128), (0,90), (0,599))
        pygame.draw.line(VUSURF, (128, 188, 128), (159,90), (159,599))
        pygame.draw.line(VUSURF, (128, 188, 128), (0,599), (159,599))
        pygame.draw.line(VUSURF, (128, 188, 128), (0,90), (159,90))
        
        # Draw the boxes
        for i in range (0, LevelL):
            if i < 20: 
                pygame.draw.rect(VUSURF, (0, 192, 0), (20, (575-i*12), 40, 10))
            elif i >= 20 and i < 30:
                pygame.draw.rect(VUSURF, (255, 255, 0), (20, (575-i*12), 40, 10))
            else:
                pygame.draw.rect(VUSURF, (255, 0, 0), (20, (575-i*12), 40, 10))
        for i in range (0, LevelR):
            if i < 20: 
                pygame.draw.rect(VUSURF, (0, 192, 0), (100, (575-i*12), 40, 10))
            elif i >= 20 and i < 30:
                pygame.draw.rect(VUSURF, (255, 255, 0), (100, (575-i*12), 40, 10))
            else:
                pygame.draw.rect(VUSURF, (255, 0, 0), (100, (575-i*12), 40, 10))
        # Draw the peak bars
        if PeakL > 0:
            pygame.draw.rect(VUSURF, (255, 255, 255), (20, (584-int(PeakL+1)*12), 40, 2))
        if PeakR > 0:
            pygame.draw.rect(VUSURF, (255, 255, 255), (100, (584-int(PeakR+1)*12), 40, 2))

        # Detect Overmod
        if LevelL >= 39 or LevelR >= 39:
            pygame.draw.rect(VUSURF, (255, 0, 0), (0, 0, 160, 88))
            text = fontMed.render("OVER", 1, (0, 0, 0))
            textpos = text.get_rect()
            VUSURF.blit(text, (35, 35))

        # Detect Silence
        if LevelL < 5 and LevelR < 5:
            Silence = Silence + 1
        if LevelL > 10 or LevelR > 10:
            Silence = 0
        if Silence > 200:
            pygame.draw.rect(VUSURF, (255, 255, 0), (0, 0, 160, 88))
            text = fontMed.render("SILENCE", 1, (0, 0, 0))
            textpos = text.get_rect()
            VUSURF.blit(text, (15, 30))
        
        # Detect phaze error
        mdata = audioop.tomono(data, 2, 1, 1)
        amplitudem = ((audioop.rms(mdata, 2))/32767)
        if amplitudem < (amplitudel/2) or amplitudem < (amplituder/2):
            Phazerror = Phazerror + 1
        if amplitudel > amplituder and amplitudem > amplitudel:
            Phazerror = 0
        if amplituder > amplitudel and amplitudem > amplituder:
            Phazerror = 0
        if Phazerror > 10:
            pygame.draw.rect(VUSURF, (0, 255, 255), (0, 0, 160, 88))
            text = fontMed.render("PHAZE", 1, (0, 0, 0))
            textpos = text.get_rect()
            VUSURF.blit(text, (25, 15))
            text = fontMed.render("ERROR", 1, (0, 0, 0))
            textpos = text.get_rect()
            VUSURF.blit(text, (25, 45))
            
        pygame.display.update(vurect)
        now = time.localtime()
        now_second = now[5]
        #pygame.time.wait(10)

    # Log the start of a silence in log.txt
    if Silence > 200 and Silence_Previous <= 200:
        file = open("log.txt", "a")
        file.write("Silence Started "+ str(now_hour24) + ":" + str(now_minute) + ":" + str(now_second)+" "+time.strftime("%a %d %b", time.localtime())+"\n")
        file.close()
    # Log the end of a silence in log.txt    
    if Silence < 200 and Silence_Previous > 200:
        file = open("log.txt", "a")
        file.write("Silence Ended "+ str(now_hour24) + ":" + str(now_minute) + ":" + str(now_second)+" "+time.strftime("%a %d %b", time.localtime())+"\n")
        file.close()
        
    Phazerror_Previous = Phazerror
    Silence_Previous = Silence
       
    pygame.display.flip()

