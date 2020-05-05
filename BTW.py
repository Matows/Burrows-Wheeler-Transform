#!/bin/env python3
from collections import Counter
class Rotation:
    """
        Provide convenient operations on rotated iterables.
        `Rotation(s, i)` represent something like `s[i:]`
    """


    def __init__(self, string, index):
        """string : methode getitem et lt
            string : iterable object passed as reference, implementing standard operators (>,<, ==...)
            index : index of first value
        """

        self.string = string
        self.index = index


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
    """Renvoie la dernière colonne d'une matrice sous la forme List<List>"""
    return [rotation[-1] for rotation in rotation_table]


def BTW(iterable):
    """Effectue la transformé de Burrows-Wheeler sur un iterable avec la classe Rotation"""
    # On crée une liste des rotations
    rotation_table = list(map(lambda i: Rotation(iterable, i), range(len(iterable))))
    # On la trie
    rotation_table = sorted(rotation_table)
    index = None
    # On cherche l'indice de la chaine de départ
    for i, rotation in enumerate(rotation_table):
        if rotation.index == 0:
            index = i
            break
    return index, lastCol(rotation_table)


def invert_BTW(index, lastCol):
    """ Effectue l'inverse de la transformé de Burrows-Wheeler.

        Notation from official PDF :
        lastCol = L
        len(lastCol) = N
        index = I
        lastColSorted = F
        precedingChars = C, même taille que alphabet
        P = P, même taille que la colonne
    """
    # On cherche à construire T, est une liste qui à un numéro de ligne de la matrice M associe une ligne de la matrice M' (étant une matrice dont chaque ligne à été décalé de 1)

    lastColSorted = sorted(lastCol) # UNUSED

    P = [] # i -> Nombre d'instances du caracère lastCol[i] dans le préfix lastCol[:i] (L[0,...,i-1])
    freq = {}
    # a en position 7 dans L -> a=0 dans P
    # aabc -> 0 1 0 0
    for i, char in enumerate(lastCol):
        freqChar = freq.get(char, 0)
        P.append(freqChar)
        freq[char] = freqChar+1

    precedingChars = {}
    tmp = 0
    for c in sorted(freq.keys()):
        precedingChars[c] = tmp
        tmp += freq[c]

    del freq

    T = []
    for i, char in enumerate(lastCol):
        T.append(P[i] + precedingChars[char])

    del precedingChars, P

    word = []
    # Explication notation :
    # T^2 = T[T[I]
    # T^3 = T[T^2[I] = T[T[T[I]
    tmp = index
    for i in range(len(lastCol)):
        word.append(lastCol[tmp])
        tmp = T[tmp]

    word.reverse()
    word = "".join(word)

    return word


def RLE(word):
    """optionnel"""
    ...

def invert_RLE(word):
    """optionnel"""
    ...

def MTF(word):
    ...

def invert_MTF(word):
    ...

### HUFFMAN
def huffman_tree(text):
    """Renvoie l'arbre des lettres utilisé dans le texte, suivant l'encoding de Huffman"""

    def minimum(freq):
        """Renvoie la plus petite valeur de `freq` suivant sont indice (occurences) et la supprime de `freq`"""
        mini = min(freq, key = lambda i: i[0])
        freq.remove(mini)
        return mini

    freq = [(occurence, letter) for letter, occurence in Counter(text).items()]

    while len(freq) > 1:
        left_indice, left_element = minimum(freq)
        right_indice, right_element = minimum(freq)
        freq.append(  (left_indice + right_indice, (left_element, right_element) )  )

    #(('A', 'V'), ('O', ('B', 'R'))) pour BRAVO.
    return freq[0][1]


def huffman_dictionnary(tree, prefix='', dictionnary={}):
    """Renvoie un dictionnaire des correspondance lettre -> code"""
    # TODO: Corriger le bug qui renvoie le dictionnaire précédent
    # TEMP FIX : call huffman_dictionnary(tree, '', {})
    if isinstance(tree, tuple):
        one = huffman_dictionnary(tree[0], prefix + '0', dictionnary)
        two = huffman_dictionnary(tree[1], prefix + '1', dictionnary)
        dictionnary.update(one)
        dictionnary.update(two)
    else:
        dictionnary[tree] = prefix
    return dictionnary


def huffman_encode(text):
    ...

def huffman_decode(dictionnary, binary_text):
    ...
### END HUFFMAN

def invert_huffman(word):
    ...

if __name__ == "__main__":
    from sys import argv
    mot = argv[1]
    print(invert_BTW(*BTW(mot)))
