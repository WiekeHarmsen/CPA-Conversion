# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 10:16:56 2020

@author: Wieke Harmsen (w.harmsen@student.ru.nl)
"""
import glob
import textgrids as tg
import os
import pandas as pd

# =============================================================================
#
# This script has two functions.
# 1. Conversion of the CPA (Computer Phonetic Alphabet) of a lexicon.
# 2. Conversion of the CPA (Computer Phonetic Alphabet) of a phoneme tier in a TextGrid.
#       The new phoneme tier is added to the original TextGrid
# 
# Before you run this script, specify the variables below.
# =============================================================================

#LEXICON CONVERSION
#Set this boolean to True if you want to convert a lexicon (Boolean):
lexicon_conversion = False
#The name of the lexicon you want to convert, put it in the same directory as this script (String)
#This lexicon should have the following format:
#  Word - TAB - Phonetic Transcription
input_lexicon = "lexicon_dutch_original.txt"

#TEXTGRID CONVERSION
#Set this boolean to TRUE if you want to convert a phoneme tier of one/multiple textgrid(s) to another CPA (Boolean):
textgrid_conversion = True
#The full path to the directory where the input TextGrid(s) are stored (e.g. r"C:\Users\Documents\data")
directory = r"C:\Users\wieke\Documents\Universiteit\Internship\JASMIN\JASMIN_output_FA"
#Name of the phoneme tier that you want to convert in these textgrids (String):
phoneme_tier = "kaldi_phone"

#ALWAYS SPECIFY:
#Set the CPA (Computer Phonetic Alphabet) of the input lexicon or input phoneme tiers (String).
input_CPA = "CGN2"
#Set the CPA (Computer Phonetic Alphabet) of the output lexicon or output phoneme tiers (String).
output_CPA = "CGN"
#Possible CPAs: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2


def create_CPA_matrix():
    #Based on the document "CPA_ADAPT_SAMPA_CGN_CGN2_IPA.pdf"
    names = ['p_in_pak','b_in_bak','t_in_tak','d_in_dak', 'k_in_kap','g_in_goal','f_in_fel','v_in_vel', 's_in_sein', 'z_in_zijn', 'sh_in_show','ge_in_bagage','g_in_goed','ch_in_toch', 'h_in_hand','m_in_met','n_in_net','ng_in_bang', 'l_in_land', 'r_in_rand', 'w_in_wit','j_in_ja','gn_in_campagne','ie_in_vier', 'ee_in_veer','aa_in_naam','oo_in_voor','oe_in_voer', 'uu_in_vuur', 'eu_in_deur', 'i_in_pit','e_in_pet','a_in_pad','o_in_pot', 'u_in_put','e_in_gemak','ij_in_fijn','ui_in_huis', 'ou_in_goud', 'e_in_creme', 'eu_in_freule','o_in_roze','in_in_bassin','en_in_genre', 'on_in_chanson','un_in_vingt-et-un','aai_in_draai','ooi_in_mooi', 'ieuw_in_nieuw', 'uw_in_duw', 'eeuw_in_sneeuw','oei_in_roeiboot','[SPN]','SIL','']
    ADAPT = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','J','i','e','a','o','u','y','2','I','E','A','O','Y','@','&','1','3','4','5','6','7','8','9','%','a[SPACE]j','o[SPACE]j','i[SPACE]w','y[SPACE]w','e[SPACE]w','u[SPACE]j','[SPN]','SIL','']
    SAMPA1 = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','n[SPACE]j','i','e','a','o','u','y','UNKNOWN','I','E','A','O','Y','@','Ei','9y','Au','E:','9','O:','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','a[SPACE]j','o[SPACE]j','i[SPACE]w','y[SPACE]w','e[SPACE]w','u[SPACE]j','[SPN]','SIL','']
    SAMPA2 = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','n[SPACE]j','i','e:','a:','o:','u','y','2:','I','E','A','O','Y','@','Ei','9y','Au','E:','9','O:','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','a:i','o:i','iu','yu','e:u','ui','[SPN]','SIL','']
    SAMPA3 = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','n[SPACE]j','i','e:','a:','o:','u','y','2:','I','E','A','O','Y','@','Ei','9y','Au','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN','a:[SPACE]j','o:[SPACE]j','i[SPACE]w','y[SPACE]w','e:[SPACE]w','u[SPACE]j','[SPN]','SIL','']
    CGN = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','J','i','e','a','o','u','y','2','I','E','A','O','Y','@','E+','Y+','A+','E:','Y:','O:','E~','A~','O~','Y~','a[SPACE]j','o[SPACE]j','i[SPACE]w','y[SPACE]w','e[SPACE]w','u[SPACE]j','[SPN]','SIL','']
    CGN2 = ['p','b','t','d','k','g','f','v','s','z','S','Z','G','x','h','m','n','N','l','r','w','j','J','i','e','a','o','u','y','EU','I','E','A','O','U','@','EI','UI','AU','E2','O[SPACE]j','O','E[SPACE]n','A[SPACE]n','O[SPACE]n','U[SPACE]n','a[SPACE]j','o[SPACE]j','i[SPACE]w','y[SPACE]w','e[SPACE]w','u[SPACE]j','[SPN]','SIL','']
      
    matrix = [names, ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2]
    assert len(names) == len(ADAPT) == len(SAMPA1) == len(SAMPA2) == len(SAMPA3) == len(CGN) == len(CGN2), "The lexicon arrays should have the same length."
   # df = pd.DataFrame(matrix)
    #df = df.transpose()
    #print(df.head())
    #df.to_csv("matrix.csv", index=False)    
    
    return matrix

def read_CPA_matrix():
    matrix = pd.read_csv("CPAs_table.csv", sep = ";", header = 0)
    matrix = matrix.transpose()
    matrix2 = matrix.values.tolist()
    for list in matrix2:
        list.append("")
    return matrix2

def change_CPA_lexicon(cpa_matrix, lexicons):
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
    
def create_new_phon_tier(file,file_name, cpa_matrix, lexicons):

    phone_key_name = phoneme_tier
    
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
                    
def change_CPA_textgrids(cpa_matrix,lexicons):
     #Create list of all TextGrid files in the directory
    output_extension_1 = '*.TextGrid'
    path1 = os.path.join(directory, output_extension_1)
    output_extension_2 = '*.tg'
    path2 = os.path.join(directory, output_extension_2)
    output_extension_3 = '*.Textgrid'
    path3 = os.path.join(directory, output_extension_3)
    files_list1 = glob.glob(path1)
    files_list2 = glob.glob(path2)
    files_list3 = glob.glob(path3)
    files_list = files_list1 + files_list2 + files_list3
    
    assert (input_CPA in lexicons), "Error: fromCPA is written incorrectly. Use one of these CPAs as input: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2"
    assert output_CPA in lexicons, "Error: toCPA is written incorrectly. Use one of these CPAs as output: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2"
    
    
    for file_name in files_list:
    
        #Some TextGrid files start with the line: 3 File type = "ooTextFile"
        #The "3" should be removed to use the textgrids package. 
        #Therefore use this function:
        change_format_first_line(file_name)
            
        #read TextGrid file
        file = tg.TextGrid(file_name)

        #Add new tier in desired CPA to TextGrid file
        file[output_CPA] =  create_new_phon_tier(file, file_name,cpa_matrix, lexicons)
        
        #Create new name of output file
        base_name = os.path.basename(file_name)
        new_name = base_name.replace(".TextGrid", "")
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
    

def main():
    lexicons = ['name','ADAPT','SAMPA1','SAMPA2','SAMPA3','CGN','CGN2']
    #matrix = create_CPA_matrix()
    cpa_matrix = read_CPA_matrix()
    assert len(cpa_matrix) == len(lexicons)
    
    if lexicon_conversion:
        change_CPA_lexicon(cpa_matrix, lexicons)
    
    if textgrid_conversion:
        change_CPA_textgrids(cpa_matrix, lexicons)
   

if __name__ == "__main__": 
    main()
    

