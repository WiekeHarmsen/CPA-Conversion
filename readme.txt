ReadMe - CPA conversion

Author: Wieke Harmsen
Date: April 3th, 2020

This ReadMe will explain how to run/use the following scripts in this ZIP:
	1. dutch_CPA_conversion_lexicon.py
	2. dutch_CPA_conversion_textgrids.py
	3. dutch_CPA_conversion.py
	4. CPAs_table.csv
	5. lexicon_CGN2.txt

These scripts were made in python 3.7
Necessary Python packages:
    praat-textgrids==1.0.2 (https://pypi.org/project/praat-textgrids/1.0.2/)
    pandas==1.0.3

-------------------------------------------------------------------------------------------------------------------------------------------------

*1. dutch_CPA_conversion_lexicon.py*

Description:
This script converts the CPA (Computer Phonetic Alphabet) of a lexicon file (containing words and phonetic transcriptions).
Run this script from the command prompt.

Example:
python dutch_CPA_conversion_lexicon.py --inputLexicon lexicon_CGN2.txt --fromCPA CGN2 --toCPA ADAPT

Explanations of flags:
--inputLexicon	.txt file with Dutch lexicon. This file is saved in the same directory as the script (dutch_CPA_conversion_lexicon.py).
		Every row in the lexicon has the following structure: [word] TAB [phonetic transcription, one space between each phoneme]
		Example:
		beroepsmensen	b @ r u p s m E n s @ n
		scootermobiel	s k u t @ r m o b i l
		winteropslag	w I n t @ r O p s l A x
		keusgat	k EU s G A t
--fromCPA	The name of the phonetic alphabet in which the lexicon is written.
		Choose from: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2
--toCPA		The name of the phonetic alphabet in which you want the new lexicon to be written.
		Choose from: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2

---------------------------------------------------------------------------------------------------------------------------------------------------

*2. dutch_CPA_conversion_textgrids.py*

Description:
This script converts the CPA of a phoneme tier in a TextGrid. The phoneme tier in the new CPA is added to the original TextGrid.
Run this script from the command prompt.

Example:
python dutch_CPA_conversion_textgrids.py --directory C:\Users\home\data --phoneme_tier kaldi_phone --fromCPA CGN2 --toCPA ADAPT

Explanations of flags:
--directory	This directory contains TextGrid files (.TextGrid or .tg) with a phoneme tier.
--phoneme_tier	The name of the phoneme tier in the TextGrid.
--fromCPA	The name of the phonetic alphabet in which the specified phoneme tier in the TextGrid is written.
		Choose from: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2
--toCPA		The name of the phonetic alphabet in which the new tier in the TextGrid will be written.
		Choose from: ADAPT, SAMPA1, SAMPA2, SAMPA3, CGN, CGN2

Output:
TextGrid file(s) that contain an extra phoneme tier in the specified output CPA.

--------------------------------------------------------------------------------------------------------------------------------------------------

*3. dutch_CPA_conversion.py*

Description:
This script is able to convert both lexicons and phoneme tiers.
Run this script in a python IDE (like Spyder or PyCharm).
Specify the input parameters at the beginning of the script.
This script contains some old code. Use this script if you want to test new functionalities. 

----------------------------------------------------------------------------------------------------------------------------------------------------

*4. CPAs_table.csv*

This is a table with an overview of all phonemes in all CPAs. 
This table is based on the document CPA_ADAPT_SAMPA_CGN_CGN2_IPA_2020_04_06b.docx.
This table is used by all three python files.
If you want to add a new CPA, just fill in an extra column.
'UNK' means that there is no symbol known in the CPA for a specific phoneme.

----------------------------------------------------------------------------------------------------------------------------------------------------

*5. lexicon_CGN2.txt*

This is an example of a Dutch lexicon file, with phonemes written in CGN2.

----------------------------------------------------------------------------------------------------------------------------------------------------

END