

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

COLORS = [MAGENTA, BLUE, GREEN, YELLOW, RED, BOLD, UNDERLINE, ON_BLUE, ON_RED,
          ON_MAGENTA, ON_YELLOW, BLACK]

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


def tablify(mat, invert=False, replace=(None, None), extended_ascii=True, fixedCols=[], gradient=[], _colorMax='') :
    """ Returns a (str) table containing the items of the matrix.

    In :
    --   mat : list(list(alpha))
    --  invert : boolean
            If True, lines become columns, columns become lines.
    -- replace : (str, str)
            Instead of printing replace[0] when encountered, print replpace[1].
    -- extended_ascii : boolean
            if True, uses extended ascii.
    -- fixedCol : list(int)
            Specifies sizes (width) for each column.
    -- gradient : list((number, str))
            example : gradient=[(20, BLUE), (40, RED), (80, YELLOW)]
            makes every number in the mat colored in BLUE if under 20, RED if under 40 etc.
    -- _colorMax : str
            TODO
            if not empty, colors the maximum value of each line with the provided color

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

    # sizes : list(int), list of width of each col
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
                # if _colorMax in COLORS and type(matCopy[i][j]) in [float, int] and matCopy[i][j] == max([e for e in matCopy[i] if e in [float, int]]):
                    # tab += cstring(str(matCopy[i][j]), _colorMax) + " " * ((sizes[j]) - len(str(matCopy[i][j])))

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

def printData(name, _extended_ascii=True, _colors=True):
    data = {
        '1_random' : (
                [
                    ['Nb joueurs\\Nb restaurants','2','10','20'], 
                    ['2', 74.5, 94.5, 97.5], 
                    ['10', 20, 63.6, 83.1], 
                    ['20', 10, 43.75, 63.95]], 
                [(50, [ BOLD]), (75, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée avec la stratégie Random (en %)"),
        '1_tetu' : (
                [
                    ['Nb joueurs\\Nb restaurants','2','10','20'], 
                    ['2', 100, 100, 100], 
                    ['10', 20, 70, 80], 
                    ['20', 10, 50, 70]], 
                [(50, [ BOLD]), (75, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée avec la stratégie Tetu (en %)"),
        '1_mere' : (
                [
                            ['Nb joueurs\\Nb restaurants','2','10','20'], 
                            ['2', 51, 51, 51], 
                            ['10', 10.2, 10.8, 11.2], 
                            ['20', 5.1, 5.8, 6.2]], 
                [(50, [ BOLD]), (75, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée avec la stratégie Retour à la normale (en %)"),
        '1_wrostocho' : (
                [
                            ['Nb joueurs\\Nb restaurants','2','10','20'], 
                            ['2', 74, 80, 81], 
                            ['10', 17.8, 46.4, 48], 
                            ['20', 10, 35.2, 35.9]], 
                [(50, [ BOLD]), (75, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée avec la stratégie Wrong Stochastic Choice (en %)"),
        '1_stocho' : (
                [
                            ['Nb joueurs\\Nb restaurants','2','10','20'], 
                            ['2', 71, 93, 97], 
                            ['10', 19.4, 67.4, 79.8], 
                            ['20', 10, 45.1, 66.2]], 
                [(50, [ BOLD]), (75, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée avec la stratégie Stochastic Choice (en %)"),
        'all_vs_alea' : (
                [
                            ['Nb restaurants','Random', 'Têtu', 'MeanRegression', 'W.Stochastic', 'Stochastic'], 
                            ['2',  5,  7,  12, 9,  12], 
                            ['10', 42, 35, 45, 43, 42], 
                            ['20', 63, 58, 62, 56, 62]], 
                [(20, [BOLD]), (50, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée en fonction du nombre de restaurants (en %)"),
        '5_mere_15_random' : (
                [
                            ['Nb restaurants','5 vs 15', '1 vs 19'], 
                            ['2',  10.4, 12], 
                            ['10', 16.4, 45], 
                            ['20', 19.6, 62]], 
                [(20, [BOLD]), (50, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée en fonction du nombre de restaurants (en %)\n\
comparaison du cas 5 contre 15 et 1 contre 19"),
        'all_vs_all' : (
                [
                            ['Nb restaurants','Random', 'Têtu', 'MeanRegression', 'W.Stochastic', 'Stochastic'], 
                            ['2',  11,   11, 11,    8,    9], 
                            ['10', 57.5, 34, 11.5, 46.5, 48], 
                            ['20', 69, 46.5, 16, 53.5, 69.5]], 
                [(20, [BOLD]), (50, [MAGENTA, BOLD]), (100, [RED, BOLD])],
                "Probabilité d'obtenir un point à une manche donnée en fonction du nombre de restaurants (en %)")
    }
    if name not in data.keys():
        raise ValueError("Unknown name provided")

    if _colors:
        _gradient = data[name][1]
    else:
        _gradient = []

    table = tablify(
                    data[name][0], 
                    extended_ascii=_extended_ascii, 
                    gradient=_gradient)
    print(data[name][2], "\n" + table)

def main():
    print("Example:")
    extended_ascii = True
    colors = True
    printData("1_random", _extended_ascii=extended_ascii, _colors=colors)

    # print_format_table()

if __name__ == "__main__":
    main()