# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 11:55:58 2020

@author: Wieke Harmsen (w.harmsen@student.ru.nl)
@first version: 3 April 2020
@second version: 6 April 2020

python 3.7
packages:
    praat-textgrids==1.0.2
    pandas==1.0.3
    
"""

import textgrids as tg
import os
import argparse
import pandas as pd

def read_CPA_matrix():
    matrix = pd.read_csv("CPAs_table.csv", sep = ";", header = 0)
    matrix = matrix.transpose()
    matrix2 = matrix.values.tolist()
    for list in matrix2:
        list.append("")
    return matrix2

def change_CPA_lexicon(cpa_matrix, lexicons,args):
    input_CPA = args.fromCPA
    output_CPA = args.toCPA
    input_lexicon = args.inputLexicon
    
    
    input_lex_name = input_lexicon.replace(".txt", "")
    output_lexicon = input_lex_name + "_" + output_CPA + ".txt"
    
    #Create output lexicon file
    out = open(output_lexicon,"w")
    
    #Read input lexicon file
    with open(input_lexicon, "r") as f:
        lines = f.readlines()
        
        for idx in range(len(lines)):
            # Get word string and phoneme string of every line
            entry = lines[idx].split("\t")
            word = entry[0]
            phon = entry[1].replace("\n", "")
            
            #Change phoneme string to phoneme array
            phon_array = phon.split(" ")
            
            #Find for every input phoneme the corresponding output phoneme
            new_phon =""
            for i in range(len(phon_array)):
                p = phon_array[i]
                from_array = cpa_matrix[lexicons.index(input_CPA)]
                to_array = cpa_matrix[lexicons.index(output_CPA)]
                new_p = to_array[from_array.index(p)]
                new_phon += new_p
                new_phon += " "
                
            #Write the output to the new txt file
            out.write(word +"\t" +new_phon[:-1] +"\n")
            
    print("Conversion of " + input_lexicon +" from " +input_CPA +" to "+output_CPA + " is done.")
    print("This is the output file:")
    print(os.path.realpath(output_lexicon))
    
def run(args):
    lexicons = ['name','ADAPT','SAMPA-1','SAMPA-2','SAMPA-3','CGN','CGN2']
    cpa_matrix = read_CPA_matrix()
    assert len(cpa_matrix) == len(lexicons)
    
    change_CPA_lexicon(cpa_matrix, lexicons, args)

def main():
    parser = argparse.ArgumentParser("Message")
    parser.add_argument("--inputLexicon", type=str, help = "This is a help message")
    parser.add_argument("--fromCPA", type=str, help = "Choose the CPA (Computer Phonetic Alphabet) of your input lexicon.")
    parser.add_argument("--toCPA", type=str, help = "Choose the CPA (Computer Phonetic Alphabet) in which you want to convert your input lexicon.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)   

if __name__ == "__main__": 
    main()