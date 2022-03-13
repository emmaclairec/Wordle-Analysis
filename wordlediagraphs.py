import pandas as pd
import numpy as np

class WordList:

    def __init__(self, wordlist):
        self.txt = open(wordlist, 'r').read()
        self.list = self.getlist()
        self.table = self.gettable()
        self.blends = self.getcblends()
        [self.blenddict, self.worddict] = self.countblends()
        self.blendtable = pd.DataFrame(self.worddict).transpose()
        #self.blendtable = self.updateblendtable()


    def getlist(self):
        return eval(self.txt)

    def getcblends(self):
        charstoreplace = "aeiouy,"
        replacewith = " " * len(charstoreplace)
        removechars = '[]\"'
        table = self.txt.maketrans(charstoreplace, replacewith, removechars)
        blends = self.txt.translate(table).split()
        s = set()
        for i in blends:
            if len(i) > 1:
                s.add(i)
        return s

    def gettable(self):
        df = pd.DataFrame({"Word": self.list})
        n = 0
        for t in ['1st', '2nd', '3rd', '4th', '5th']:
            df[t] = df.Word.str[n]
            n += 1
        return df

    def countblends(self):
        blenddict = dict.fromkeys(self.blends, 0)
        worddict = dict.fromkeys(self.list, dict(blenddict))
        for word in worddict:
            for blend in blenddict:
                if blend in word:
                    worddict[word][blend] = True
                    blenddict[blend] += 1
                else:
                    worddict[word][blend] = False
        for blend in blenddict:
            blenddict[blend] = int(blenddict[blend])/len(self.list)
        return [blenddict, worddict]

    #def updateblendtable(self):
    #    for blend in self.blenddict:
    #        self.blendtable[blend].replace([True, False],[self.blenddict[blend], 0], inplace=True)
    #    return self.blendtable


class CountLetters:

    def __init__(self, countletters):
        self.CountLetters = countletters
        self.lst = ['1st', '2nd', '3rd', '4th', '5th']
        self.SumTables = self.summarizeletters()

    def summarizeletters(self):
        mydict = {}
        for t in self.lst:
            mydict[t] = self.CountLetters[t].value_counts()
        return mydict


#viableWords = WordList('Wordle Guesses.txt').table
wordle = WordList('Wordle Word List.txt')
solutions = wordle.table
df = pd.DataFrame(data={'Odds': wordle.blenddict})
table = wordle.blendtable


solutions_numbers = CountLetters(solutions).SumTables
#lst = ['1st', '2nd', '3rd', '4th', '5th']

with pd.ExcelWriter("results.xlsx") as Writer:
    df.to_excel(Writer, sheet_name="blends")
    wordle.blendtable.to_excel(Writer, sheet_name="blendtable")
    solutions_numbers.to_excel(Writer, sheet_name="overallodds")
    #viableWords.to_excel(Writer, sheet_name="Viable Words")

#    for t in lst:
#        solutions_numbers[t].to_excel(Writer, sheet_name=t)
