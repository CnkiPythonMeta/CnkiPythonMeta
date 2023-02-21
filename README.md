<pre> 
We report a computational method and program（CnkiPythonMeta）based on the Python programming language for basic data 
analysis and processing.This is also a CnkiPythonMeta package for processing data from CNKI(https://www.cnki.net/),
which the input file must be TXT format from 2000 to 2023 and it will merge the TXT file into a single EXCEL file 
friendly and frequently as basic data for further analysis.

<1>Download and install Python:
If you are completely new to Python, we highly recommend you to get started with the Python from the Python official 
website for downloading and installing Python:https://wiki.python.org/moin/BeginnersGuide/Download.

<2>Install CnkiPythonMeta:
CnkiPythonMeta releases are available as wheel packages for Windows and Linux on PyPI. Install it using pip:  
 	>>> pip install CnkiPythonMeta --upgrade  
	
<3>Firstly, you may now add files or directories that are used to contruct the input directory and file for running 
CnkiPythonMeta. When you’re done, the input directory and file structure will look like this:
   
Running_CnkiPythonMeta/  
├─Input_Data_1-Included_Literature/  
│       ├─1.txt  
│       ├─2.txt  
│       ├─...  
│       └─n.txt  
│      
└─Input_Data_2-Core_Journal_Data/ 
       └─Core_Journal_Data.txt  


If you are still struggle with the input directory and file structure, you could directly copy the test data to your 
computer and the test data are now made available at:https://github.com/CnkiPythonMeta/CnkiPythonMeta/tree/main/raw_data.
	
<4>Start the Python interpreter where Running_CnkiPythonMeta is located, then import the Python package:  
	    python/py  
	>>> import os
	>>> import xlwt
	>>> import matplotlib.pyplot as plt
	>>> from scipy.stats import pearsonr
	>>> import numpy as np 
	>>> from CnkiPythonMeta import *

<5>Merge and extract the basic data information from TXT files into a single EXEL file and output the duplicate data:  
	>>> input_dir = os.getcwd()
	>>> input_file_path = input_dir+'\\'+'Input_Data_1-Included_Literature\\'
	>>> journal_data_path = input_dir+'\\' + "Input_Data_2-Core_Journal_Data\\"
	>>> journal_list = get_journal_list(journal_data_path)
	>>> paperName_infoList_dict = get_paperName_infoList_dict(input_file_path) 
	
<6>Output filtered basic data:  
    >>> result_list = output_result(journal_list, paperName_infoList_dict)  
	
<7>Generate the histogram:  
	>>> all_year_paperNum_dict,year_paperNum_dict,first_organ_list, found_list, author_paperNum_dict, author_list,keyWords_num_dict, Keyword_set, all_keywords_list = get_year_paperNum_dict(result_list)
	>>> Histogram(year_paperNum_dict, all_year_paperNum_dict)  
	
<8>Generate the organization data:  
	>>> Organ_caculate(first_organ_list) 
	
<9>Generate the fund data:  
	>>> Found_caculate(found_list)  

<10>Generate the author data:  
	>>> Author_caculate(author_paperNum_dict, author_list) 

<11>Generate the key word data:
	>>> plot_list = KeyWord_caculate(keyWords_num_dict, Keyword_set)
	
<12>Output the orgin2023 input file:
	>>> Origin_input_file(Keyword_set, all_keywords_list, plot_list)

<pre> 	
