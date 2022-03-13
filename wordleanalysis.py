import pandas as pd
import numpy as np

class WordList:

    def __init__(self, WordList):
        self.imported_text_file = WordList
        self.list = self.getlist()
        self.table = self.gettable()

    def getlist(self):
        txt = open(self.imported_text_file, 'r').read()
        return eval(txt)

    def gettable(self):
        df = pd.DataFrame({"Word": self.list})
        n = 0
        for t in ['1st', '2nd', '3rd', '4th', '5th']:
            df[t] = df.Word.str[n]
            n += 1
        return df


class CountLetters:

    def __init__(self, CountLetters):
        self.CountLetters = CountLetters
        self.lst = ['1st', '2nd', '3rd', '4th', '5th']
        self.SumTables = self.summarizeletters()

    def summarizeletters(self):
        mydict = {}
        for t in self.lst:
            mydict[t] = self.CountLetters[t].value_counts()
        return mydict


viableWords = WordList('Wordle Guesses.txt').table
solutions = WordList('Wordle Word List.txt').table

solutions_numbers = CountLetters(solutions).SumTables
lst = ['1st', '2nd', '3rd', '4th', '5th']

with pd.ExcelWriter("results.xlsx") as Writer:
    solutions.to_excel(Writer, sheet_name="Solutions")
    viableWords.to_excel(Writer, sheet_name="Viable Words")

    for t in lst:
        solutions_numbers[t].to_excel(Writer, sheet_name=t)
