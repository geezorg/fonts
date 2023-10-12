import os
from os import path
import pandas as pd

from fontTools import ttLib
from fontTools.ttLib.tables import _c_m_a_p

block_basic      = set(range(0x1200,0x137D))
block_extended   = set(range(0x2D80,0x2DDF))
block_extended_a = set(range(0xAB01,0xAB2F))
block_extended_b = set(range(0x1E7E0,0x1E7FF))
empty_basic = {
            0x1249, 0x124E, 0x124F,
    0x1257, 0x1259, 0x125E, 0x125F, 
            0x1289, 0x128E, 0x128F,
    0x12B1, 0x12B6, 0x12B7, 0x12BF,
    0x12C1, 0x12C6, 0x12C7,
                    0x12D7,
    0x1311, 0x1316, 0x1317,
    0x135B, 0x135C
}
empty_extended = {
    0x2D97, 0x2D98, 0x2D99, 0x2D9A, 0x2D9B, 0x2D9C, 0x2D9D, 0x2D9E, 0x2D9F,
    0x2DA7, 0x2DAF,
    0x2DB7, 0x2DBF,
    0x2DC7, 0x2DCF,
    0x2DD7, 0x2DDF
}
empty_extended_a = {
    0xAB00, 0xAB07, 0xAB08, 0xAB0F,
    0xAB10, 0xAB17, 0xAB18, 0xAB19, 0xAB1A, 0xAB1B, 0xAB1C, 0xAB1C, 0xAB1D, 0xAB1E, 0xAB1F,
            0xAB27,         0xAB2F
}
basic      = block_basic - empty_basic
supplement = set( range(0x1380,0x139A) )
extended   = block_extended   - empty_extended
extended_a = block_extended_a - empty_extended_a
extended_b = block_extended_b - { 0x1E7E7, 0x1E7EC, 0x1E7EF }
ethiopic   = basic | supplement | extended | extended_a | extended_b

meen  = { 0x1207, 0x1247, 0x1287, 0x12AF, 0x12CF, 0x12EF, 0x130F } | set( range( 0x2D80, 0x2D93 ) )
bench = set( range( 0x2DA0, 0x2DDF ) )
old_gurage = { 0x1381, 0x1382, 0x1385, 0x1386, 0x1389, 0x138A, 0x138D, 0x138E }
archaic = { 0x1227, 0x1358, 0x1359, 0x135A }

modern_geez = ethiopic - archaic - old_gurage - meen - bench - extended_a

size_ethiopic    = len(ethiopic)
size_modern_geez = len(modern_geez)


CURR_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

FontLicenses = [ 'OpenSource', "Free to Use", "Shareware", "Commercial" ]

def findMissing(font, uni_range, missing):
    cmap = font["cmap"].getBestCmap()
    for char in uni_range:
        if( char not in cmap ):
            missing.add( char )

def printTableHeader(htmlFile):
    print( '<tr>\n    <th rowspan="2">Font Name</th>', '<th colspan="8">Unicode</th>', '<th colspan="3">Modern Geʾez Sylalbary</th>', sep='', file=htmlFile)
    print( "<tr>\n    <th>Missing Basic</th>", "<th>Missing Supplement</th>", "<th>Missing Extended</th>", "<th>Missing Extended A</th>", "<th>Missing Extended B</th>", "<th>Total Missing</th>", "<th>Total</th>",  "<th>% Complete</th>", "<th>Missing MGS</th>", "<th>Total MGS</th>", "<th>% Complete</th>", sep='', file=htmlFile)

def openHTML(htmlFileName):
    htmlFile = open ( CURR_DIR + "/" + htmlFileName, 'w' )
    print( '<html>\n<head>\n  <title>Detailed Statistics of Font Coverage</title>\n  <link rel="stylesheet" href="simple.css">\n</head>\n<body>\n\n', file=htmlFile )

    print( '<h1>Detailed Statistics of Font Coverage</h1>', file=htmlFile )
    print( "<h2>Fonts by License Type</h2>\n<ul>", file=htmlFile )
    for license in FontLicenses: print( '<li><a href="#' + license.replace(' ', '') + '">' + license  + ' Fonts</a></li>', file=htmlFile )
    print( "</ul>", file=htmlFile )

    return htmlFile

def startTable(htmlFile):
    print( '<table class="stats">\n', file=htmlFile )

def endTable(htmlFile):
    print( '</table>\n', file=htmlFile )

def closeHTML(htmlFile):
    print( "\n\n</body>\n</html>", file=htmlFile )
    htmlFile.close()

def printRow( image_file, font_name, missing_basic, missing_supplement, missing_extended, missing_extended_a, missing_extended_b, total_missing, total, total_percent, total_missing_modern_geez, total_modern_geez, total_percent_modern_geez, htmlFile ):
    # image_file = image_path + font_file

    print( "  <tr>\n    <td>",
          font_name, '<br/><img src="', image_file, '"/>'
          "</td><td>",
          missing_basic,
          "</td><td>",
          missing_supplement,
          "</td><td>",
          missing_extended,
          "</td><td>",
          missing_extended_a,
          "</td><td>",
          missing_extended_b,
          "</td><td>",
          total_missing,
          "</td><td>",
          total,
          "</td><td>",
          str(total_percent).replace( ".0", "" ),
          "%</td><td>",
          total_missing_modern_geez,
          "</td><td>",
          total_modern_geez,
          "</td><td>",
          str(total_percent_modern_geez).replace( ".0", "" ),
          "%</td>\n  </tr>",
          sep="", file=htmlFile )

def main():
    # FontLicenses = [ 'OpenSource', "Free to Use", "Shareware", "Commercial" ]
    htmlFile = openHTML( "html/DetailedFontCoverage.html" )

    df_dict = pd.read_excel( CURR_DIR + "/FontData.xlsx", sheet_name=None )

    for sheet in df_dict:
        df = df_dict.get( sheet )
        print( '<h2 id="' + sheet.replace(' ', '') + '">', sheet, ' Fonts</h2>\n', file=htmlFile, sep='', flush=True )
        licenseType = sheet.replace( ' ', '' ).casefold()
        # image_path = CURR_DIR + "/images/" + licenseType + "/"
        image_path = "images" 
        startTable( htmlFile )
        printTableHeader( htmlFile )

        for row in df.index: 
            htmlFile.flush()

            font_file = df['File'][row]

            print( "Working on: ", font_file )
            font = ttLib.TTFont(CURR_DIR + font_file)
            font_name = df['Name'][row]

            missing_basic      = set()
            missing_supplement = set()
            missing_extended   = set()
            missing_extended_a = set()
            missing_extended_b = set()

            findMissing(font,basic,missing_basic)
            """
            print( "Missing: ", len(missing_basic) )
            if( len(missing_basic) != 0):
                for x in missing_basic:
                    print( hex(x) )
            """

            findMissing(font,supplement,missing_supplement)
            """
            print( "Missing: ", len(missing_supplement) )
            if( len(missing_supplement) != 0):
                for x in missing_supplement:
                    print( hex(x) )
            """

            findMissing(font,extended,missing_extended)
            """
            print( "Missing: ", len(missing_extended) )
            if( len(missing_extended) != 0):
                for x in missing_extended:
                    print( hex(x) )
            """

            findMissing(font,extended_a,missing_extended_a)
            """
            print( "Missing: ", len(missing_extended_a) )
            if( len(missing_extended_a) != 0):
                for x in missing_extended_a:
                    print( hex(x) )
            """

            findMissing(font,extended_b,missing_extended_b)
            """
            print( "Missing: ", len(missing_extended_b) )
            if( len(missing_extended_b) != 0):
                for x in missing_extended_b:
                    print( hex(x) )
            """

            missing = missing_basic | missing_supplement | missing_extended | missing_extended_a | missing_extended_b
            total_missing = len(missing)
            total = len(ethiopic) - total_missing
            missing_modern_geez = modern_geez.intersection( missing )
            total_missing_modern_geez = len(missing_modern_geez)
            total_modern_geez = len(modern_geez) - total_missing_modern_geez
            image_file = "images/fonts/" + licenseType + "/" + font_name.replace(" ", "_") + '.png'
            printRow( image_file, font_name, len(missing_basic), len(missing_supplement), len(missing_extended), len(missing_extended_a), len(missing_extended_b), total_missing, total, round((total/size_ethiopic)*100, 1), total_missing_modern_geez, total_modern_geez, round((total_modern_geez/size_modern_geez)*100,1), htmlFile )

        endTable( htmlFile )
        print( '<p><br/></p><hr/>', file=htmlFile )
    closeHTML( htmlFile )

if __name__ == "__main__":
    main()