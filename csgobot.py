from discord.ext import commands

import cv2
import numpy as np
from mss import mss
import enum
from time import sleep

#IF YOU ARE DOWNLOADING THIS FROM GITHUB, CHANGE THIS TO YOUR BOT'S TOKEN!!!!
token = "token"

client = commands.Bot(command_prefix = "!")

tStarPixels = [ [195, 128], [200, 125], [256, 128] ]
tBorderPixels = [ [224, 72], [192, 172], [182, 160], [280, 154] ]
tKnifePixels = [ [250, 144], [235, 167] ]

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

        for i in tStarPixels:
            #print(str(list(sct_numpy[i[0], i[1]])) + " " + str(colors.TSTAR.value))
            if(list(sct_numpy[i[0], i[1]]) != colors.TSTAR.value):
                break
            TeamHasWon = True
        for i in tBorderPixels:
            if(list(sct_numpy[i[0], i[1]]) != colors.TBORDER.value):
                break
            TeamHasWon = True
        for i in tKnifePixels:
            if(list(sct_numpy[i[0], i[1]]) != colors.TKNIFE.value):
                break
            TeamHasWon = True

        if not TeamHasWon:
            isShowingWinLogo = False

        print(isShowingWinLogo, TeamHasWon)

        if TeamHasWon and not isShowingWinLogo:
            isShowingWinLogo = True
            twins+= 1

            await ctx.send("Terrorists Win! " + "Ts: " + str(twins) + "      CTs: " + str(ctwins))
            sleep(10)

        sleep(1)

        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

class colors(enum.Enum):
    TSTAR =   [ 61,  76,  86, 255 ]
    TBORDER = [ 49,  61,  69, 255 ]
    TKNIFE =  [ 30,  49,  63, 255 ]

client.run(token)
