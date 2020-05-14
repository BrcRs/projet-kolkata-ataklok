

MAGENTA = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ON_BLUE = '\33[44m'
ON_RED = '\33[41m'
ON_MAGENTA = '\33[45m'
ON_YELLOW = '\33[43m'
BLACK = '\33[30m'


def cstring(text, _clist):
    """ Returns text in color
    -- text : str
    -- clist : list(str), from bcolors
    """
    if type(_clist) is not list :
        clist = [_clist]
    else:
        clist = _clist
    output = ""

    output = output.join(clist + [text] + [ENDC])
    return (output)

def gradient_color(mat, steps_colors):
    """
    -- mat : list(list(number))
    -- steps_colors : list((number, str))
    """
    res = []
    for line in mat:
        newLine = []
        for item in line:
            for i in range(len(steps_colors)):
                if item < steps_colors[i][0]:
                    newLine.append(cstring(str(item), steps_colors[i][1]))
                    break
        res.append(newLine)
    return res

def gradientify(n, steps_colors):
    """
    -- n : number
    -- steps_colors : list((number, str))
    """
    for i in range(len(steps_colors)):
        if n <= steps_colors[i][0]:
            return cstring(str(n), steps_colors[i][1])


def tablify(mat, invert=False, replace=(None, None), extended_ascii=True, fixedCols=[], gradient=[]) :
    """ Returns a (str) table containing the (str) items of the matrix.

    In :
     --   mat : list(list(alpha))
     --  invert : boolean
            If True, lines become columns, columns become lines.
     -- replace : (str, str)
            Instead of printing replace[0] when encountered, print replpace[1].
    -- extended_ascii : boolean
            if True, uses extended ascii.
    -- fixedCol : list(int)
            ...
    -- gradient : list((number, str))
        example : gradient=[(20, BLUE), (40, RED), (80, YELLOW)]
            makes every number in the mat colored in BLUE if under 20, RED if under 40 etc.

    Out :
     -- : str
    """
    symbols = {}
    if extended_ascii :
        symbols = {
            "chl" : "┌",
            "chr" : "┐",
            "cll" : "└",
            "clr" : "┘",
            "vb" : "│",
            "hb" : "─"
        }
    else :
        symbols = {
            "chl" : "+",
            "chr" : "+",
            "cll" : "+",
            "clr" : "+",
            "vb" : "|",
            "hb" : "~"
        }

    # matyCopy : list(list(alpha))
    matCopy = mat.copy()

    """ Inverting """
    if invert :
        matCopy2 = [[] for j in range(len(matCopy[0]))]
        for i in range(len(matCopy)) :
            for j in range(len(matCopy[i])) :
                matCopy2[j].append(matCopy[i][j])
        matCopy = matCopy2
    """                       """

    # sizes : list(int), liste des tailles des colonnes
    sizes = [0] * len(matCopy[0])

    """ Updating optimal column sizes """
    if len(fixedCols) <= 0:
        for i in range(len(matCopy)) :
            for j in range(len(matCopy[i])) :
                # sizes[j]'s value is the length of the longest item of column j
                sizes[j] = max(sizes[j], len(str(matCopy[i][j])))
    else :
        for i in range(len(fixedCols)) :
            sizes[i] = fixedCols[i]
    """                                                """

    """ Inserting a line separator (for headings) """
    matCopy.insert(1, ["-" * (sizes[i]) for i in range(len(matCopy[0]))])

    # tab : str, result
    tab = symbols['chl']

    for j in range(len(matCopy[i])) :
        tab += symbols['hb'] * (sizes[j] + 2)

    tab += symbols['hb'] * (len(matCopy[0]) - 1) +\
            symbols['chr']+"\n"

    for i in range(len(matCopy)) :
        tab += symbols['vb']

        for j in range(len(matCopy[i])) :
            tab += " "

            if str(matCopy[i][j]) == replace[0] :
                tab += replace[1] + " " * ((sizes[j]) - len(str(matCopy[i][j])))

            else :
                if len(gradient) > 0 and type(matCopy[i][j]) in [float, int]:
                    tab += gradientify(matCopy[i][j], gradient) + " " * ((sizes[j]) - len(str(matCopy[i][j])))
                else:
                    tab += str(matCopy[i][j]) + " " * ((sizes[j]) - len(str(matCopy[i][j])))

            tab += " " + symbols['vb']
        tab += "\n"
    tab += symbols['cll']

    for j in range(len(matCopy[i])) :
        tab += symbols['hb'] * (sizes[j] + 2)

    tab += symbols['hb'] * (len(matCopy[0]) - 1) +\
    symbols['clr']
    return tab

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')



def main():  

    mat = [
        [5, 1, 2, 4, 7, 2],
        [5, 4, 8, 1, 6, 7],
        [4, 5, 4, 7, 1, 0],
        [1, 5, 9, 4, 6, 2]
    ]
    color_mat = gradient_color(mat, [(2, GREEN), (4, [ON_BLUE, BOLD]), (6, RED), (8, MAGENTA), (10, UNDERLINE)])
    # print(color_mat)

    print(tablify(color_mat))

    # print_format_table()

if __name__ == "__main__":
    main()