from PIL import Image

#constants
maxCols = 168
maxRows = 47

# greyscale chars from darkest to brighest, you can alter this string all you want
greyscale = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# is altered in init(), could be used to debug or use custom scaling
rectWidth = 3
rectHeight = 6

#prep image and output.txt
im = Image.open('source.jpg')
pix = im.load()
txt_file = open("output.txt", "w")

#takes range1 and maps the value to range2
#used to convert a value from [0,255] a usable index for the greyscale array (eg. [0, len(greyscale)])
#visit: https://rosettacode.org/wiki/Map_range for formula
def map(low1, high1, low2, high2, val):
    t = low2 + ((val - low1)*(high2 - low2))/(high1 - low1)
    return round(t)


#converts rgb value to greyscale value
def rgbToGrey(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b 

#creates average greyscale of rectangle with dimensions rectWidth and rectHeight (= 1 Char)
#using the coordinates of the top left corner of this particular rectangle
def getRectScale(x, y):
    global rectWidth, rectHeight, pix

    cursum = 0
    curcnt = 0

    for curX in range(rectWidth):
        for curY in range(rectHeight):

            #needed to prevent out of bounds errors, maybe refactor loop in loopImage()
            if ( x + curX ) in range(0, im.size[0]) and ( y + curY) in range(0, im.size[1]):

                #fecth rgb vals
                r = pix[curX + x, curY + y][0]
                g = pix[curX + x, curY + y][1]
                b = pix[curX + x, curY + y][2]

                #build sum, increment count
                cursum = cursum + rgbToGrey(r,g,b)
                curcnt = curcnt + 1
    
    return cursum / curcnt

#setup program:
# - load image
# - create pixmap
# - calc the size of oen rectangle -> based on the maximum visible
#       chars per row in a fullscreen windows editor
def init():
    global rectHeight, rectWidth

    rectWidth = round(im.size[0]/maxCols)
    rectHeight = round(im.size[1]/maxRows)

    loopImage()
    txt_file.close()

#divides image into rectangles and passes coords to getRectScale()
# + writes curresponding char into the txt file
def loopImage():
    global pix, rectWidth, rectHeight, greyscale

    # y first to simplify writing (-> one line break per y row)
    for y in range(0, im.size[1], rectHeight):
        for x in range(0, im.size[0], rectWidth):
            curgreyscale = getRectScale(x, y)

            #index of char for rectangle
            curInd = map(0, 255, 0, len(greyscale) - 1, curgreyscale)
            txt_file.write(greyscale[curInd])

        #line break after each row
        txt_file.write("\n")

init()
