from math import sqrt

def getPalavrasdoDicionario(lemmas):
    words = set()
    for lemma in lemmas:
        words.update(set(lemmas[lemma]))
    return words

def truncar(words, cutlength):
    stems = {}
    for word in words:
        stem = word[:cutlength]
        try:
            stems[stem].update([word])
        except KeyError:
            stems[stem] = set([word])
    return stems

def contaIntersecoes(l1, l2):

    x1, y1 = l1[0]
    x2, y2 = l1[1]
    x3, y3 = l2[0]
    x4, y4 = l2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0.0:  # lines are parallel
        if x1 == x2 == x3 == x4 == 0.0:
            return (0.0, y4)

    x = (
        (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denominator
    y = (
        (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denominator
    return (x, y)


def getDerivacao(coordinates):

    try:
        return coordinates[1] / coordinates[0]
    except ZeroDivisionError:
        return float("inf")


def calcula_cut(lemmawords, stems):
    umt, wmt = 0.0, 0.0
    for stem in stems:
        cut = set(lemmawords) & set(stems[stem])
        if cut:
            cutcount = len(cut)
            stemcount = len(stems[stem])
            # Unachieved merge total
            umt += cutcount * (len(lemmawords) - cutcount)
            # Wrongly merged total
            wmt += cutcount * (stemcount - cutcount)
    return (umt, wmt)


def calcula(lemmas, stems):

    n = sum(len(lemmas[word]) for word in lemmas)
    gdmt, gdnt, gumt, gwmt = (0.0, 0.0, 0.0, 0.0)

    for lemma in lemmas:
        lemmacount = len(lemmas[lemma])
        gdmt += lemmacount * (lemmacount - 1)
        gdnt += lemmacount * (n - lemmacount)

        umt, wmt = calcula_cut(lemmas[lemma], stems)

        gumt += umt
        gwmt += wmt

    return (gumt / 2, gdmt / 2, gwmt / 2, gdnt / 2)


def indices(gumt, gdmt, gwmt, gdnt):

    try:
        ui = gumt / gdmt
    except ZeroDivisionError:
        # If GDMT (max merge total) is 0, define UI as 0
        ui = 0.0
    try:
        oi = gwmt / gdnt
    except ZeroDivisionError:
        # IF GDNT (max non-merge total) is 0, define OI as 0
        oi = 0.0
    try:
        sw = oi / ui
    except ZeroDivisionError:
        if oi == 0.0:
            # OI and UI are 0, define SW as 'not a number'
            sw = float("nan")
        else:
            # UI is 0, define SW as infinity
            sw = float("inf")
    return (ui, oi, sw)


class Paice(object):

    def __init__(self, lemmas, stems):

        self.lemmas = lemmas
        self.stems = stems
        self.coords = []
        self.gumt, self.gdmt, self.gwmt, self.gdnt = (None, None, None, None)
        self.ui, self.oi, self.sw = (None, None, None)
        self.errt = None
        self.update()

    def __str__(self):
        text = ["Global Unachieved Merge Total (GUMT): %s\n" % self.gumt]
        text.append("Global Desired Merge Total (GDMT): %s\n" % self.gdmt)
        text.append("Global Wrongly-Merged Total (GWMT): %s\n" % self.gwmt)
        text.append("Global Desired Non-merge Total (GDNT): %s\n" % self.gdnt)
        text.append("Understemming Index (GUMT / GDMT): %s\n" % self.ui)
        text.append("Overstemming Index (GWMT / GDNT): %s\n" % self.oi)
        text.append("Stemming Weight (OI / UI): %s\n" % self.sw)
        text.append("Error-Rate Relative to Truncation (ERRT): %s\r\n" % self.errt)
        coordinates = " ".join(["(%s, %s)" % item for item in self.coords])
        text.append("Truncation line: %s" % coordinates)
        return "".join(text)

    def getIndicesTruncamento(self, words, cutlength):

        truncated = truncar(words, cutlength)
        gumt, gdmt, gwmt, gdnt = calcula(self.lemmas, truncated)
        ui, oi = indices(gumt, gdmt, gwmt, gdnt)[:2]
        return (ui, oi)

    def getCoordenadasTruncamento(self, cutlength=0):
        
        words = getPalavrasdoDicionario(self.lemmas)
        maxlength = max(len(word) for word in words)

        coords = []
        while cutlength <= maxlength:
            pair = self.getIndicesTruncamento(words, cutlength)
            if pair not in coords:
                coords.append(pair)
            if pair == (0.0, 0.0):
                return coords
            if len(coords) >= 2 and pair[0] > 0.0:
                derivative1 = getDerivacao(coords[-2])
                derivative2 = getDerivacao(coords[-1])

                if derivative1 >= self.sw >= derivative2:
                    return coords
            cutlength += 1
        return coords

    def _errt(self):
        self.coords = self.getCoordenadasTruncamento()
        if (0.0, 0.0) in self.coords:
            if (self.ui, self.oi) != (0.0, 0.0):
                return float("inf")
            else:
                return float("nan")
        if (self.ui, self.oi) == (0.0, 0.0):
            return 0.0
        intersection = contaIntersecoes(
            ((0, 0), (self.ui, self.oi)), self.coords[-2:]
        )
        op = sqrt(self.ui ** 2 + self.oi ** 2)
        ot = sqrt(intersection[0] ** 2 + intersection[1] ** 2)
        return op / ot

    def update(self):
        self.gumt, self.gdmt, self.gwmt, self.gdnt = calcula(self.lemmas, self.stems)
        self.ui, self.oi, self.sw = indices(self.gumt, self.gdmt, self.gwmt, self.gdnt)
        self.errt = self._errt()