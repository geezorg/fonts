import pandas as pd
import os


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

OpenSourceLicenses = {
    'OpenFont License' : 'https://scripts.sil.org/OFL',
    'GNU GPL v2' : 'https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html#SEC1'
}
Foundries = {
    'SIL International': 'https://sil.org/',
    'BlackFoundry': 'https://sil.org/',
    'Senamirmir Project': 'https://senamirmir.org/',
    # 'Concept Data Systems, PLC': 'http://www.conceptsdatasystems.com/'
    'Custcor Computing, PLC':  'https://www.custor.net/',
}


def printTableHeader(htmlFile):
    print( '  <tr>\n    <th rowspan="2">Font Name</th><th rowspan="2">Details</th><th colspan="2">Ethiopic Unicode<br/>Completeness</th><th colspan="2">Modern Geʾez<br/>Completeness</th>\n  </tr>', file=htmlFile )
    print( "  <tr>\n    <th># Missing</th><th>% Complete</th><th># Missing</th><th>% Complete</th>\n  </tr>", file=htmlFile)

def openHTML(htmlFileName):
    htmlFile = open ( CURR_DIR + "/" + htmlFileName, 'w' )
    print( '<html>\n<head>\n<link rel="stylesheet" href="simple.css">\n  </head>\n  <body>\n\n', file=htmlFile )
    return htmlFile

def startTable(htmlFile):
    print( '<table>\n', file=htmlFile )

def endTable(htmlFile):
    print( '</table>\n', file=htmlFile )

def closeHTML(htmlFile):
    print( "\n\n</body>\n</html>", file=htmlFile )
    htmlFile.close()

def printRow(imagePath,fontName, manufacturer, manufacturerURL, designer, license, downloadURL, note, missingUnicode, completeUnicode, missingMGS, completeMGS, htmlFile ):
    imageFile = imagePath + fontName.replace(" ", "_") + '.png' 

    if(not pd.isna(manufacturerURL) ):
        manufacturer = '<a href="' + manufacturerURL + '">' + manufacturer + '</a>'

    if( pd.isna(note) ):
        note = ""
    else:
        note = "<br/>\n<b>Note:</b> " + note

    if( pd.isna(downloadURL) ):
        downloadURL = ""
    else:
        downloadURL = "<br/><br/><b>Download: </b>" + '<a href="'+downloadURL+'">'+downloadURL+"</a>"

    if( license in OpenSourceLicenses ):
        license = '<a href="'+OpenSourceLicenses[license]+'">'+license+"</a>"

    print( "  <tr>\n    <td><b>",
          fontName, '</b><br/><img src="', imageFile, '"/>'
          "</td><td><b>Manufacturer:</b> ",
          manufacturer,".<br/><b>Designer:</b> ",designer,".<br/><b>License:</b> ",license,".<br/>\n",note,
          downloadURL,
          "</td><td>",
          missingUnicode,
          "</td><td>",
          str(completeUnicode).replace( ".0", "" ),
          "%</td><td>",
          missingMGS,
          "</td><td>",
          str(completeMGS).replace( ".0", "" ),
          "%</td>\n  </tr>",
          sep="", file=htmlFile )


def main():
    FontLicenses = [ 'OpenSource', "Free to Use", "Shareware", "Commercial" ]
    htmlFile = openHTML( "html/index.html" )

    print( "<h1>Fonts by License Type</h1>\n<ul>", file=htmlFile )
    for license in FontLicenses: print( '<li><a href="#' + license.replace(' ', '') + '">' + license  + ' Fonts</a></li>', file=htmlFile )
    print( "</ul>", file=htmlFile )

    df_dict = pd.read_excel( CURR_DIR + "/FontData.xlsx", sheet_name=None )
    stats = pd.read_excel( CURR_DIR + "/FontStats.xlsx", sheet_name="Font Stats" )

    for sheet in df_dict:
        df = df_dict.get( sheet )

        print( '<h2 id="' + sheet.replace(' ', '') + '">', sheet, ' Fonts</h2>\n', file=htmlFile, sep='', flush=True )
        htmlFile.flush()
        startTable( htmlFile )
        printTableHeader( htmlFile )

        for row in df.index:    
            print( "File:", df['File'][row] )
            statRow = stats.loc[ stats['File'] == df['File'][row] ]
            missingUnicode = statRow['Total Missing'].values[0]
            completeUnicode = statRow['% Unicode Complete'].values[0]
            missingMGS = statRow['Missing MGS'].values[0]
            completeMGS = statRow['% MGS Complete'].values[0]
            printRow( "images/fonts/"+sheet.casefold().replace(" ", "")+"/",
                     df['Name'][row],
                     df['Manufacturer'][row],
                     df['Manufacturer URL'][row],
                     df['Designer'][row],
                     df['License'][row],
                     df['URL'][row],
                     df['Note'][row],
                     missingUnicode, completeUnicode, missingMGS, completeMGS,
                     htmlFile )

        endTable( htmlFile )
        print( '<p><br/></p><hr/>', file=htmlFile )
    closeHTML( htmlFile )


if __name__ == "__main__":
    main()