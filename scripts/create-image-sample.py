import os
from os import path
import glob
import sys

import re
import numpy as np

from fontTools import ttLib
from fontTools.ttLib.tables import _c_m_a_p

from PIL import Image, ImageDraw, ImageFont, ImageOps


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

def openHTML(htmlFileName):
    htmlFile = open ( CURR_DIR + "/" + htmlFileName, 'w' )
    print( "<html>\n<body>\n\n<table>", file=htmlFile )
    return htmlFile

def closeHTML(htmlFile):
    print( "</table>\n\n</body>\n</html>", file=htmlFile )
    htmlFile.close()

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    bbox = font.getmask(text_string).getbbox()

    if bbox is not None:
        text_width  = bbox[2]
        text_height = bbox[3] + descent
    else:
        return ( 256, 64 )
    # text_width  = font.getmask(text_string).getbbox()[2]
    # text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)


def createTextImage(fontFile, text, htmlFile, imagePath):

        fonttoolsFont = ttLib.TTFont(fontFile)
        # fullName = fonttoolsFont['name'].getBestFullName()
        # familyName = fonttoolsFont['name'].getBestFamilyName()
        # fontName = fonttoolsFont['name'].getDebugName(4)
        fontName = fonttoolsFont['name'].getBestFullName()


        # font16 = ImageFont.truetype( fontFile, size=16 )
        # fontName, style = font16.getname()
        # print( fontName )
        # twidth, theight = get_text_dimensions( fontName, font16 )

        font36 = ImageFont.truetype( fontFile, size=36 )
        ewidth, eheight = get_text_dimensions( text, font36 )
        # ewidth, eheight = ImageDraw.Draw.multiline_textsize( text, font36 )
        # width = ewidth + 10
        # height = theight + eheight + 10
        
        rows = len( re.findall('\n', text) ) + 1
        width, height = ( ewidth + 10, eheight*rows + 10 )

        img = Image.new( 'RGB', (width, height), color='white' )
        draw = ImageDraw.Draw( img )

        # lx, ly = 5, theight
        # draw.text((5, 5),  fontName, font=font16, fill=(0, 0, 0))
        # draw.line((lx, ly, lx + twidth, ly), fill=(0, 0, 0))

        # draw.text((5, theight), text, font=font36, fill=(0, 0, 0))
        draw.text( (5, 5), text, font=font36, fill=(0, 0, 0) )

        imageFile = fontName.replace(" ", "_") + '.png' 

        savePath = CURR_DIR + imagePath + imageFile 
        img.save( savePath )

        """
        img = Image.open( savePath )
        img.load()
        padding = [ -5, -5, 5, 5 ]
        invert_img = ImageOps.invert(img)
        imageBox = invert_img.getbbox()
        if( imageBox is not None ):
            imageBox = tuple( np.asarray(imageBox) + padding )
            # imageBox = tuple( np.asarray(imageBox) )

            cropped = img.crop(imageBox)

            # after padding, a black line *may* appear on the left side for some images, so we draw a white box over it
            shape = [(0,0), (5, height)]
            draw = ImageDraw.Draw( cropped )
            draw.rectangle( shape, fill="white")

            cropped.save( savePath )
        else:
            print( "Skipping: ", fontName )

        linkPath = (imagePath+imageFile).replace( "/html/", "" )
        # print( '  <tr><td><u>' + fontName + '</u><br/><img src="' + linkPath + '"/></td></tr>', file=htmlFile )
        """


def main():
    # htmlFile = openHTML( "html/index.html" )
    # licenseType = "opensource"
    licenseType = "freetouse"
    # licenseType = "commercial"
    # licenseType = "shareware"
    fontDir = CURR_DIR + "/fonts/" + licenseType + "/*.ttf"
    fonts    = sorted( glob.glob(fontDir) )

    # Ge'ez Only
    # createTextImage( CURR_DIR + '/' + sys.argv[1], 'ሀለሐመሠረሰ\nቀበተኀነአከወዐ\nዘየደገጠጸፀፈፐ', None, "/" )
    createTextImage( CURR_DIR + '/' + sys.argv[1], 'ሀለሐመሠረሰ\nሸቀቐበቨተቸ\nኀነኘአከኸወዐ\nዘዠየደጀገጘ\nጠጨጰጸፀፈፐ', None, "/" )

    # closeHTML( htmlFile )


if __name__ == "__main__":
    main()
