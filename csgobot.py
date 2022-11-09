from discord.ext import commands

import cv2
import numpy as np
from mss import mss
import enum
from time import sleep

#IF YOU ARE DOWNLOADING THIS FROM GITHUB, CHANGE THIS TO YOUR BOT'S TOKEN!!!!
token = "token"

client = commands.Bot(command_prefix = "!")

tStarPixels =         [ [195, 128], [200, 125], [256, 128], [268, 144], [196, 131] ]
tBorderPixels =       [ [224, 72],  [192, 172], [182, 160], [280, 154], [212, 183] ]
tKnifePixels =        [ [250, 144], [235, 167], [252, 145], [227, 173], [255, 136] ]

ctDarkWingPixels =    [ [209, 96],  [244, 124], [249, 159], [240, 93],  [223, 91]  ]
ctWireCuttersPixels = [ [209, 124], [260, 152], [271, 104], [221, 132], [213, 133] ]
ctBorderPixels =      [ [224, 72],  [192, 172], [182, 160], [280, 154], [212, 183] ]

@client.event
async def on_ready():
    print("I'm online now!")

@client.command()
async def start(ctx):
    isShowingWinLogo = False
        
    twins = 0
    ctwins = 0
        
    await ctx.send("Starting Game!")

    bounding_box = {'top': 0, 'left': 1152, 'width': 256, 'height': 290}

    sct = mss()

    while True:
        sct_img = sct.grab(bounding_box)
        sct_numpy = np.array(sct_img)

        cv2.imshow('screen', sct_numpy)

        TeamHasWon = False
        victoriousTeam = team.NONE
        proceedT = True
        proceedCT = False

        #--------------------------t--------------------------
        for i in tStarPixels:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy, tStarPixels, colors.TSTAR, team.TERRORISTS)

        if proceedT:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy, tBorderPixels, colors.TBORDER, team.TERRORISTS)

        if proceedT:
            TeamHasWon, victoriousTeam, proceedT = CheckPixels(sct_numpy, tKnifePixels, colors.TKNIFE, team.TERRORISTS)


        #--------------------------ct--------------------------
        if victoriousTeam == team.NONE:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy, ctDarkWingPixels, colors.CTDARKWING, team.COUNTERTERRORISTS)

        if proceedCT:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy, ctWireCuttersPixels, colors.CTWIRECUTTERS, team.COUNTERTERRORISTS)

        if proceedCT:
            TeamHasWon, victoriousTeam, proceedCT = CheckPixels(sct_numpy, ctBorderPixels, colors.CTBORDER, team.COUNTERTERRORISTS)


        #print(CheckPixels(sct_numpy, ctDarkWingPixels, colors.CTBORDER, team.COUNTERTERRORISTS))

        if not TeamHasWon:
            isShowingWinLogo = False

        if TeamHasWon and not isShowingWinLogo:
            isShowingWinLogo = True

            if victoriousTeam == team.TERRORISTS:
                twins += 1
                await ctx.send("Terrorists Win! " + "Ts: " + str(twins) + "      CTs: " + str(ctwins))
            elif victoriousTeam == team.COUNTERTERRORISTS:
                ctwins += 1
                await ctx.send("Counter Terrorists Win! " + "Ts: " + str(twins) + "      CTs: " + str(ctwins))
            
            
            sleep(10)

        sleep(0.5)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

def CheckPixels(screen, pixels, color, currentteam):
    proceed = True
    teamhaswon = False
    victoriousteam = team.NONE
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

class team(enum.Enum):
    TERRORISTS = 0
    COUNTERTERRORISTS = 1
    NONE = 69

client.run(token)