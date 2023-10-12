import os
from os import path
import pandas as pd

import re
import numpy as np

from fontTools import ttLib
from fontTools.ttLib.tables import _c_m_a_p

from PIL import Image, ImageDraw, ImageFont, ImageOps


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

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


def createTextImage(fontFile, fontName, text, imagePath):

        try:
            font36 = ImageFont.truetype( fontFile, size=36 )
        except:
            print( "Cound not open: <", fontFile, '>', sep='' )
            return

        ewidth, eheight = get_text_dimensions( text, font36 )
        
        rows = len( re.findall('\n', text) ) + 1
        width, height = ( ewidth + 10, eheight*rows + 10 )

        img = Image.new( 'RGB', (width, height), color='white' )
        draw = ImageDraw.Draw( img )

        draw.text( (5, 5), text, font=font36, fill=(0, 0, 0) )

        imageFile = fontName.replace(" ", "_") + '.png' 

        savePath = CURR_DIR + imagePath + imageFile 
        img.save( savePath )

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


def main():
    FontLicenses = [ 'OpenSource', "Free to Use", "Shareware", "Commercial" ]

    df_dict = pd.read_excel( CURR_DIR + "/FontData.xlsx", sheet_name=None )

    for sheet in df_dict:
        df = df_dict.get( sheet )

        for row in df.index: 
            fontFile = df['File'][row]
            print( "File:", fontFile )
            licenseType = sheet.casefold().replace( ' ', '') 
            createTextImage( CURR_DIR + fontFile, df['Name'][row], 'ሀለሐመሠረሰ\nሸቀቐበቨተቸ\nኀነኘአከኸወዐ\nዘዠየደጀገጘ\nጠጨጰጸፀፈፐ', "/html/images/fonts/"+licenseType+"/" )

if __name__ == "__main__":
    main()
