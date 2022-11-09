from discord.ext import commands

import cv2
import numpy as np
from mss import mss
import enum
from time import sleep

#IF YOU ARE DOWNLOADING THIS FROM GITHUB, CHANGE THIS TO YOUR BOT'S TOKEN!!!!
token = "token"

client = commands.Bot(command_prefix = "!")

tStarPixels =          [ [195, 128], [200, 125], [256, 128], [268, 144], [196, 131] ]
tBorderPixels =        [ [224, 72],  [192, 172], [182, 160], [280, 154], [212, 183] ]
tKnifePixels =         [ [250, 144], [235, 167], [252, 145], [227, 173], [255, 136] ]

ctDarkWingPixels =     [ [209, 96],  [244, 124], [249, 159], [240, 93],  [223, 91]  ]
ctWireCuttersPixels =  [ [209, 124], [260, 152], [271, 104], [221, 132], [213, 133] ]
ctBorderPixels =       [ [224, 72],  [192, 172], [182, 160], [280, 154], [212, 183] ]

bombPlantedPixels =    [ [63, 74],   [36, 216],  [70, 4],    [69, 24],   [36, 165], [34, 50],  [64, 190], [72, 238], [63, 253], [40, 157] ]
notBombPlantedPixels = [ [34, 70],   [44, 105],  [34, 227],  [29, 90],   [51, 26],  [57, 112], [41, 241], [39, 119], [29, 193], [65, 154] ]

@client.event
async def on_ready():
    print("I'm online now!")

@client.command()
async def start(ctx):
    isShowingWinLogo = False
    isShowingBombPlantText = False
    #wow nice variable name
    bombPlantedAndIsCountingRightNow = False
        
    twins = 0
    ctwins = 0
        
    await ctx.send("Starting Game!")

    bounding_box_winlogo = {'top': 0, 'left': 1152, 'width': 256, 'height': 290}
    bounding_box_bomb = { 'top': 1050, 'left': 1152, 'width': 256, 'height': 75 }

    sct = mss()

    while True:
        #grab screenshots every (about) 0.2s
        sct_img_winlogo =   sct.grab(bounding_box_winlogo)
        sct_img_bombplant = sct.grab(bounding_box_bomb)
        sct_numpy_win =     np.array(sct_img_winlogo)
        sct_numpy_bomb =    np.array(sct_img_bombplant)

        cv2.imshow('screen',    sct_numpy_win)
        cv2.imshow('bombplant', sct_numpy_bomb)

        #resetting variables
        TeamHasWon = False
        victoriousTeam = team.NONE
        proceedT = True
        proceedCT = False
        bombPlanted =  False

        #this checks if specefic pixles on screen are specific colors, and if (for example) pixel [224, 72] is colored [ 49,  61,  69,  255 ], and all other pixels
        #that are checked are that color, assume that the terrorists have won
        #same thing happens for cts and for the bomb planted text

        #--------------------------t--------------------------
        for i in tStarPixels:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy_win, tStarPixels, colors.TSTAR, team.TERRORISTS)

        if proceedT:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy_win, tBorderPixels, colors.TBORDER, team.TERRORISTS)

        if proceedT:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy_win, tKnifePixels, colors.TKNIFE, team.TERRORISTS)


        #--------------------------ct--------------------------
        if victoriousTeam == team.NONE:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy_win, ctDarkWingPixels, colors.CTDARKWING, team.COUNTERTERRORISTS)

        if proceedCT:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy_win, ctWireCuttersPixels, colors.CTWIRECUTTERS, team.COUNTERTERRORISTS)

        if proceedCT:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy_win, ctBorderPixels, colors.CTBORDER, team.COUNTERTERRORISTS)

        #--------------------------bomb plant--------------------------
        if victoriousTeam == team.NONE:
            bombPlanted = CheckPixels(sct_numpy_bomb, bombPlantedPixels, colors.WHITETEXT, team.NONE)[2]
        if bombPlanted:
            bombPlanted = not CheckPixels(sct_numpy_bomb, notBombPlantedPixels, colors.WHITETEXT, team.NONE)[2]

        #check if the win screens or bomb planted text is showing
        if not TeamHasWon:
            isShowingWinLogo = False
        if not bombPlanted:
            isShowingBombPlantText = False
        
        #if this frame is the first frame that a win screen or bomb planted text is showing, message the discord server about it
        if TeamHasWon and not isShowingWinLogo:
            isShowingWinLogo = True

            if victoriousTeam == team.TERRORISTS:
                twins += 1
                await ctx.send("Terrorists Win! " + "Ts: " + str(twins) + "      CTs: " + str(ctwins))
            elif victoriousTeam == team.COUNTERTERRORISTS:
                ctwins += 1
                await ctx.send("Counter Terrorists Win! " + "Ts: " + str(twins) + "      CTs: " + str(ctwins))
            sleep(10)

        if bombPlanted and not isShowingBombPlantText:
            isShowingBombPlantText = True
            
            await ctx.send("The bomb has been planted!")
            sleep(2)

        sleep(0.5)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

def CheckPixels(screen, pixels, color, currentteam):
    proceed = True
    teamhaswon = False
    victoriousteam = team.NONE
    #if any pixel in the list is not the specified color, ignore the rest of the list and just say that win screens or bomb planted text are not being displayed
    for i in pixels:
        if list(screen[i[0], i[1]]) != color.value:
            teamhaswon = False
            victoriousteam = team.NONE
            proceed = False
            break
        victoriousteam = currentteam
        proceed = True
        teamhaswon = True
    return (teamhaswon, victoriousteam, proceed)

class colors(enum.Enum):
    TSTAR =         [ 61,  76,  86,  255 ]
    TBORDER =       [ 49,  61,  69,  255 ]
    TKNIFE =        [ 30,  49,  63,  255 ]

    CTDARKWING =    [ 49,  42,  30,  255 ]
    CTWIRECUTTERS = [ 164, 155, 141, 255 ]
    CTBORDER =      [ 147, 123, 94,  255 ]

    WHITETEXT =     [ 255, 255, 255, 255 ]

class team(enum.Enum):
    TERRORISTS = 0
    COUNTERTERRORISTS = 1
    NONE = 69

client.run(token)