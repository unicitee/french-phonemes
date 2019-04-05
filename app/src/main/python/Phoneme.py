#!/usr/local/bin/python
# -*- coding: cp1252 -*-

# this language module is written to be part of
# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
#
# this module Copyright (C) 2016 Azia Giles Abuara
# Contact information at aziacomics-com.webs.com, aziagiles@gmail.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""functions to take a French word and return a list of phonemes
"""
# from breakdowns.unicode_hammer import latin1_to_ascii as hammer
from unicode_hammer import latin1_to_ascii as hammer


# Phoneme conversion dictionary: CMU on the left to Preston Blair on the right
phoneme_conversion = {
    'AA0': 'AI',  # odd     AA D
    'AA1': 'AI',
    'AA2': 'AI',
    'AE0': 'AI',  # at   AE T
    'AE1': 'AI',
    'AE2': 'AI',
    'AH0': 'AI',  # hut  HH AH T
    'AH1': 'AI',
    'AH2': 'AI',
    'AO0': 'O',  # ought AO T
    'AO1': 'O',
    'AO2': 'O',
    'AW0': 'O',  # cow   K AW
    'AW1': 'O',
    'AW2': 'O',
    'AY0': 'AI',  # hide HH AY D
    'AY1': 'AI',
    'AY2': 'AI',
    'B': 'MBP',  # be    B IY
    'CH': 'etc',  # cheese   CH IY Z
    'D': 'etc',  # dee   D IY
    'DH': 'etc',  # thee DH IY
    'EH0': 'E',  # Ed    EH D
    'EH1': 'E',
    'EH2': 'E',
    'ER0': 'E',  # hurt  HH ER T
    'ER1': 'E',
    'ER2': 'E',
    'EY0': 'E',  # ate   EY T
    'EY1': 'E',
    'EY2': 'E',
    'F': 'FV',  # fee    F IY
    'G': 'etc',  # green G R IY N
    'HH': 'etc',  # he   HH IY
    'IH0': 'AI',  # it   IH T
    'IH1': 'AI',
    'IH2': 'AI',
    'IY0': 'E',  # eat   IY T
    'IY1': 'E',
    'IY2': 'E',
    'JH': 'etc',  # gee  JH IY
    'K': 'etc',  # key   K IY
    'L': 'L',  # lee L IY
    'M': 'MBP',  # me    M IY
    'N': 'etc',  # knee  N IY
    'NG': 'etc',  # ping P IH NG
    'OW0': 'O',  # oat   OW T
    'OW1': 'O',
    'OW2': 'O',
    'OY0': 'WQ',  # toy  T OY
    'OY1': 'WQ',
    'OY2': 'WQ',
    'P': 'MBP',  # pee   P IY
    'R': 'etc',  # read  R IY D
    'S': 'etc',  # sea   S IY
    'SH': 'etc',  # she  SH IY
    'T': 'etc',  # tea   T IY
    'TH': 'etc',  # theta    TH EY T AH
    'UH0': 'U',  # hood  HH UH D
    'UH1': 'U',
    'UH2': 'U',
    'UW0': 'U',  # two   T UW
    'UW1': 'U',
    'UW2': 'U',
    'V': 'FV',  # vee    V IY
    'W': 'WQ',  # we W IY
    'Y': 'etc',  # yield Y IY L D
    'Z': 'etc',  # zee   Z IY
    'ZH': 'etc',  # seizure  S IY ZH ER
    # The following phonemes are not part of the CMU phoneme set, but are meant to fix bugs in the CMU dictionary
    'E21': 'E',  # E21 is used in ENGINEER
    '_':'rest'
}


# input_encoding = locale.getdefaultlocale()[1]  # standard system encoding??
# input_encoding = 'cp1252'
input_encoding = 'utf-8'
# input_encoding = 'utf-16'
# input_encoding = 'latin-1'
# input_encoding = 'iso-8859-1'


# lists containing different accented vowels
accented_a = ['\N{LATIN SMALL LETTER A WITH ACUTE}', '\N{LATIN SMALL LETTER A WITH GRAVE}',
              '\N{LATIN SMALL LETTER A WITH CIRCUMFLEX}', '\N{LATIN SMALL LETTER A WITH TILDE}',
              '\N{LATIN SMALL LETTER A WITH DIAERESIS}', '\N{LATIN SMALL LETTER A WITH RING ABOVE}',
              '\N{LATIN SMALL LETTER AE}']
accented_e = ['\N{LATIN SMALL LETTER E WITH CIRCUMFLEX}', '\N{LATIN SMALL LETTER E WITH DIAERESIS}',
              '\N{LATIN SMALL LETTER E WITH GRAVE}', '\N{LATIN SMALL LETTER E WITH ACUTE}',
              '\N{LATIN SMALL LIGATURE OE}']
accented_i = ['\N{LATIN SMALL LETTER I WITH ACUTE}', '\N{LATIN SMALL LETTER I WITH CIRCUMFLEX}',
              '\N{LATIN SMALL LETTER I WITH GRAVE}', '\N{LATIN SMALL LETTER I WITH DIAERESIS}']
accented_o = ['\N{LATIN SMALL LETTER O WITH CIRCUMFLEX}', '\N{LATIN SMALL LETTER O WITH DIAERESIS}',
              '\N{LATIN SMALL LETTER O WITH STROKE}', '\N{LATIN SMALL LETTER O WITH GRAVE}',
              '\N{LATIN SMALL LETTER O WITH ACUTE}', '\N{LATIN SMALL LETTER O WITH TILDE}']
accented_u = ['\N{LATIN SMALL LETTER U WITH ACUTE}', '\N{LATIN SMALL LETTER U WITH GRAVE}',
              '\N{LATIN SMALL LETTER U WITH CIRCUMFLEX}', '\N{LATIN SMALL LETTER U WITH DIAERESIS}']


def breakdownWord(word, recursive=False):
    word = word.lower()
    phonemes = []
    simple_convert = {
        'j': 'JH',
        'k': 'K',
        'q': 'K',
        'v': 'V',
        '\N{LATIN SMALL LETTER C WITH CEDILLA}': 'S'  # �
    }
    easy_consonants = list(simple_convert.keys())
    pos = 0
    previous = ' '
    for letter in word:
        if letter == len(word) > pos + 1 and word[pos + 1]:
            phonemes.append({letter})
        elif letter in ['b', 'd', 'g', 'p', 'x'] and pos + 1 == len(word):  # silent at end of words
            pass
        elif letter in ['a', accented_a]:
            if (len(word) > pos + 2 and word[pos + 1] in ['i', accented_i]) and word[pos + 2] != 'l':  # ai
                phonemes.append('EH0')
            elif len(word) > pos + 1 and word[pos + 1] in ['u', accented_u]:  # au
                phonemes.append('AO0')
            else:
                phonemes.append('AE0')
        elif letter in ['e', accented_e]:
            if pos + 1 == len(word) and len(word) == 2:  # takes care of words like 'je'
                phonemes.append('EH0')
            elif previous == 'u' and pos + 1 == len(word) and len(word) == 3 and word[pos - 2] == 'q':  # que
                phonemes.append('EH0')
            elif pos + 1 == len(word) and len(word) > 2:  # takes care of words like 'parle'
                pass
            elif previous == 'l' and word[pos + 1] == 's' and len(word) == 5 and word[pos - 2] == 'l':  # elles
                pass
            elif len(word) > pos + 2 and word[pos + 1] == 'a' and word[pos + 2] == 'u':
                pass
            elif previous in ['o', accented_o]:
                pass
            elif word[0] == letter and (
                    len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and word[pos + 2] in ['m',
                                                                                              'n']) and (
                    word != 'ennemmi'):
                phonemes.append('AE0')
            elif previous != 'i' and (len(word) == pos + 2 and word[pos + 1] in ['m', 'n']) or (
                    len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and word[pos + 2] in ['b', 'c', 'd',
                                                                                              'f',
                                                                                              'g', 'j', 'k',
                                                                                              'l',
                                                                                              'p', 'q', 'r',
                                                                                              's',
                                                                                              't', 'v', 'w',
                                                                                              'x',
                                                                                              'z']):
                phonemes.append('AE0')
            elif previous == 'f' and len(word) > pos + 3 and word[pos + 1] == 'm' and word[pos + 2] == 'm' and word[
                pos + 3] == 'e':
                phonemes.append('AE0')
            elif previous == 'u' and word[pos - 2] == 'q' and pos == len(word):
                pass
            else:
                phonemes.append('EH0')
        elif letter in ['i', accented_i]:
            if previous in ['e', accented_e] and ((len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and word[
                pos + 2] in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w',
                             'x', 'z']) or (len(word) == pos + 2)):
                pass
            elif previous in ['f', 't', 'v', 's'] and word[-1] == 'n' and len(word) > 1 and letter == word[-2]:
                phonemes.append('EH0')
            elif len(word) > pos + 2 and word[pos + 1] == 'm' and word[pos + 2] in ['b', 'p']:
                phonemes.append('EH0')
            elif len(word) > pos + 2 and word[pos + 1] == 'n' and word[pos + 2] in ['c', 'd', 'f', 'g', 'j', 'l', 'q',
                                                                                    's', 't', 'v']:
                phonemes.append('EH0')
                phonemes.append('NG')
            elif previous in ['a', accented_a] and len(word) > pos + 1 and word[pos + 1] != 'l':
                phonemes.append('EH0')
            elif previous in ['o', accented_o] and len(word) == pos + 2 and word[pos + 1] == 'n':
                phonemes.append('EH0')
            elif previous in ['o', accented_o] and len(word) > pos + 2 and word[pos + 1] == 'n' and word[pos + 2] in [
                'b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'z']:
                phonemes.append('EH0')
            elif previous in ['o', accented_o] and not (len(word) > pos + 2 and word[pos + 1] == 'n' and (
                    word[pos + 2] in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't',
                                      'v',
                                      'w', 'x', 'z'] or pos + 2 == len(word))):
                phonemes.append('AE0')
            else:
                phonemes.append('IH0')
        elif letter in ['o', accented_o]:
            if previous == 'm' and len(word) > pos + 6 and word[pos + 1] == 'n' and word[pos + 2] == 's' and word[
                pos + 3] == 'i' and word[pos + 4] == 'e' and word[pos + 5] == 'u' and word[pos + 6] == 'r':
                phonemes.append('EH0')  # monsieur
            elif len(word) > pos + 1 and word[pos + 1] == 'y':
                phonemes.append('W')
                phonemes.append('AE0')
            elif len(word) > pos + 2 and word[pos + 1] == 'i' and word[pos + 2] in ['m', 'n']:
                phonemes.append('W')
                phonemes.append('EH0')
            elif len(word) > pos + 2 and word[pos + 1] == 'u' and word[pos + 2] in ['i', accented_i]:  # stress vowel
                phonemes.append('W')
            elif len(word) > pos + 1 and word[pos + 1] in ['i', accented_i]:
                phonemes.append('W')
            elif len(word) > pos + 1 and word[pos + 1] in ['u', accented_u]:
                phonemes.append('UW0')
            elif len(word) > pos + 1 and word[pos + 1] in ['e', accented_e]:
                phonemes.append('EH0')
            else:
                phonemes.append('AO0')
        elif letter in ['u', accented_u]:
            if previous == 'l' and len(word) > pos + 3 and word[pos + 1] == 'n' and word[pos + 2] == 'd' and word[
                pos + 3] == 'i':
                phonemes.append('EH0')  # lundi
            elif previous == 'o' and len(word) > pos + 1 and word[pos + 1] in ['i', accented_i]:
                pass
            elif previous in ['b', 'c', 'd', 'f', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x',
                              'z'] and len(word) > pos + 1 and word[pos + 1] == 'i':
                phonemes.append('W')
            elif (len(word) == pos + 2 and word[pos + 1] in ['m', 'n']) or (
                    len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and word[pos + 2] in ['b', 'c', 'd',
                                                                                              'f',
                                                                                              'g', 'j', 'k',
                                                                                              'l',
                                                                                              'p', 'q', 'r',
                                                                                              's',
                                                                                              't', 'v', 'w',
                                                                                              'x',
                                                                                              'z']):
                phonemes.append('EH0')
            elif previous in ['a', accented_a]:
                phonemes.append('AO0')
            elif previous in ['g', 'q']:
                pass
            elif previous in ['o', accented_o]:
                phonemes.append('UW0')
            elif len(word) > pos + 1 and word[pos + 1] in ['a', accented_a]:
                phonemes.append('AE0')
            elif len(word) > pos + 1 and word[pos + 1] in ['e', accented_e]:
                phonemes.append('EH0')
            elif previous == 'g' and len(word) > pos + 1 and word[pos + 1] in ['e', accented_e]:
                phonemes.append('JH')
            else:
                phonemes.append('UW0')
        elif letter == 'y':
            if letter == word[0]:
                phonemes.append('Y')
            elif previous in ['a', 'e', 'i', 'o', 'u', accented_a, accented_e, accented_i, accented_o,
                              accented_u] and len(word) > pos + 1 and word[pos + 1] in ['a', 'e', 'i', 'o', 'u',
                                                                                        accented_a, accented_e,
                                                                                        accented_i, accented_o,
                                                                                        accented_u]:
                phonemes.append('Y')
            elif len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and len(word) == pos + 2:
                phonemes.append('EH0')
            elif len(word) > pos + 2 and word[pos + 1] in ['m', 'n'] and word[pos + 2] in ['b', 'c', 'd', 'f', 'g', 'j',
                                                                                           'k', 'l', 'p', 'q', 'r', 's',
                                                                                           't', 'v', 'w', 'x', 'z']:
                phonemes.append('EH0')
            else:
                phonemes.append('IH0')
        elif letter == 'b':
            if len(word) > pos + 1 and word[pos + 1] in ['s', 't']:
                phonemes.append('P')
            else:
                phonemes.append('B')
        elif letter == 'c':
            if len(word) > pos + 2 and word[pos + 1] == 'q' and word[pos + 2] == 'u':
                pass
            elif word[pos - 2] == 'p' and previous in ['e', accented_e] and len(word) == pos + 2 and word[
                pos + 1] == 't':  # takes care of words like 'respect'
                pass
            elif previous == 's' and len(word) > pos + 1 and word[pos + 1] in ['e', 'i', 'y', accented_e, accented_i]:
                pass
            elif len(word) > pos + 1 and word[pos + 1] == word[-1] and word[-1] in ['e', accented_e]:
                phonemes.append('Z')
            elif len(word) > pos + 1 and (
                    word[pos + 1] in ['a', 'o', 'u', 'l', accented_a, accented_o, accented_u] or word[
                pos + 1] in ['b',
                             'c',
                             'd',
                             'f',
                             'g',
                             'j',
                             'k',
                             'l',
                             'm',
                             'n',
                             'p',
                             'q',
                             'r',
                             's',
                             't',
                             'v',
                             'w',
                             'x',
                             'z']):
                phonemes.append('K')
            elif len(word) > pos + 1 and word[pos + 1] in ['e', 'i', 'y', accented_e, accented_i]:
                phonemes.append('S')
            elif previous == 'n' and len(word) == pos + 1:
                pass
            else:
                pass
        elif letter == 'd':
            if len(word) > pos + 1 and word[pos + 1] in ['-', '_']:
                phonemes.append('T')
            elif len(word) > pos + 1 and word[pos + 1] in ['s', 't']:
                pass
            else:
                phonemes.append('D')
        elif letter == 'f':
            if len(word) > pos + 1 and word[pos + 1] in ['-', '_']:
                phonemes.append('V')
            else:
                phonemes.append('F')
        elif letter == 'g':
            if previous == 'n':
                phonemes.append('NG')
            elif len(word) > pos + 1 and word[pos + 1] in ['e', 'i', 'y', accented_e, accented_i]:
                phonemes.append('JH')
            elif len(word) > pos + 1 and word[pos + 1] in ['s', 't']:
                pass
            else:
                phonemes.append('G')
        elif letter == 'h':
            if previous == 'c' and len(word) > pos + 1 and word[pos + 1] == 'r':
                phonemes.append('K')
            elif previous == 'c' and len(word) > pos + 1 and word[pos + 1] != 'r':
                phonemes.append('SH')
            else:
                pass
        elif letter == 'l':
            if word[pos - 2] in ['m', 'v', 'h', 'k'] and previous == 'i' and word[pos - 3] not in ['a',
                                                                                                   '']:  # mil*, vil*
                phonemes.append('L')
            elif word[pos - 3] in ['m', 'v'] and word[pos - 2] == 'i' and previous == 'l' and word[pos - 4] not in ['a',
                                                                                                                    '']:  # mill* ,vill*
                phonemes.append('L')
            elif word[pos - 3] == 'q' and word[pos - 2] == 'u' and previous == 'i':  # tranquil*
                phonemes.append('L')
            elif word[pos - 3] == 'u' and word[pos - 2] == 'i' and previous == 'l' and word[
                pos - 4] == 'q':  # tranquill*
                phonemes.append('L')
            elif ((previous == 'i' or (previous == 'i' and len(word) > pos + 1 and word[pos + 1] == letter) or (
                    previous == 'i' and len(word) > pos + 2 and word[pos + 1] == letter and word[
                pos + 2] == 'e'))):
                phonemes.append('Y')
            elif ((word[pos - 2] == 'i' and previous == letter) or (
                    word[pos - 2] == 'i' and previous == letter and len(word) > pos + 1 and word[
                pos + 1] == 'e')):  # il, ill,ille
                phonemes.append('Y')
            else:
                phonemes.append('L')
        elif letter == 'm':
            if previous == 'a' and len(word) > pos + 1 and word[pos + 1] == 'n':
                pass
            elif letter == word[-1] and word[-2] == 'i' and word[-3] == 'a':
                phonemes.append('NG')
            elif previous in ['a', 'e', 'i', 'o', 'u'] and (len(word) == pos + 1 or (
                    len(word) > pos + 1 and word[pos + 1] in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'p', 'q',
                                                              'r',
                                                              's', 't', 'v', 'w', 'x', 'z'])):
                phonemes.append('NG')
            else:
                phonemes.append('M')
        elif letter == 'n':
            if previous == 'o' and len(word) > pos + 5 and word[pos + 1] == 's' and word[pos + 2] == 'i' and word[
                pos + 3] == 'e' and word[pos + 4] == 'u' and word[pos + 5] == 'r':
                pass
            elif previous in ['a', 'e', 'i', 'o', 'u', accented_a, accented_e, accented_i, accented_o, accented_u] and (
                    len(word) == pos + 1 or (
                    len(word) > pos + 1 and word[pos + 1] in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l',
                                                              'n', 'p', 'q',
                                                              'r', 's', 't', 'v', 'w', 'x',
                                                              'z'])):  # n was forcefully added
                phonemes.append('NG')
            else:
                phonemes.append('N')
        elif letter == 'p':
            if len(word) > pos + 1 and word[pos + 1] in ['-', '_']:
                phonemes.append('P')
            elif previous == 'm' and len(word) > pos + 1 and word[pos + 1] == 't':  # mpt
                pass
            elif len(word) > pos + 1 and word[pos + 1] == 'h':  # ph
                phonemes.append('F')
            else:
                phonemes.append('P')
        elif letter == 'r':
            if word[pos - 2] == 'e' and previous == 'u':
                phonemes.append('R')
            elif pos + 1 == len(word):
                pass
            else:
                phonemes.append('R')
        elif letter == 's':
            if pos + 1 == len(word) and not ((word[pos - 3] == 'i' and word[pos - 2] == 'l' and previous == 'i') or (
                    word[pos - 3] in ['e', accented_e, 't'] and word[
                pos - 2] == 'l' and previous == 'a') or (
                                                     word[pos - 3] == 'f' and word[pos - 2] == 'i' and previous == 'l') or word == 'lis'):
                pass
            elif len(word) > pos + 2 and word[pos + 1] == 'c' and word[pos + 2] == 'h':
                pass
            elif previous in ['d', 't']:
                pass
            elif previous == 'e' and pos + 2 == len(word) and len(word) == 3 and word[pos + 1] == 't':  # est
                pass
            elif previous in ['a', 'e', 'i', 'o', 'u', accented_a, accented_e, accented_i, accented_o,
                              accented_u] and len(word) > pos + 1 and word[pos + 1] in ['a', 'e', 'i', 'o', 'u',
                                                                                        accented_a, accented_e,
                                                                                        accented_i, accented_o,
                                                                                        accented_u]:
                phonemes.append('Z')
            else:
                phonemes.append('S')
        elif letter == 't':
            if pos + 1 == len(word) and previous not in ['i', 'c', accented_i] and word != 'gadget' or word[
                pos - 2] in ['a', accented_a]:
                pass
            elif len(word) > pos + 1 and word[pos + 1] == 's':
                pass
            elif previous in ['d', 'g']:
                pass
            elif word[pos - 3] == 'p' and word[pos - 2] == 'e' and previous == 'c' and len(word) == pos + 1:
                pass
            elif len(word) > pos + 1 and word[pos + 1] in ['-', '_']:
                phonemes.append('T')
            elif len(word) > pos + 3 and word[pos + 1] == 'i' and word[pos + 2] == 'o' and word[pos + 3] == 'n' or len(
                    word) > pos + 5 and word[pos + 1] == 'i' and word[pos + 2] == 'e' and word[pos + 3] == 'n' and word[
                pos + 4] == 'c' and word[pos + 5] == 'e':
                phonemes.append('S')  # takes care of words ending with 'ience'
            else:
                phonemes.append('T')
        elif letter == 'w':
            if len(word) > pos + 4 and word[1:] == 'agon':
                phonemes.append('V')  # wagon
            else:
                phonemes.append('W')
        elif letter == 'x':
            if previous == 'u' and pos == len(word):
                pass
            elif len(word) > pos + 1 and word[pos + 1] in ['-', '_']:
                phonemes.append('Z')
            elif (len(word) > pos + 1 and word[pos + 1] in ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'q',
                                                            'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) or (
                    word[pos - 2] == 't' and previous != 'a'):
                phonemes.append('K')
                phonemes.append('S')
            elif len(word) > pos + 1 and word[pos + 1] in ['a', 'e', 'h', 'i', 'o', 'u', accented_a, accented_e,
                                                           accented_i, accented_o, accented_u] and (
                    word[pos - 2] != 't' and previous not in ['a', accented_a]):
                phonemes.append('Z')
            else:
                phonemes.append('K')
                phonemes.append('S')
        elif letter == 'y':
            if previous == 'a':  # ay
                phonemes.append('EH0')
            else:
                phonemes.append('IH0')
        elif letter == 'z':
            if word[-1] == letter and word[:-1] == 'berlio':
                phonemes.append('Z')
            elif word[-1] == letter and len(word) > 1:
                pass
            else:
                phonemes.append('Z')
        elif letter in easy_consonants:
            phonemes.append(simple_convert[letter])
        elif letter == ' ':
            phonemes.append("_")
        elif len(hammer(letter)) == 1:
            if not recursive:
                phon = breakdownWord(hammer(letter[0]), True)
                if phon:
                    phonemes.append(phon[0])
                    # ~ else:
                    # ~ print "not handled", letter, word
        pos += 1
        previous = letter
    # return " ".join(phonemes)
    # return phonemes
    temp_phonemes = []
    previous_phoneme = " "
    for phoneme in phonemes:
        if phoneme != previous_phoneme:
            temp_phonemes.append(phoneme)
        previous_phoneme = phoneme
    return temp_phonemes


def convertPhonemes(word):
    converted = []
    phonemesList = breakdownWord(word)
    for phoneme in phonemesList:
        converted.append(phoneme_conversion[phoneme])

    return converted
