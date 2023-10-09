import pandas as pd
import numpy as np
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

OpenSourceLicenses = {
    'OpenFont License' : 'https://scripts.sil.org/OFL',
    'GNU GPL v2' : 'http://www.gnu.org/copyleft/gpl.html'
}


def printTableHeader(htmlFile):
    print( '  <tr>\n    <th rowspan="2">Font Name</th><th rowspan="2">Details</th><th colspan="2">Ethiopic Unicode<br/>Completeness</th><th colspan="2">Modern Geʾez<br/>Completeness</th>\n  </tr>', file=htmlFile )
    print( "  <tr>\n    <th># Missing</th><th>% Complete</th><th># Missing</th><th>% Complete</th>\n  </tr>", file=htmlFile)

def openHTML(htmlFileName):
    htmlFile = open ( CURR_DIR + "/" + htmlFileName, 'w' )
    print( '<html>\n<head>\n<link rel="stylesheet" href="simple.css">\n  </head>\n  <body>\n\n<table>', file=htmlFile )
    return htmlFile

def closeHTML(htmlFile):
    print( "</table>\n\n</body>\n</html>", file=htmlFile )
    htmlFile.close()

def printRow(imagePath,fontName, manufacturer, designer, license, downloadURL, note, htmlFile):
    imageFile = imagePath + fontName.replace(" ", "_") + '.png' 

    if( pd.isna(note) ):
        note = ""
    else:
        note = "<br/>\n<b>Note:</b> " + note

    if( pd.isna(downloadURL) ):
        downloadURL = ""
    else:
        downloadURL = "<br/><br/><b>Download: </b>" + '<a href="'+downloadURL+'">'+downloadURL+"</a>" + "</td><td>"

    if( license in OpenSourceLicenses ):
        license = '<a href="'+OpenSourceLicenses[license]+'">'+license+"</a>"

    print( "  <tr>\n    <td><b>",
          fontName, '</b><br/><img src="', imageFile, '"/>'
          "</td><td><b>Manufacturer:</b> ",
          manufacturer,".<br/><b>Designer:</b> ",designer,".<br/><b>License:</b> ",license,".<br/>\n",note,
          downloadURL,
          "</td>\n  </tr>",
          sep="", file=htmlFile )


def main():
    FontLicenses = [ 'OpenSource', "Free to Use", "Shareware", "Commercial" ]
    htmlFile = openHTML( "html/index.html" )
    printTableHeader( htmlFile )

    df_dict = pd.read_excel( CURR_DIR + "/FontData.xlsx", sheet_name=None )

    for sheet in df_dict:
        # df = pd.read_excel( "FontData.xlsx", sheet_name="OpenSource" )
        df = df_dict.get( sheet )
        for row in df.index:    
            printRow( "images/fonts/"+sheet.casefold().replace(" ", "")+"/", df['Name'][row], df['Manufacturer'][row], df['Designer'][row], df['License'][row], df['URL'][row], df['Note'][row], htmlFile )

    closeHTML(htmlFile)


if __name__ == "__main__":
    main()