
import os
import pdb
import xlrd
import xlwt
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

    


def get_paperName_infoList_dict(input_file_path):
    
    input_paper_file_list = [file for file in sorted(os.listdir(input_file_path)) if ".txt" in file]
            
    paperName_infoList_dict = {}

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("基础数据")
    title_list = ['SrcDatabase-来源库',
                    'Title-题名',
                    'Author-作者',
                    'Organ-单位',
                    'Source-文献来源',
                    'Keyword-关键词',
                    'Summary-摘要',
                    'PubTime-发表时间',
                    'FirstDuty-第一责任人',
                    'Fund-基金',
                    'Year-年',
                    'Volume-卷',
                    'Period-期',
                    'PageCount-页码',
                    'CLC-中图分类号',
                    'URL-网址',
                    'DOI-DOI']

    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
    a = []
    for file in input_paper_file_list:
     
        with open(input_file_path+file, encoding = 'gb18030') as f_file:
            f_file.readline()
            for line in f_file:

                column_list = line.strip("\r\n").split("\t")
                if column_list[0] == 'SrcDatabase-来源库':
                    continue
                elif column_list[0] == '':
                    continue
                    
                for index in range(len(column_list)):
                    sheet.write(i, index, column_list[index])
                i += 1 
                
                paperName_infoList_dict[column_list[1]]= column_list
                a.append(column_list[1])
    
    out = open("附件3-基础数据汇总-重复数据.txt", "w")
    out.write("\t".join(['文献名', '重复次数'])+'\n')
    for i in paperName_infoList_dict:
        if a.count(i) > 1:
            out.write("\t".join([i, str(a.count(i))])+"\n")
    out.close()

    workbook.save("附件1-结果文件-基础数据汇总.xls")
    return paperName_infoList_dict

    

def get_journal_list(journal_data):
    
    journal_list = []
    
    with open(journal_data, encoding = 'utf-8') as f_journal_data:
        
        f_journal_data.readline()
        for line in f_journal_data:
            
            if "中国福建省委党校" in line or "中共中央党校" in line:
                journal_list.append(line.strip())   
            elif "." in line:
                journal_list.append(line[:line.find(".")])
            elif "（" in line:
                journal_list.append(line[:line.find("（")])
            elif "." not in line:
                journal_list.append(line.strip())                

    return journal_list
    
            
def output_result(journal_list, paperName_infoList_dict, paperName_QuotationsDownloadsInfo_dict):
    
    result_list = []
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("基础数据-核心期刊-作者数量")
    title_list = ['SrcDatabase-来源库',
                    'Title-题名',
                    'Author-作者',
                    'Organ-单位',
                    'Source-文献来源',
                    'Keyword-关键词',
                    'Summary-摘要',
                    'PubTime-发表时间',
                    'FirstDuty-第一责任人',
                    'Fund-基金',
                    'Year-年',
                    'Volume-卷',
                    'Period-期',
                    'PageCount-页码',
                    'CLC-中图分类号',
                    'URL-网址',
                    'DOI-DOI',
                    '核心期刊',
                    '作者数量',
                    '引用量',
                    '下载量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1

    for paperName in paperName_infoList_dict:

        journal_name = paperName_infoList_dict[paperName][4]
        journal_name = journal_name.split("(")[0]
        column_list = paperName_infoList_dict[paperName]
        
        if column_list[2] == "":
            author_num = '0'
        else:
            author_num = len(column_list[2].strip(";").split(";"))

        if journal_name in journal_list:
            
            if paperName in paperName_QuotationsDownloadsInfo_dict:
                line_list = column_list+['是', str(author_num)] + paperName_QuotationsDownloadsInfo_dict[paperName]
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1
                result_list.append(line_list)
            else:
            
                paperName = paperName.strip('"')
                if '—' in paperName:
                    paperName = paperName[:paperName.find('—')]
                else:
                    paperName = paperName
                if '""' in paperName:
                    paperName = paperName.replace('""', '"')
                else:
                    paperName = paperName
                if paperName not in  paperName_QuotationsDownloadsInfo_dict:
                    paperName = '"' + paperName                    
                line_list = column_list+['是', str(author_num)] + paperName_QuotationsDownloadsInfo_dict[paperName]
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1
                result_list.append(line_list)
        else:
            if paperName in paperName_QuotationsDownloadsInfo_dict:
                line_list = column_list+['否', str(author_num)] + paperName_QuotationsDownloadsInfo_dict[paperName]
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1 
                result_list.append(line_list)
            else:

                paperName = paperName.strip('"')
                if '—' in paperName:
                    paperName = paperName[:paperName.find('—')]
                else:
                    paperName = paperName
                if '""' in paperName:
                    paperName = paperName.replace('""', '"')
                else:
                    paperName = paperName  
                if paperName not in  paperName_QuotationsDownloadsInfo_dict:
                    paperName = '"' + paperName
                line_list = column_list+['否', str(author_num)] + paperName_QuotationsDownloadsInfo_dict[paperName]
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1
                result_list.append(line_list)

 
    workbook.save("附件2-结果文件-基础数据-去重-核心期刊标注-作者数量统计-引用量统计-下载量统计.xls")

    return result_list
    
    
def get_paperName_QuotationsDownloadsInfo_dict(Quotations_and_downloads_data_dir):
    
    paperName_QuotationsDownloadsInfo_dict = {}
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("引用量和下载量数据")
    title_list = ['序号',
                    'Title-题名',
                    'Author-作者',
                    'Source-文献来源',
                    'PubTime-发表时间',
                    '数据库',
                    '引用量',
                    '下载量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
    
    all_write_list = []

    Quotations_and_downloads_data_file_list = os.listdir(Quotations_and_downloads_data_dir)
    
    with open(Quotations_and_downloads_data_dir+"//"+Quotations_and_downloads_data_file_list[0], encoding = 'utf-8') as f_Quotations_and_downloads_data_file:
        
        file_str = f_Quotations_and_downloads_data_file.read()
        file_str_list = file_str.split('收藏')
           
    for paperinfo in  file_str_list:
        
        paper_info_list = paperinfo.split('\t')
        paper_info_list = [paper_info_list[0].replace('\n', '')]+ paper_info_list[1:-1] + [paper_info_list[-1].replace('\n', '')]
        
        if len(paper_info_list) == 10:
            # for index in range(len(paper_info_list[:8])):
                # sheet.write(i, index, paper_info_list[index])
            # i += 1
            all_write_list.append(paper_info_list[:8]) 
        elif len(paper_info_list) > 10:

            split_list = paper_info_list[7].split("\n")
            
            if len(split_list) == 2:
                write_list = paper_info_list[:7]+[split_list[0].strip()]
                # for index in range(len(write_list)):
                    # sheet.write(i, index, write_list[index])
                # i += 1 
                all_write_list.append(write_list)             
                write_list_B = [split_list[1]]+paper_info_list[8:]
                write_list_B = write_list_B[:8]
                all_write_list.append(write_list_B) 
            else:
                write_list = paper_info_list[:7]+[split_list[1].strip()]
                # for index in range(len(write_list)):
                    # sheet.write(i, index, write_list[index])
                # i += 1 
                all_write_list.append(write_list)             
                write_list_B = [split_list[2]]+paper_info_list[8:]
                write_list_B = write_list_B[:8]                    
                all_write_list.append(write_list_B) 
        else:
            # for index in range(len(paper_info_list)):
                # sheet.write(i, index, paper_info_list[index])
            # i += 1 
            all_write_list.append(paper_info_list) 
    
    transfered_all_write_list = []
    for line_list in all_write_list:
        
        transfered_all_write_list.append([int(line_list[0])]+line_list[1:])
    
    num_list = []
    for write_list in sorted(transfered_all_write_list):
        
        write_list = [str(i) for i in write_list]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1 
        num_list.append(int(write_list[0]))
        
        paperName = write_list[1]
        if '—' in paperName:
            key = paperName[:paperName.find("—")]
            paperName_QuotationsDownloadsInfo_dict[key] = [write_list[6], write_list[7]] 
        elif '网络首发' in paperName:
            paperName = paperName[:paperName.find('网络首发')].strip()
            paperName_QuotationsDownloadsInfo_dict[paperName] = [write_list[6], write_list[7]]
        else:
            paperName_QuotationsDownloadsInfo_dict[paperName] = [write_list[6], write_list[7]]
    for i in range(1, 2501):
        if i not in num_list:
            print (i)
    workbook.save("附件4-结果文件-引用量和下载量数据.xls")        
    
    return paperName_QuotationsDownloadsInfo_dict
    
    

def get_year_paperNum_dict(result_list):
    
    year_paperNum_dict = {}
    year_quations_dict = {}
    year_downloads_dict = {}
    Organ_paperNum_dict = {}
    found_paperNum_dict = {}
    author_paperNum_dict = {}
    
    for num in range(2000, 2023):
        year_paperNum_dict[str(num)] = 0
        year_quations_dict[str(num)] = 0
        year_downloads_dict[str(num)] = 0
    
    num = 0
    for line_list in result_list:
        
        SrcDatabase,Title,Author,Organ,Source,Keyword,Summary,PubTime,FirstDuty,Fund,Year,Volume,Period,PageCount,CLC,URL,DOI,journal,author_num,Quotations,downloads = line_list
        
        if journal != '是':
            continue
        elif Quotations == '':
            continue
        
        actul_year = PubTime[:PubTime.find('-')]
        if actul_year not in year_paperNum_dict:
            year_paperNum_dict[actul_year] = 1
        else:
            year_paperNum_dict[actul_year] = year_paperNum_dict[actul_year]+1
            
        if actul_year not in year_quations_dict:
            year_quations_dict[actul_year] = int(Quotations)
        else:
            year_quations_dict[actul_year] = year_quations_dict[actul_year]+int(Quotations)

        if actul_year not in year_downloads_dict:
            year_downloads_dict[actul_year] = int(downloads)
        else:
            if downloads == "":
                year_downloads_dict[actul_year] = year_downloads_dict[actul_year]+0
            else:
                year_downloads_dict[actul_year] = year_downloads_dict[actul_year]+int(downloads)  

        Organ_list = Organ.strip().strip(";").split(";")
        Organ_list = list(set(Organ_list))
        for organ_split in Organ_list:
            organ_split = organ_split.strip('"')
            if organ_split not in Organ_paperNum_dict:
                Organ_paperNum_dict[organ_split] = 1
            else:
                Organ_paperNum_dict[organ_split]+=1
        
        if '国家自然科学基金项目(71603270;71373279)' == Fund:
            found_list =[Fund] 
        elif ');' in Fund:
            found_list = Fund.strip('"').split(');')
        else:
            found_list = Fund.strip('"').split(';')
        
        for fund_split in found_list:
            fund_split = fund_split.strip(';')
            fund_split = fund_split.strip()
            if fund_split not in found_paperNum_dict:
                found_paperNum_dict[fund_split] = 1
            else:
                found_paperNum_dict[fund_split]+=1
                
        author_list = Author.strip(';').split(';')
        
        for author_split in author_list:
            if author_split not in author_paperNum_dict:
                author_paperNum_dict[author_split] = 1
            else:
                author_paperNum_dict[author_split] += 1
        
        num += 1
    print ('纳入的文献数量为：', num)

    return year_paperNum_dict, year_quations_dict, year_downloads_dict, Organ_paperNum_dict, found_paperNum_dict, author_paperNum_dict
        
        
    
def line_chart(year_quations_dict, year_downloads_dict):
    
    plt.figure()
    year_list = []
    paperNum_list = []
    quations_list = []
    downloads_list = []
    for year in range(2000, 2023):
        
        #paperNum_list.append(year_paperNum_dict[str(year)])
        quations_list.append(year_quations_dict[str(year)])
        downloads_list.append(year_downloads_dict[str(year)])
        year_list.append(str(year))
        
    paperNum_list = [int(i) for i in paperNum_list]
    quations_list = [int(i) for i in quations_list]
    downloads_list = [int(i) for i in downloads_list]  
    

    plt.rcParams["font.sans-serif"]=['SimHei']
    plt.rcParams["axes.unicode_minus"]=False

    #plt.plot(paperNum_list)
    plt.plot(quations_list)
    plt.plot(downloads_list)
    term = '核心引用文献引用量和下载量分布图'
    plt.plot(quations_list,label='引用量')
    plt.plot(downloads_list,label='下载量')
    plt.legend(loc='upper left')
    x = range(23)
    plt.ylabel("数量")
    plt.xlabel("年份")
    plt.xticks(x, year_list, rotation=60)
    #plt.title(term)
    plt.tight_layout()	
    plt.savefig(term +".pdf")
    plt.savefig(term +".png")
    plt.close()    


def Histogram(year_paperNum_dict):

    plt.figure()
    year_list = []
    paperNum_list = []

    for year in range(2000, 2023):
        
        paperNum_list.append(year_paperNum_dict[str(year)])
        year_list.append(str(year))
        plt.rcParams["font.sans-serif"]=['SimHei']
        plt.rcParams["axes.unicode_minus"]=False
    
    x = range(23)    
    plt.bar(year_list, paperNum_list)
    plt.xticks(x, year_list, rotation=60)
    plt.plot([],label='发表量')
    plt.legend(loc='upper left')     
    #plt.title("核心期刊文献发表量分布图")
    #plt.xlabel("年份")
    plt.ylabel("数量")
    plt.xlabel("年份")
    plt.tight_layout()
    plt.savefig('核心引用文献发表量分布图' +".pdf")
    plt.savefig('核心引用文献发表量分布图' +".png")
    plt.close()
     

def caculate_pearsonr(year_paperNum_dict, year_quations_dict, year_downloads_dict):
    
    paperNum_list = []
    quations_list = []
    downloads_list = []
    
    out = open('相关系数计算.txt', 'w')
    
    for year in range(2000, 2023):
        
        paperNum_list.append(year_paperNum_dict[str(year)])    
        quations_list.append(year_quations_dict[str(year)])
        downloads_list.append(year_downloads_dict[str(year)])
        
    print ('发文量-引用量',(pearsonr(paperNum_list, quations_list)))
    print ('发文量-下载量',(pearsonr(paperNum_list, downloads_list)))
    print ('引用量-下载量',(pearsonr(quations_list, downloads_list)))
    
    out.write("\t".join(['发文量-引用量', str(pearsonr(paperNum_list, quations_list)[0]), str(pearsonr(paperNum_list, quations_list)[1])])+'\n')
    out.write("\t".join(['发文量-下载量', str(pearsonr(paperNum_list, downloads_list)[0]), str(pearsonr(paperNum_list, downloads_list)[1])])+'\n')
    out.write("\t".join(['引用量-下载量', str(pearsonr(quations_list, downloads_list)[0]), str(pearsonr(quations_list, downloads_list)[1])])+'\n')
    out.close()
           

def Organ_caculate(Organ_paperNum_dict): 

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("机构情况统计")
    title_list = ['机构', '核心引用文献发文量', '是否医院']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
    
    for organ in Organ_paperNum_dict:
        
        if organ == "" or organ == " ":
            continue
        
        if '医院' in organ:
            flag = '是'
        else:
            flag = '否'
        write_list = [organ, Organ_paperNum_dict[organ], flag]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1 
    
    workbook.save("附件5-结果文件-机构情况.xls")


def found_caculate(found_paperNum_dict):
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("基金支持情况")
    title_list = ['基金', '文献数量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
        
    for found in found_paperNum_dict:

        if found == "" or found == " ":
            continue
            
        write_list = [found, found_paperNum_dict[found]]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1     
    workbook.save("附件6-结果文件-基金支持情况.xls")
    
    
def author_caculate(author_paperNum_dict):

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("作者情况")
    title_list = ['作者', '文献数量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
        
    for author in author_paperNum_dict:
        
        write_list = [author, author_paperNum_dict[author]]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1     
    workbook.save("附件7-结果文件-作者情况.xls")    
    
    
def main():

    #step<1>Input dir
    input_dir = os.getcwd()
    input_file_path = input_dir+'\\'+'Input_Data_1-Included_Literature\\'
    journal_data = "Input_Data_2-Core_Journal_Data\\Core_Journal_Data.txt"
    Quotations_and_downloads_data_dir = "Input_Data_3-Citations_and_Downloads_Data"
    
    #step<2>Data structure
    journal_list = get_journal_list(journal_data)
    paperName_infoList_dict = get_paperName_infoList_dict(input_file_path)
    paperName_QuotationsDownloadsInfo_dict = get_paperName_QuotationsDownloadsInfo_dict(Quotations_and_downloads_data_dir)
    
    #step<3> Filtering data
    result_list = output_result(journal_list, paperName_infoList_dict, paperName_QuotationsDownloadsInfo_dict)
    year_paperNum_dict, year_quations_dict, year_downloads_dict, Organ_paperNum_dict, found_paperNum_dict, author_paperNum_dict = get_year_paperNum_dict(result_list)
    
    #step<4>line chart
    Histogram(year_paperNum_dict)
    line_chart(year_quations_dict, year_downloads_dict)

    caculate_pearsonr(year_paperNum_dict, year_quations_dict, year_downloads_dict)
    Organ_caculate(Organ_paperNum_dict)
    found_caculate(found_paperNum_dict)
    author_caculate(author_paperNum_dict)
    #pdb.set_trace()
    
    

if __name__ == "__main__":
    main()