# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:16:56 2020

@author: Wieke Harmsen (w.harmsen@student.ru.nl)
first version: 3 April 2020
second version: 6 April 2020

python 3.7
packages:
    praat-textgrids==1.0.2
    pandas==1.0.3
    
"""
import glob
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
    
def create_new_phon_tier(file,file_name, cpa_matrix, lexicons,args):
    input_CPA = args.fromCPA
    output_CPA = args.toCPA
    phone_key_name = args.phoneme_tier
    
    assert phone_key_name in file.keys(), "Error: The argument you gave to --phoneme_tier does not exist in the textgrid file: " +file_name 
    
    new_phon_tier = file[phone_key_name]
    
    for idx in range(len(new_phon_tier)):
        p = new_phon_tier[idx].text
        
        from_array = cpa_matrix[lexicons.index(input_CPA)]
        to_array = cpa_matrix[lexicons.index(output_CPA)]
        new_p = to_array[from_array.index(p)]
        
        new_phon_tier[idx].text = new_p
    
    return new_phon_tier

def change_format_first_line(file_name):
    with open(file_name) as f:
            lines = f.readlines()
            first_line = lines[0]
            if(first_line.find("3 ") != -1):
                new_first_line = first_line.replace("3 ", "")
                lines[0] = new_first_line
                
                with open(file_name, "w") as f:
                    f.writelines(lines)
                    
def find_textgrids_in_dir(directory):
    output_extension_1 = '*.TextGrid'
    path1 = os.path.join(directory, output_extension_1)
    output_extension_2 = '*.tg'
    path2 = os.path.join(directory, output_extension_2)
    output_extension_3 = '*.Textgrid'
    path3 = os.path.join(directory, output_extension_3)
    files_list1 = glob.glob(path1)
    files_list2 = glob.glob(path2)
    files_list3 = glob.glob(path3)
    return files_list1 + files_list2 + files_list3
    
                    
def change_CPA_textgrids(cpa_matrix,lexicons,args):
    
    directory = args.directory
    input_CPA = args.fromCPA
    output_CPA = args.toCPA
    
    assert os.path.exists(directory), "Error: The directory passed to --directory does not exist."
    assert (input_CPA in lexicons), "Error: --fromCPA argument is written incorrectly. Use one of these CPAs as input: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2"
    assert output_CPA in lexicons, "Error: --toCPA argument is written incorrectly. Use one of these CPAs as output: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2"
    
    
    #Create list of all TextGrid files in the directory    
    files_list = find_textgrids_in_dir(directory)
    assert len(files_list) > 0,  "There are no TextGrid or .tg files found in this directory."
    print("There are ", len(files_list), " textgrid files found in this directory.")
    
    for file_name in files_list:
    
        #Some TextGrid files start with the line: 3 File type = "ooTextFile"
        #The "3" should be removed to use the textgrids package. 
        #Therefore use this function:
        change_format_first_line(file_name)
            
        #read TextGrid file
        file = tg.TextGrid(file_name)

        #Add new tier in desired CPA to TextGrid file
        file[output_CPA] =  create_new_phon_tier(file, file_name,cpa_matrix, lexicons, args)
        
        #Create new name of output file
        base_name = os.path.basename(file_name)
        new_name = base_name.replace(".TextGrid", "")
        new_name = new_name.replace(".tg", "")
        new_name = new_name.replace(".Textgrid", "")
        output_file_name = new_name + "_" + output_CPA +".TextGrid"

        #Create output folder if it not yet exists
        name_output_dir = 'Output_TextGrids'
        if not os.path.exists(name_output_dir):
            os.mkdir(name_output_dir)
        
        #Write output file to output folder
        path_to_output = r'./Output_TextGrids'
        output_file = os.path.join(path_to_output, output_file_name)
        file.write(output_file)
        
    print("Conversion of the phoneme tier(s) from " +input_CPA +" to " +output_CPA +" succeeded.")
    print("The output textgrid files with the new phoneme tier in " + output_CPA + " can be found in this directory: ")
    print(os.path.dirname(os.path.realpath(output_file)))
    

def run(args):
    lexicons = ['name','ADAPT','SAMPA1','SAMPA2','SAMPA3','CGN','CGN2']
    cpa_matrix = read_CPA_matrix()
    assert len(cpa_matrix) == len(lexicons)
    
    change_CPA_textgrids(cpa_matrix, lexicons,args)
   
def main():
    parser = argparse.ArgumentParser("Message")
    parser.add_argument("--directory", type=str, help = "The full path to the directory in which the TextGrid files (.TextGrid or .tg) are saved.")
    parser.add_argument("--phoneme_tier", type=str, help = "Type the name of the phoneme tier in the TextGrid.")
    parser.add_argument("--fromCPA", type=str, help = "Choose the CPA (Computer Phonetic Alphabet) of your input lexicon.")
    parser.add_argument("--toCPA", type=str, help = "Choose the CPA (Computer Phonetic Alphabet) in which you want to convert your input lexicon.")
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)  

if __name__ == "__main__": 
    main()
    

