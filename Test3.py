
# Let's test Classes with PyGame

'''Actual Code Begins'''
# Import Modules #
from __future__ import division
import  pygame, random, ctypes, pickle, os, math, fractions, datetime
from    fractions       import *
from    pygame          import *
from    pygame.locals   import *
from    math            import *

from collections import OrderedDict

# Resolution Check - Get Max Res #
MAX_WIDTH   = ctypes.windll.user32.GetSystemMetrics(0) # Get System Res X #
MAX_HEIGHT  = ctypes.windll.user32.GetSystemMetrics(1) # Get System Res Y #

# Resolution Check - Get Aspect Ratio #
RES_GCD             = gcd(MAX_WIDTH , MAX_HEIGHT)
ASPECT_RATIO_W      = MAX_WIDTH      // RES_GCD
ASPECT_RATIO_H      = MAX_HEIGHT    //  RES_GCD


ASPECT_RATIO_VAL    = MAX_HEIGHT / MAX_WIDTH

print ("DEBUGSTRING - Resolution - " +str(MAX_WIDTH) +"x" +str(MAX_HEIGHT) +" | Res Val - " +str(ASPECT_RATIO_VAL))
print ("DEBUGSTRING - Technical Aspect Ratio - " +str(ASPECT_RATIO_W) +":" +str(ASPECT_RATIO_H))

# Resolution Check - Get height from a base of 320 Pix. #
TRUE_DEFAULT_WIDTH  = 480
TRUE_DEFAULT_HEIGHT = int(TRUE_DEFAULT_WIDTH * ASPECT_RATIO_VAL) # Don't ask, // wasn't enough.
print (ASPECT_RATIO_VAL)
print ("DEBUGSTRING - Final Res = " +str(TRUE_DEFAULT_WIDTH) +"x" +str(TRUE_DEFAULT_HEIGHT))

DEBUGTODOREMOVEME_viewmodel = pygame.image.load('DEBUGTODOREMOVEME_viewmodel.png')

# Resolution Check - Set Resolutions #
# Set Current + Default Width to Aspect Ratio * 20
SCREEN_WIDTH        = TRUE_DEFAULT_WIDTH
SCREEN_HEIGHT       = TRUE_DEFAULT_HEIGHT
DEFAULT_WIDTH       = SCREEN_WIDTH
DEFAULT_HEIGHT      = SCREEN_HEIGHT
SAVED_WIDTH         = SCREEN_WIDTH
SAVED_HEIGHT        = SCREEN_HEIGHT

# Set up display and dupe surface #
FLAGS_RESIZABLE     = RESIZABLE
FLAGS_FULLSCREEN    = HWSURFACE |   DOUBLEBUF   | FULLSCREEN
TRUE_DISPLAY        = pygame.display.set_mode( (DEFAULT_WIDTH, DEFAULT_HEIGHT), FLAGS_RESIZABLE)
SCREEN_DISPLAY      = pygame.Surface((DEFAULT_WIDTH, DEFAULT_HEIGHT), HWSURFACE)
TRUE_DISPLAY.set_alpha(None)

# Load PyGame & Sound System #
pygame.mixer.pre_init(44100, -16, 2, 1024)   # irrc, only default OGGs from Audacity work.
pygame.init()
pygame.mouse.set_visible(False)


#os.environ['SDL_VIDEO_CENTERED'] ='1'

pygame.display.set_caption("Hello")


FONT_SIZE       = 15
FONT_TRUE_SIZE  = 12
FONT_MAX_W      = DEFAULT_WIDTH     //FONT_TRUE_SIZE     # Max font elements wide
FONT_MAX_H      = DEFAULT_HEIGHT    //FONT_TRUE_SIZE     # Max font elements high
GAME_FONT       = pygame.font.SysFont("pixrpg01", FONT_SIZE, False)
DEBUG_FONT      = pygame.font.SysFont("emulogic", 8, False)
Debug_Height    = FONT_SIZE -4

# Horizon - Used for FOV Calc #
Horizon_XPos = DEFAULT_WIDTH//2
Horizon_YPos = DEFAULT_HEIGHT//2

FOV = min(DEFAULT_WIDTH, DEFAULT_HEIGHT)

# Used for mouse snapping #
SCREEN_HalfX = DEFAULT_WIDTH//2
SCREEN_HalfY = DEFAULT_HEIGHT//2
    
# Game Constants #
GAME_CLOCK                  = pygame.time.Clock()
GAME_FPS                    = 144
CONST_MILLISECONDS          = 1000//GAME_FPS     # Number of Milliseconds per Frame

# Debug Colro Consts #
COL_WHITE = (255, 255, 255)
COL_NOBUFFER = (255, 0, 255)

# Global Timer #
Global_Timer                = 0
Global_Timer_Max            = 2 ** 32
Global_Timer_TimeScale      = 1
Global_Timer_Paused         = False

Demo_Timer                  = 0
Demo_Timer_Max              = GAME_FPS * 3

PlayerControlEnabled    = True

Player_XPos = 0
Player_YPos = 0
Player_ZPos = 0
Player_Height = 64
Player_Stand_Height = 64
Player_Crouch_Height = 32

Player_BaseSpeed = 1

Moving                  = False
MovingLeft              = False
MovingRight             = False
MovingUp                = False
MovingDown              = False
Jumping                 = False
Crouching               = False
Gravity                 = 0
Player_JumpForce        = 2
TerminalVelocity        = 512

Player_Pitch    = 0
Player_Yaw      = 0
Player_Roll     = 0

tau = pi * 2
Rotate_270Deg   =   tau - (pi/2)
Rotate_180Deg   =   pi
Rotate_90Deg    =   pi/2
Rotate_45Deg    =   pi/4


FPS_MouseFocus = True
pygame.mouse.set_pos(SCREEN_HalfX, SCREEN_HalfY)
Mouse_RelX = 0
Mouse_RelY = 0

FullScreen = False

def rotate2D(pos,rad): x,y=pos; s,c = sin(rad), cos(rad); return x*c-y*s, y*c+x*s

def crash():
    print ("DEBUGSTRING - MANUAL CRASH")
    0/0


'''Init Textures'''
TEX_XHAIR = pygame.image.load('TEX/xhair.png').convert_alpha()

TEX_TESTTEX_TEXTURE = pygame.image.load('TEX/test.png').convert()

TEX_TESTTEX_VM = pygame.image.load('TEX/TestVM.png').convert_alpha()

print ("\n=== BEGIN GAME LOOP ===")

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                MovingLeft = True
            if event.key == K_d:
                MovingRight = True
            if event.key == K_w:
                MovingUp = True
            if event.key == K_s:
                MovingDown = True
            if event.key == K_SPACE:
                Jumping = True
            if event.key == K_LCTRL:
                Crouching = True
            if event.key        == K_RETURN:
                FPS_MouseFocus = not FPS_MouseFocus
                
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                MovingLeft = False
            if event.key == K_d:
                MovingRight = False
            if event.key == K_w:
                MovingUp = False
            if event.key == K_s:
                MovingDown = False
            if event.key == K_LCTRL:
                Crouching = False

        if event.type == VIDEORESIZE:
            if not FullScreen:
                SCREEN_WIDTH    = event.w
                SCREEN_HEIGHT   = event.h
                
                if SCREEN_WIDTH > MAX_WIDTH:
                    SCREEN_WIDTH = MAX_WIDTH
                
                if SCREEN_HEIGHT > MAX_HEIGHT:
                    SCREEN_HEIGHT = MAX_HEIGHT
                    
                
                SAVED_WIDTH     = SCREEN_WIDTH
                SAVED_HEIGHT    = SCREEN_HEIGHT
                
                TRUE_DISPLAY      = pygame.display.set_mode((SAVED_WIDTH, SCREEN_HEIGHT), FLAGS_RESIZABLE)
        if event.type == QUIT:
            pygame.quit()
            quit()


    CurrentFPS = GAME_CLOCK.get_fps()
    if CurrentFPS > GAME_FPS:
        CurrentFPS = GAME_FPS
    FPSRatio = 1 #GAME_FPS / (CurrentFPS + 1 )

    SCREEN_DISPLAY.fill(COL_NOBUFFER)
            

    # Mouse Move
    if FPS_MouseFocus:
        pygame.mouse.set_pos(SCREEN_HalfX, SCREEN_HalfY)
        Mouse_CurrentX, Mouse_CurrentY = pygame.mouse.get_pos()
        Mouse_RelX  = SCREEN_HalfX - Mouse_CurrentX
        Mouse_RelY  = SCREEN_HalfY - Mouse_CurrentY
        Player_Pitch -= Mouse_RelX/1024
        Player_Yaw -= Mouse_RelY/1024
                
    # Game stores Pitch/Yaw as Radians; therefore, Pi Pitch/Yaw = 180Deg
    if Player_Pitch > tau:
        Player_Pitch = 0
    elif Player_Pitch < 0:
        Player_Pitch = tau

    if Player_Yaw > Rotate_90Deg:
        Player_Yaw = Rotate_90Deg
    elif Player_Yaw < -Rotate_90Deg:
        Player_Yaw = -Rotate_90Deg

    
    Player_Speed = int (Player_BaseSpeed / (Player_Crouch_Height/Player_Height) * FPSRatio)
    Player_XMove = cos(Player_Pitch) * Player_Speed# Get Rotation of Player and Mult by this amount
    Player_ZMove = sin(Player_Pitch) * Player_Speed

    # If 0 - 90 Degrees
    # MovingLeft = -X, +Z

    if Player_Pitch > 0 and Player_Pitch < Rotate_90Deg:
        None
    elif Player_Pitch > Rotate_90Deg and Player_Pitch < pi:
        None
    elif Player_Pitch > pi and Player_Pitch < Rotate_270Deg:
        None
    elif Player_Pitch > Rotate_270Deg and Player_Pitch < tau:
        None

    # If 90 - 180
    # MovingLeft = +Z, +X

    # If 180 - 270
    # MovingLeft = +X, -Z

    # If 270 - 360
    # MovingLeft = -Z, -X
    if MovingLeft:
        Player_XPos -= Player_XMove
        Player_ZPos -= Player_ZMove
    if MovingRight:
        Player_XPos += Player_XMove
        Player_ZPos += Player_ZMove
    if MovingUp:
        Player_XPos += Player_ZMove
        Player_ZPos -= Player_XMove
    if MovingDown:
        Player_XPos -= Player_ZMove
        Player_ZPos += Player_XMove
        

    # Jump Code
    if Jumping:
        Gravity += 0.05
        Gravity *= 1.02
        Player_YPos += 5 - Gravity


    # TODO - Get current sector's floorpos instead of 0 #
    if Player_YPos <= 0:
        Gravity     = 0
        Player_YPos = 0
        Jumping     = False
        
    
    if Crouching:
        if not Jumping:
            Player_Height -= 4
            if Player_Height < Player_Crouch_Height:
                Player_Height = Player_Crouch_Height
            
    else:
        Player_Height += 4
        if Player_Height > Player_Stand_Height:
            Player_Height = Player_Stand_Height

        
            


    #faces = (XOrig, YOrig, ZOrig, Width, Height, Depth, Texture)
    points = []

    # sort by ZPos, then XPos, then YPos


    # Game stores faces as Quads as theyre easier to texture map but limit polygonal range which doesn't matter and is quite retro
    # Actually, we can use ANY shape
    quads = [
        
        [ [0,0,64], [64, 0, 64], [64, -64, 64] ],  # Quad 1,  # Quad 1
        [ [128,0, 128], [64, 0, 128], [64, -64, 128]   ],   # Quad 2
        
        ]
    
    renderedquads = []
    #verts = (0, 0, 0), (1024, 0, 0), (1024, 0, 1024), (0, 0, 1024), (1024, -1024, 0), (0, -1024, 0), (0, -1024, 1024), (1024, -1024, 1024)
    #verts = sorted(verts, key=lambda verts: verts[2])

    ''' Render Skybox '''
    # Skybox is always the first thing to be rendered as it has a ZBias of Infinity. #
    

    for quad in range(len(quads)):

        

        # For each Quad, add the value of the Quad's X/YPos on Screen


        # Quads = All Quads
        # Quads[x] = Four Vertices or One Quad
        # Quads[x][y] = Single Vertice
        # Quads[x][y][0/1/2] = Vertex XYZ - Pos

        for x in range (len(quads[quad])):


            # Ok this is a bit weird but it's about 3x faster to execute a division by 2048 than SQRT
            DistFromPlayer      = sqrt( (quads[quad][x][0] - Player_XPos) ** 2 + (quads[quad][x][1] - Player_YPos) ** 2 + (quads[quad][x][2] - Player_ZPos) ** 2 )
            
            # Transform the Quad
            quads[quad][x][0]   -= Player_XPos
            quads[quad][x][1]   += Player_YPos + Player_Height
            quads[quad][x][2]   += Player_ZPos

            #quads[quad][x].append(DistFromPlayer)

            quads[quad][x][0],  quads[quad][x][2]   = rotate2D(   (quads[quad][x][0],   quads[quad][x][2]),  Player_Pitch)
            quads[quad][x][1],  quads[quad][x][2]   = rotate2D(   (quads[quad][x][1] ,   quads[quad][x][2]),  Player_Yaw)
            

            if quads[quad][x][2] <= 0:
                quads[quad][x][2] = 0.00390625

            
            f = FOV/quads[quad][x][2]
            


            pygame.draw.rect(SCREEN_DISPLAY, (255, 255, 255), (DEFAULT_WIDTH//2 - 4, DEFAULT_HEIGHT//2 - 4, 8, 8), 1)
            

            
            quads[quad][x][0] = int(quads[quad][x][0] * f)  + Horizon_XPos           
            quads[quad][x][1] = int(quads[quad][x][1] * f)  + Horizon_YPos
            

            if quads[quad][x][0] < -128:
                quads[quad][x][0] = -128
                
            elif quads[quad][x][0] > SCREEN_WIDTH + 128:
                quads[quad][x][0] = SCREEN_WIDTH + 128
                
            if quads[quad][x][1] < -128:
                quads[quad][x][1] = -128

            elif quads[quad][x][1] > SCREEN_HEIGHT + 128:
                quads[quad][x][1] = SCREEN_HEIGHT + 128


            SCREEN_DISPLAY.set_at( (int(quads[quad][x][0]), int(quads[quad][x][1]) ), (255, 255, 255) )

            

            
            
            quads[quad][x].append( DistFromPlayer )

           

            

            

    # Sort the Quads now they're transformed #
    # Are ALL sections of the Quad Behind Us? If they are, exclude their rendering, else Render as if they're on Screen.

    # Now, sort each Quad by their ZPos #
    
    for quad in range (len(quads)):

        # DO a While Loop - Scan through each Quad after transformation, then
        
                    
        PolyCount = len(quads[quad])
        PolysOnScreen   = 0
        Poly_Counter    = 0

        # Loop for each Polygon.
        while Poly_Counter != PolyCount:
            
            # If ANY Vert is On-Screen, render it and break this loop.
            # Repeat for each Poly

            '''TODO REMOVE LINE BELOW AND UNCOMMENT !!!!!!!!! '''
            #renderedquads +=  [quads[quad]]
            if quads[quad][Poly_Counter][2] > 0 and quads[quad][Poly_Counter][0] > 0 and quads[quad][Poly_Counter][0] < DEFAULT_WIDTH and quads[quad][Poly_Counter][1] > 0 and quads[quad][Poly_Counter][1] < DEFAULT_HEIGHT:
                renderedquads +=  [quads[quad]]
                break
            else:
                Poly_Counter += 1
            

    # For each RenderedQuad, sort by ZPos, then delete ZPos
    # Technically, these aren't rendered QUADS, but Rendered Polys.
    rendered_polydepth = []
    
    for quad in range (len(renderedquads)):
 
        column = 3

        # Bug! - I only want the sum of the THIRD Indexes, NOT all values. I'm trying to fix this.
        PolyZ = sum(poly[column] for poly in renderedquads[quad]) / len(renderedquads[quad])

        
        
        
        for poly in range(len(renderedquads[quad])):
            del renderedquads[quad][poly][2:]
            
        rendered_polydepth.append ( [PolyZ, quad] )


    
    rendered_polydepth = sorted(rendered_polydepth, key=lambda x: x[0])
    RenderedQuadLength = len(rendered_polydepth)

    for poly in range (len(rendered_polydepth)):
        if len(rendered_polydepth) > 0:
            del (rendered_polydepth[poly][0])


    print (rendered_polydepth)
    
    for zbuffer in rendered_polydepth:

        # Sort PER Polygon by their ZPos AFTER being sorted in proper order
        CurrentFace = zbuffer[0]
        
        for quad in range(RenderedQuadLength):
            pygame.draw.polygon(SCREEN_DISPLAY, ( (127 * CurrentFace) % 256 , (32 * CurrentFace) % 256, (32 * CurrentFace) % 256), renderedquads[CurrentFace], 0)
            

    
    ''' Draw HUD '''
    SCREEN_DISPLAY.blit(TEX_XHAIR, (SCREEN_HalfX - (TEX_XHAIR.get_width() // 2), SCREEN_HalfY - (TEX_XHAIR.get_height() // 2) ) )

    ''' Draw Viewmodel '''
    # Increase Bob by SineX or w/e, if it gets too far Right, Move Left
    SCREEN_DISPLAY.blit(TEX_TESTTEX_VM, (DEFAULT_WIDTH - (TEX_TESTTEX_VM.get_width()) , DEFAULT_HEIGHT - (TEX_TESTTEX_VM.get_height()) ) )
    
    ''' Debug Information '''     
    SCREEN_DISPLAY.blit(GAME_FONT.render("FPS? " +str(int(CurrentFPS))+"/"+str(GAME_FPS) +" GT? " +str(Global_Timer) +" FPS RAT? " +str(FPSRatio), 0, COL_WHITE, 0), (0, 0))
    SCREEN_DISPLAY.blit(GAME_FONT.render("X" +str(round(Player_XPos,4)) +" Y" +str(round(Player_YPos,4)) +" Z" +str(round(Player_ZPos, 4)), 0, COL_WHITE, 0), (0, Debug_Height))
    SCREEN_DISPLAY.blit(GAME_FONT.render("JMP? " +str(Jumping) +" GRV? " +str(round(Gravity, 4)) +" CRCH? " +str(Crouching) +" HGT? " +str(Player_Height) , 0, COL_WHITE, 0), (0, Debug_Height * 2))
    SCREEN_DISPLAY.blit(GAME_FONT.render("PCH? " +str(round(Player_Pitch,3)) +" YAW? " +str(round(Player_Yaw,3)) +" RLL? " +str(round(Player_Roll, 3)), 0, COL_WHITE, 0), (0, Debug_Height * 3))
    SCREEN_DISPLAY.blit(GAME_FONT.render("AX? " +str(round(degrees(Player_Pitch),3)) +" AY? " +str(round(degrees(Player_Yaw),3)) +" AZ? " +str(round(degrees(Player_Roll), 3)), 0, COL_WHITE, 0), (0, Debug_Height * 4))


    ''' Screen Renderer '''
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (SCREEN_WIDTH, SCREEN_HEIGHT))
    TRUE_DISPLAY.blit(SCREEN_DISPLAY, (0,0))
    SCREEN_DISPLAY      = pygame.transform.scale(SCREEN_DISPLAY, (DEFAULT_WIDTH, DEFAULT_HEIGHT))
    pygame.display.flip()
    
    GAME_CLOCK.tick(GAME_FPS)
    Global_Timer += 1
    
