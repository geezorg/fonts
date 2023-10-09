import os
from os import path
import glob

from fontTools import ttLib

CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def listFonts(fontDir):
    fontPath = CURR_DIR + fontDir + "*.[ot]tf"
    fonts    = sorted( glob.glob(fontPath) )

    for fontFile in fonts:
        font = ttLib.TTFont(fontFile)
        fontName = font['name'].getBestFullName()
        local = fontFile.replace( CURR_DIR, '' )
        print( local , fontName, sep="," )

def main():
    # fontDir = "/Users/dmekonnen/Downloads/140+ Amharic Fonts/*.ttf"
    # print( "OpenSource" )
    # listFonts( "/fonts/opensource/" )
    # print( "Free to Use" )
    # listFonts( "/fonts/freetouse/" )
    # print( "Shareware" )
    # listFonts( "/fonts/shareware/" )
    # print( "Commercial" )
    listFonts( "/fonts/commercial/" )

if __name__ == "__main__":
    main()
