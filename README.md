<pre> 
we report a computational method and program（CnkiPythonMeta）based on the Python programming language for basic data analysis 
and processing.This is a CnkiPythonMeta package for processing data from CNKI(https://www.cnki.net/),which the input file 
must be TXT format form 2000 to 2022 and it will merge the TXT files into the single EXCEL file as basic data for further analysis.

<1>Download and install Python:
If you are not familiar with Python, we highly recommend you to browse the Python official website for 
downloading and installing Python:https://wiki.python.org/moin/BeginnersGuide/Download.

<2> Firstly, you may now add files or directories that are used to prepare the input directory and file for running CnkiPythonMeta.  
    When you’re done, the input directory and file structure will look like this:
   
Running_CnkiPythonMeta/  
├─Input_Data_1-Included_Literature  
│       ├─1.txt  
│       ├─2.txt  
│       ├─...  
│       └─n.txt  
│      
├─Input_Data_2-Core_Journal_Data  
│       └─Core_Journal_Data.txt  
│      
└─Input_Data_3-Citations_and_Downloads_Data

If you still struggle with the input directory and file structure, you could directly copy the test data 
to your computer and the test data are now made available at:https://github.com/CnkiPythonMeta/CnkiPythonMeta/tree/main/test


<3>CnkiPythonMeta releases are available as wheel packages for Windows and Linux on PyPI. Install it using pip:  
 	>>> pip install CnkiPythonMeta --upgrade  
	
<4>Run Python where Running_CnkiPythonMeta is located, then import python packages:  
	python/py  
	>>> import os  
	>>> import xlrd  
	>>> import xlwt  
	>>> import matplotlib.pyplot as plt  
	>>> from scipy.stats import pearsonr  	

<4>Merge and extract the basic data information from TXT files into a single EXEL file and output duplicate data:  
	>>> input_dir = os.getcwd()  
	>>> input_file_path = input_dir+'\\'+'Input_Data_1-Included_Literature\\'  
	>>> journal_data = "Input_Data_2-Core_Journal_Data\\Core_Journal_Data.txt"  
	>>> Quotations_and_downloads_data_dir = "Input_Data_3-Citations_and_Downloads_Data"  
	>>> journal_list = CnkiPythonMeta.get_journal_list(journal_data)  
	>>> paperName_infoList_dict = CnkiPythonMeta.get_paperName_infoList_dict(input_file_path)  
	
<5>Extract all downloads and citations data from TXT files into a single EXEL file:  
    >>> paperName_QuotationsDownloadsInfo_dict = CnkiPythonMeta.get_paperName_QuotationsDownloadsInfo_dict(Quotations_and_downloads_data_dir)  

<6>Mark the core journals, count the number of authors, merge citations and downloads data:  
    >>> result_list = CnkiPythonMeta.output_result(journal_list, paperName_infoList_dict, paperName_QuotationsDownloadsInfo_dict)  
	
<7>Generate the histogram:  
	>>> year_paperNum_dict, year_quations_dict, year_downloads_dict, Organ_paperNum_dict, found_paperNum_dict, author_paperNum_dict = CnkiPythonMeta.get_year_paperNum_dict(result_list)  
	>>> CnkiPythonMeta.Histogram(year_paperNum_dict)  
	
<8>Generate the line chart:  
	>>> CnkiPythonMeta.line_chart(year_quations_dict, year_downloads_dict)  
  
<9>Calculate the Pearson correlation coefficient:  
	>>> CnkiPythonMeta.caculate_pearsonr(year_paperNum_dict, year_quations_dict, year_downloads_dict)  
	
<10>Generate the organization data:  
	>>> CnkiPythonMeta.Organ_caculate(Organ_paperNum_dict)  
	
<11>Generate the fund data:  
	>>> CnkiPythonMeta.found_caculate(found_paperNum_dict)  

<12>Generate the author data:  
	>>> CnkiPythonMeta.author_caculate(author_paperNum_dict)  
	
<pre> 	
	
