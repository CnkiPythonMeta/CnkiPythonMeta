<pre> 
We report a computational method and program CnkiPythonMeta based on the Python programming language for basic data 
analysis and processing.This is also a CnkiPythonMeta package for summarzing the data from CNKI(https://www.cnki.net/),
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
computer and the test data are now made available at:https://github.com/CnkiPythonMeta/CnkiPythonMeta/tree/main/raw_data, 
then just running CnkiPythonMeta  to summarize the basic data.


<pre> 	
