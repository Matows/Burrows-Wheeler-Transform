#!/bin/env python3
# s par référence
class Rotation:
    """
        Provide convenient operations on rotated iterables.
        `Rotation(s, i)` represent something like `s[i:]`
    """
    def __init__(self, string, index):
        """string : methode getitem et lt
            string : iterable object
            index : index of first value
        """

        self.string = string
        self.index = index
        #self._vector = list(range(len(string)))

    def __str__(self):
        return str(self.string[self.index:] + self.string[:self.index])

    def __repr__(self):
        return 'Rot(' + str(self.string[self.index:] + self.string[:self.index]) + ')'

    def __getitem__(self, index):
        return self.string[(self.index + index)%len(self.string)]

    def __len__(self):
        return len(self.string) - self.index

    def __eq__(self, other):
        return self.string == other.string and self.index == other.index

    def __lt__(self, other):
        """ Lower Than `<` operator 
            usage : Rotation(s, index2) < Rotation (s, index2)
            other : Roration
        """ 
        for i in range(min(len(self), len(other))):
           if self[i] < other[i]:
               return True
           elif self[i] > other[i]:
               return False
        return len(self) < len(other)

    def __le__(self, other):
        """ Lower Than `<=` operator 
            usage : Rotation(s, index2) <= Rotation (s, index2)
            other : Roration
        """ 
        if self[0] <= other[0]:
           return True
        else:
           return False

    def __gt__(self, other):
        """ Lower Than `>` operator 
            usage : Rotation(s, index2) > Rotation (s, index2)
            other : Roration
        """
        for i in range(min(len(self), len(other))):
           if self[i] > other[i]:
               return True
           elif self[i] < other[i]:
               return False
        return False

    def __ge__(self, other):
        """ Lower Than `>=` operator 
            usage : Rotation(s, index2) >= Rotation (s, index2)
            other : Roration
        """ 
        if self[0] >= other[0]:
           return True
        else:
           return False

def lastCol(rotation_table):
    return [rotation[-1] for rotation in rotation_table]

def BTW(iterable):
    rotation_table = list(map(lambda i: Rotation(iterable, i), range(len(iterable))))
    rotation_table = sorted(rotation_table)
    index = None
    for i, rotation in enumerate(rotation_table):
        if rotation.index == 0:
            index = i
            break
    return index, lastCol(rotation_table)

def invert_BTW(index, lastCol):
    """ Notation from official PDF :
        lastCol = L
        len(lastCol) = N
        index = I
        lastColSorted = F
        precedingChars = C, même taille que alphabet
        P = P, même taille que la colonne
    """
    # (D1) sort last column
    # (D2) T est une liste (vecteur math) qui à un numéro de ligne de la matrice M associe une ligne de la matrice M'

    lastColSorted = sorted(lastCol)


    P = [] # i -> Nombre d'instances du caracère lastCol[i] dans le préfix lastCol[:i] (L[0,...,i-1])
    freq = {}
    # a en position 7 dans L -> a=0 dans P
    # aabc; 0 1 0 0
    for i, char in enumerate(lastCol):
        freqChar = freq.get(char, 0)
        P.append(freqChar)
        freq[char] = freqChar+1

    precedingChars = {}
    tmp = 0
    for c in sorted(freq.keys()):
        precedingChars[c] = tmp      # ou permuter les deux lignes, à vérifier
        tmp += freq[c]

    del freq

    T = []
    for i, char in enumerate(lastCol):
        T.append(P[i] + precedingChars[char])

    del precedingChars, P

    word = []
    # T^2 = T[T[I]
    # T^3 = T[T^2[I] = T[T[T[I]
    tmp = index
    for i in range(len(lastCol)):
        try:
            word.append(lastCol[tmp])
            tmp = T[tmp]
        except IndexError:
            print(tmp, lastCol)
            break

    word.reverse()
    word = "".join(word)

    return word

if __name__ == "__main__":
    from sys import argv
    mot = argv[1]
    print(invert_BTW(*BTW(mot)))
