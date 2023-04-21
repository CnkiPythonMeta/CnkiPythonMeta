import pdb
import os
import xlwt
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np
from itertools import combinations
import networkx as nx

    


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
                if 'SrcDatabase' in column_list[0]:
                    continue
                elif column_list[0] == '':
                    continue
                
                
                if '科技成果' == column_list[0]:
                    column_list = [column_list[0], column_list[2],column_list[1],  column_list[3]]+ column_list[3:]
                    for index in range(len(column_list)):
                        sheet.write(i, index, column_list[index])
                    i += 1 
                    paperName_infoList_dict[column_list[3]]= column_list
                    a.append(column_list[3])                                        
                else:                
                    for index in range(len(column_list)):
                        sheet.write(i, index, column_list[index])
                    i += 1 
                    
                    paperName_infoList_dict[column_list[1]]= column_list
                    a.append(column_list[1])
    
    out = open("附件2-原始下载数据汇总-重复数据.xls", "w")
    out.write("\t".join(['文献名', '重复次数'])+'\n')
    for i in paperName_infoList_dict:
        if a.count(i) > 1:
            out.write("\t".join([i, str(a.count(i))])+"\n")
    out.close()

    workbook.save("附件1-原始下载数据汇总.xls")

    return paperName_infoList_dict

    

def get_journal_list(journal_data_path):

    journal_data = os.listdir(journal_data_path)[0]
    
    journal_list = []
    
    with open(journal_data_path+journal_data, encoding = 'utf-8') as f_journal_data:
        
        f_journal_data.readline()
        for line in f_journal_data:
            
            if "中国福建省委党校" in line or "中共中央党校" in line:
                journal_list.append(line.strip()) 
                duplicate_journal_A = line[:line.find("（")] + '学报'
                duplicate_journal_B = line[line.find("（")+ 1: line.find("）")] + '学报'
                journal_list.append(duplicate_journal_A)
                journal_list.append(duplicate_journal_B)
                
            elif "." in line:
                journal_list.append(line[:line.find(".")])
            elif "（" in line:
                journal_list.append(line[:line.find("（")])
            elif "." not in line:
                journal_list.append(line.strip())                

    return journal_list
    
            
def output_result(journal_list, paperName_infoList_dict):
    
    result_list = []
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("基础数据-核心期刊")
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
                    '核心期刊']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1

    for paperName in paperName_infoList_dict:

        journal_name = paperName_infoList_dict[paperName][4]
        journal_name = journal_name.split("(")[0]
        column_list = paperName_infoList_dict[paperName]

        if journal_name in journal_list:
            
            line_list = column_list+['是']
            temp_list = []
            if len(line_list) < 18:
                for index in range(18-len(line_list)):
                    temp_list.append('')
                line_list = column_list+temp_list+['是']  
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1 
                result_list.append(line_list)
            else:
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1
                result_list.append(line_list)
        else:
            line_list = column_list+['否']
            temp_list = []
            if len(line_list) < 18:
                for index in range(18-len(line_list)):
                    temp_list.append('')
                line_list = column_list+temp_list+['否']
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1 
                result_list.append(line_list)
            elif len(line_list) == 19:
                line_list = column_list[:-1]+['否']
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1 
                result_list.append(line_list)
            else:
                for index in range(len(line_list)):
                    sheet.write(i, index, line_list[index])
                i += 1 
                   
                result_list.append(line_list)
 
    workbook.save("附件3-原始下载数据汇总-去重-核心期刊标注.xls")

    return result_list
    
    

def get_year_paperNum_dict(result_list):
    
    year_paperNum_dict = {}
    all_year_paperNum_dict = {}
    Organ_paperNum_dict = {}
    author_paperNum_dict = {}
    found_list = []
    author_list = []
    keyWords_num_dict = {}
    Keyword_set = set()
    all_keywords_list = []
    
    first_organ_list = []
    
    for num in range(2000, 2024):
        year_paperNum_dict[str(num)] = 0
        all_year_paperNum_dict[str(num)] = 0
    
    num = 0
    for line_list in result_list:
        
        SrcDatabase,Title,Author,Organ,Source,Keyword,Summary,PubTime,FirstDuty,Fund,Year,Volume,Period,PageCount,CLC,URL,DOI,journal= line_list
        PubTime = PubTime.replace('/', '-')
        actul_year = PubTime[:PubTime.find('-')]
        
        if Author == '':####################新排除
            continue
        elif '记者' in Author:
            continue
             
        if journal != '是':
            if actul_year not in all_year_paperNum_dict:
                all_year_paperNum_dict[actul_year] = 1
            else:
                all_year_paperNum_dict[actul_year] = all_year_paperNum_dict[actul_year]+1
            continue
               
        if actul_year not in year_paperNum_dict:
            year_paperNum_dict[actul_year] = 1
            all_year_paperNum_dict[actul_year] = 1
        else:
            year_paperNum_dict[actul_year] = year_paperNum_dict[actul_year]+1
            all_year_paperNum_dict[actul_year] = all_year_paperNum_dict[actul_year]+1
            
        Organ = Organ.strip(';')
        Organ = Organ.strip('"')
        
        if ';' in Organ:
            Organ_list = Organ.split(";")
            first_organ_list.append(Organ_list[0])
        elif ',' in Organ:
            Organ_list = Organ.split(",")
            first_organ_list.append(Organ_list[0])
        elif '·' in Organ:
            Organ_list = Organ.split(".")
            first_organ_list.append(Organ_list[0])
        elif '/' in Organ:
            Organ_list = Organ.split("/")
            first_organ_list.append(Organ_list[0])
        elif ' ' in Organ:
            Organ_list = Organ.split(" ")
            first_organ_list.append(Organ_list[0])
        elif '、' in Organ:
            Organ_list = Organ.split("、")
            first_organ_list.append(Organ_list[0])
        else:
            first_organ_list.append(Organ)

        #pdb.set_trace()
        
        Fund = Fund.strip('"')
        Fund = Fund.strip('“')
        Fund.strip('\r\n').replace('\r\n', '')
        if Fund != "":
            found_list.append(Fund)
   
        Author = Author.strip(';').strip('"')
        if '驻地记者' == Author[:4]:
            Author = Author[Author.find('驻地记者')+5:]
        
        if ';' in Author:
            Author_list = Author.split(';')
        elif ',' in Author:
            Author_list = Author.split(',')
        elif ' ' in Author:
            Author_list = Author.split(' ')
        else:
            Author_list = Author.split(';')
        
        if Author_list[0] not in author_paperNum_dict:
            author_paperNum_dict[Author_list[0]] = 1
        else:
            author_paperNum_dict[Author_list[0]] += 1
        author_list.append(Author_list[0])
        
        Keyword = Keyword.strip('"')
        Keyword_list = Keyword.split(';')
        all_keywords_list.append(Keyword_list)
        
        for keyword in Keyword_list:

            if keyword == '':
                continue
            if keyword not in keyWords_num_dict:
                keyWords_num_dict[keyword] = 1
            else:
                keyWords_num_dict[keyword] +=1
            Keyword_set.add(keyword)
        
        num += 1
    return all_year_paperNum_dict, year_paperNum_dict, first_organ_list, found_list, author_paperNum_dict, author_list, keyWords_num_dict, Keyword_set, all_keywords_list
        
        

def Histogram(year_paperNum_dict, all_year_paperNum_dict):


    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("发文量数据")
    title_list = ['年份',
                    '核心期刊论文发文量', '全部期刊论文发文量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1    
    
    year_list = []
    paperNum_list = []
    all_paperNum_list = []

    for year in range(2000, 2024):
        
        paperNum_list.append(year_paperNum_dict[str(year)])
        all_paperNum_list.append(all_year_paperNum_dict[str(year)])
        year_list.append(str(year))
        #plt.rcParams["font.sans-serif"]=['SimHei']
        
        write_list = [str(year), year_paperNum_dict[str(year)], all_year_paperNum_dict[str(year)]]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1    
    R,P = (pearsonr(paperNum_list, all_paperNum_list))[0], (pearsonr(paperNum_list, all_paperNum_list))[1]
    
    #print ('发文量-引用量',(pearsonr(paperNum_list, all_paperNum_list)))  
    #pdb.set_trace()
    
    length = len(paperNum_list)
    x = np.arange(length)
    listDate = year_list
 
    #plt.figure(dpi=500,figsize=(3.1496,2.5))
    plt.figure(dpi=500, figsize=(6.2992,4.2))
    plt.rcParams['font.sans-serif']=['STSong']
    plt.rcParams["axes.unicode_minus"]=False
    plt.rcParams['font.size'] = '9' 
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    
    total_width, n = 0.85, 2   # 柱状图总宽度，有几组数据
    width = total_width/n   # 单个柱状图的宽度
    x1 = x - width/2   # 第一组数据柱状图横坐标起始位置
    x2 = x1 + width   # 第二组数据柱状图横坐标起始位置
    
    #plt.legend(fontsize=9)
    plt.xlabel("年份", fontsize=9)   # 横坐标label 
    plt.ylabel("数量", fontsize=9)   # 纵坐标label
    plt.bar(x1, paperNum_list, width=width, label="核心期刊论文发文量", color='r')
    plt.bar(x2, all_paperNum_list, width=width, label="全部期刊论文发文量", color='b')
    plt.xticks(x, listDate, fontsize=9)   # 替换横坐标x的值
    #plt.rcParams['savefig.dpi'] = 500
    
    
    for a, b in zip(x1, paperNum_list):
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=7)
     
    for a, b in zip(x2, all_paperNum_list):
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=7)    
    
    plt.annotate('r='+str(R), (0,850))
    plt.annotate('P='+str(P), (0,800))
    plt.legend(loc='upper left')  
    plt.xticks(x, year_list, rotation=60)
    plt.tight_layout()
    plt.savefig('图1' +".pdf")
    plt.savefig('图1' +".jpg")
    plt.close()
    workbook.save("附件4-论文发文量数据.xls")
    
    
    
def caculate_pearsonr(year_paperNum_dict, year_quations_dict, year_downloads_dict):
    
    paperNum_list = []
    quations_list = []
    downloads_list = []
    
    out = open('相关系数计算.txt', 'w')
    
    for year in range(2000, 2024):
        
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
           

def Organ_caculate(first_organ_list): 

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("机构情况统计")
    title_list = ['序号', '第一机构']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
    
    processed_first_organ_list = []
    B_processed_first_organ_list = []
    for organ in first_organ_list:
        
        if '(' in organ:
            organ = organ[:organ.find('(')]
            if '·' in organ:
                processed_first_organ_list.append(organ.split('·')[0])
            else:
                processed_first_organ_list.append(organ)
        elif '、' in organ:
            processed_first_organ_list.append(organ.split('、')[0])
        elif '·' in organ:
            processed_first_organ_list.append(organ.split('·')[0])
        elif '(' in organ:
            processed_first_organ_list.append(organ.split('(')[0])            
        elif '/' in organ:
            processed_first_organ_list.append(organ.split('/')[0])              
        else:
            processed_first_organ_list.append(organ)
    num = 0
    for organ in processed_first_organ_list:

        organ = organ.strip()
        if organ == '北京大学医学部公共卫生学院':
            B_processed_first_organ_list.append('北京大学医学部')
            num+= 1   
        elif '国家医疗保障研究院华科基地华中科技大学' in organ:
            B_processed_first_organ_list.append('国家医疗保障研究院')
            num+= 1             
        elif (organ[-2:] == '大学' or organ[-2:] == '医院'):
            B_processed_first_organ_list.append(organ)
            num+= 1
            
        elif '附属' in organ:
            
            if '中心' in organ and '医院' not in organ:
                B_processed_first_organ_list.append(organ[:organ.find('中心')+2])
                num+= 1               
            elif '保健院' in organ and '医院' not in organ:
                B_processed_first_organ_list.append(organ[:organ.find('保健院')+3])
                num+= 1
            else:
                B_processed_first_organ_list.append(organ[:organ.find('医院')+2])
                num+= 1

        elif '大学' in organ and '医院' not in organ:
            if '北京大学医学部' in organ:
                B_processed_first_organ_list.append(organ)
                num+= 1
            else:
                B_processed_first_organ_list.append(organ[:organ.find('大学')+2])
                num+= 1
        elif '管理' in organ and '学院' in organ and '大学' not in organ:
            B_processed_first_organ_list.append(organ[:organ.find('学院')+2])#
            num += 1

        elif '中心' == organ[-2:] and '学院' not in organ and '医院' not in organ:
            B_processed_first_organ_list.append(organ)
            num += 1
        elif '医院' in organ and '大学' in organ:
            if '清华大学' in organ or '华中科技' in organ:                
                B_processed_first_organ_list.append(organ[:organ.find('大学')+2])
                num+= 1
            else:
                B_processed_first_organ_list.append(organ[:organ.find('医院')+2])
                num+= 1                  
        elif '中国' in organ:
            if '中国医学科学院' in organ:
                B_processed_first_organ_list.append('中国医学科学院研究所')
                num+=1
            else:
                B_processed_first_organ_list.append(organ)
                num+=1
        elif '学院' in organ and '学校' not in organ and '医院' not in organ:
            B_processed_first_organ_list.append(organ[:organ.find('学院')+2])
            num+=1
        elif '医院' in organ:
            if '学校' in organ:
                B_processed_first_organ_list.append(organ[:organ.find('学校')+2])
                num+=1
            elif '集团' in organ:
                B_processed_first_organ_list.append(organ[:organ.find('集团')+2])
                num+=1 
            elif '杂志' in organ:
                B_processed_first_organ_list.append(organ)
                num+=1 
            elif '研究所' in organ:
                B_processed_first_organ_list.append(organ)
                num+=1 
            else:
                B_processed_first_organ_list.append(organ[:organ.find('医院')+2])
                num+= 1 
        elif '中心' in organ:
            B_processed_first_organ_list.append(organ[:organ.find('中心')+2])
            num+= 1 
        elif '委员会' in organ:
            B_processed_first_organ_list.append(organ[:organ.find('委员会')+3])
            num+= 1 
        elif organ[-1] == '局':
            B_processed_first_organ_list.append(organ)
            num+= 1         
        elif '所' in organ:
            B_processed_first_organ_list.append(organ[:organ.find('所')+1])
            num+= 1
        elif organ[-1] == '院':
            if '校' in organ:
                B_processed_first_organ_list.append(organ[:organ.find('校')+1])
                num+= 1   
            else:
                B_processed_first_organ_list.append(organ)
                num+= 1  
        elif '委' in organ:
            if '健康委' in organ:
                B_processed_first_organ_list.append(organ[:organ.find('委')+1])
                num+= 1 
            else:
                B_processed_first_organ_list.append(organ)
                num+= 1  
        elif '院' in  organ:
            B_processed_first_organ_list.append(organ[:organ.find('院')+1])
            num+= 1 
            
        elif '协会' in  organ:
            B_processed_first_organ_list.append(organ[:organ.find('协会')+2])
            num+= 1 
        else:
            B_processed_first_organ_list.append(organ)
            num+=1
    j = 1
    for organ in set(processed_first_organ_list):
        write_list = [str(j), organ]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1
        j+=1
    workbook.save("附件5-机构情况.xls")
    
    
    
def Author_caculate(author_paperNum_dict,author_list):

    core_author_set = set()
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("作者情况")
    title_list = ['第一作者', '文献数量']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1
        
    for author in author_list:
        
        if author == '':
            continue
        elif '记者' in author:
            continue
        write_list = [author, author_paperNum_dict[author]]
        
        if int(author_paperNum_dict[author]) > 3:
            core_author_set.add(author)
        
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1

    workbook.save("附件7-作者情况.xls")  
  
    return core_author_set
    

def Found_caculate(found_list):
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("基金情况")
    # title_list = ['基金项目']
    # i = 0
    # for index in range(len(title_list)):
        # sheet.write(i, index, title_list[index])
    # i += 1
    i = 0    
    for Found in found_list:
        
        write_list = [Found]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1     
    workbook.save("附件6-基金情况.xls") 
    

def KeyWord_caculate(keyWords_num_dict, Keyword_set):
    
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("关键词情况")
    
    all_Keyword_num_list = []

    i = 0    
    for keyword in Keyword_set:
        
        write_list = [keyword, keyWords_num_dict[keyword]]
        all_Keyword_num_list.append(write_list)
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1     
    workbook.save("附件8-关键词情况.xls")

    sorted_all_Keyword_num_list = sorted(all_Keyword_num_list, key=(lambda x : x[1]), reverse=True) 
    plot_list = sorted_all_Keyword_num_list[:35]
    
    return plot_list
    

def Origin_input_file(Keyword_set, all_keywords_list, plot_list):

    findal_plot_list = []
    
    for keyword_list in plot_list:
        findal_plot_list.append(keyword_list[0])

    out = open('orgin-input.txt', 'w')
    
    keywordA_keywordB_value_dict = {}
    
    for keyWord in Keyword_set:
        keywordA_keywordB_value_dict[keyWord] = {}
    
    for keywordA in keywordA_keywordB_value_dict:

         for keyword_list in all_keywords_list:
            
            for keywordB in keyword_list:

                if keywordA != keywordB and keywordA in keyword_list and keywordB not in keywordA_keywordB_value_dict[keywordA]:
                    keywordA_keywordB_value_dict[keywordA][keywordB] = 1
                #pdb.set_trace()
                elif keywordA != keywordB and keywordA in keyword_list and keywordB in keywordA_keywordB_value_dict[keywordA]:

                    keywordA_keywordB_value_dict[keywordA][keywordB] += 1
    
    
    for keyWord in findal_plot_list:
        
        if keyWord == '':
            continue
        for keywordB in keywordA_keywordB_value_dict[keyWord]:
            
            if keyWord == keywordB:
                continue
            elif keywordB == '':
                continue
            write_line_list = [keyWord, keywordB, str(keywordA_keywordB_value_dict[keyWord][keywordB])]
            out.write('\t'.join(write_line_list)+'\n')
    out.close()
    #pdb.set_trace()
            

def make_autopct(value_list):
    def my_autopct(pct):
        total = sum(value_list)
        val = int(round(pct*total/100.0))
        # 同时显示数值和占比的饼图
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        
    return my_autopct
    


def journal_pie_plot(result_list):
    
    journal_num_dict = {}
    
    for line_list in result_list:

        if line_list[-1] == '否':
            continue
        elif line_list[2] == '':####################新排除
            continue
        elif '记者' in line_list[2]:
            continue        
        
        journal= line_list[4]
        
        if '(' in journal:
            journal = journal[:journal.find('(')]
        else:
            journal = journal
        
        if journal not in journal_num_dict:
            journal_num_dict[journal] = 1
        else:
            journal_num_dict[journal] += 1
        
    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("期刊发文")
    
    journal_num_list = []
    i = 0
    for journal in journal_num_dict:
        
        line_list = [journal, journal_num_dict[journal]]
        journal_num_list.append(line_list)
        for index in range(len(line_list)):
            sheet.write(i, index, line_list[index])
        i += 1     
    workbook.save("附件9-期刊发文情况.xls")
    
    sorted_journal_num_list = sorted(journal_num_list, key=lambda x:x[1], reverse=True)
    plot_list = []
    pie_label_list = []
    pie_value_list = []
    other_journal = 0
    for line_list in sorted_journal_num_list:
        if line_list[1] < 11:
            other_journal += line_list[1]
            continue
        #plot_list.append((line_list[0]+str(line_list[1])+'篇', line_list[1]))
        plot_list.append((line_list[0], line_list[1]))

        #pie_label_list.append(line_list[0]+str(line_list[1])+'篇')
        #pie_value_list.append(line_list[1])
    #pie_label_list.append('论文数量<10的期刊'+str(other_journal)+'篇') 
    #pie_value_list.append(other_journal)

    #plot_list.append(('论文数量<10的期刊'+str(other_journal)+'篇', other_journal))
    plot_list.append(('论文数量<10的期刊', other_journal))
    
    for line_tuple in sorted(plot_list, key=lambda x:x[1], reverse=True):
        jornal, value = line_tuple
        pie_label_list.append(jornal)
        pie_value_list.append(value)    
        
    plt.figure(dpi=500, figsize=(6.2992,4.2))
    plt.rcParams['font.sans-serif']=['STSong']
    plt.rcParams["axes.unicode_minus"]=False
    plt.rcParams['font.size'] = '9' 
    labels =pie_label_list
    explode = pie_value_list
    plt.pie(pie_value_list, labels=labels, autopct=make_autopct(pie_value_list))
    #plt.rcParams['legend.fontsize'] = 7 # 图例大小
    #plt.legend(loc='upper left')
    plt.axis('equal')#

    plt.tight_layout()
    plt.savefig('图2' +".pdf")
    plt.savefig('图2' +".jpg")
    plt.close()
    
    
def Author_network(core_author_set, result_list):
    
    all_author_list = []
    all_author_network_list = []

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("全部作者情况")
    title_list = ['序号', '作者数量', '作者']
    i = 0
    j = 1
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1  
    
    for line_list in result_list:

        if line_list[-1] == '否':
            continue
        elif line_list[2] == '':####################新排除
            continue
        elif '记者' in line_list[2]:
            continue  
        elif line_list[2] == '':
            line_list = [j, 0]
            for index in range(len(line_list)):
                sheet.write(i, index, line_list[index])
            i += 1 
            j += 1        
            continue
            
        author_str = line_list[2]

        if ';' in author_str:
            author_list = author_str.strip(';').strip('"').split(';')
        elif ',' in author_str:
            author_list = author_str.strip(';').strip('"').split(',')
            
        all_author_list.append(author_list)


    for author_list in all_author_list:
        
        # flag = 0
        # for author in author_list:
            # if author in core_author_set:
                # flag = 1
        # if flag == 1:
        #all_author_network_list.append(author_list)
            
        #flag = 0
        
        line_list = [j, len(author_list)]+author_list
        for index in range(len(line_list)):
            sheet.write(i, index, line_list[index])
        i += 1 
        j += 1
    all_author_set = set()
    for i_list in all_author_list:
        for i in i_list:
            all_author_set.add(i)
    workbook.save("附件10-"+str(len(all_author_set))+"全部作者情况.xls")
    
    node_author_set = set()
    author_author_dict = {}
    
    for author_network_list in all_author_list:
        #pdb.set_trace()
        sorted_author_network_list = sorted(author_network_list)
        #if len(sorted_author_network_list) == 1 and sorted_author_network_list[0] in core_author_set:
        if len(sorted_author_network_list) == 1:
            #node_author_set.add(author_network_list[0])
            if (sorted_author_network_list[0],sorted_author_network_list[0]) not in author_author_dict:
                author_author_dict[(sorted_author_network_list[0],sorted_author_network_list[0])] = 1
            else:
                author_author_dict[(sorted_author_network_list[0],sorted_author_network_list[0])] += 1
        elif len(sorted_author_network_list) == 2:
            A, B = sorted_author_network_list
            if (A,B) not in author_author_dict:
                author_author_dict[(A,B)] = 1
            else:
                author_author_dict[(A,B)] += 1
        else:
            author_tuple_list = sorted(list(combinations(sorted_author_network_list, 2)))
            for author_tuple in author_tuple_list:
                A, B = author_tuple
                if (A,B) not in author_author_dict:
                    author_author_dict[(A,B)] = 1
                else:
                    author_author_dict[(A,B)] += 1  

    core_cuthor_matrix_list = []
    plot_core_set = set()
    
    for A, B in author_author_dict:
        
        # if A not in core_author_set and B not in core_author_set:
            # continue       
        core_cuthor_matrix_list.append((A, B, author_author_dict[(A, B)]))
        

        plot_core_set.add(A)
        plot_core_set.add(B)
        
    # final_plot_node_author = set()
    # for author in node_author_set:
        # if author not in plot_core_set:
            # final_plot_node_author.add(author)
    
    # filted_core_cuthor_matrix_list = []
    # for tuple_info in core_cuthor_matrix_list:
        
        # A, B, num = tuple_info
        # if num < 8:
            # continue
        # filted_core_cuthor_matrix_list.append(tuple_info)
        
    plt.figure(dpi=500, figsize=(6.2992,4.2))
    plt.rcParams['font.sans-serif']=['STSong']
    plt.rcParams["axes.unicode_minus"]=False
    plt.rcParams['font.size'] = '9' 
     
    # #edges = read_excel('A.xlsx')#这里#数据集的位置
    # edges = filted_core_cuthor_matrix_list
    # g= nx.Graph()#定义有向图，无向图是nx.Graph()
    # g.add_weighted_edges_from(edges)

    # #生成节点位置序列
    # #pos = nx.random_layout(g)
    # pos=nx.random_layout(g) 
    # weights = nx.get_edge_attributes(g, "weight")
    # nx.draw_networkx(g, pos, with_labels=True,node_size = 20)
    # nx.draw_networkx_edge_labels(g, pos, edge_labels=weights)
    filtered_author_author_dict = {}
    for AB in author_author_dict:
        if author_author_dict[AB] < 7:
            continue
        filtered_author_author_dict[AB] = author_author_dict[AB]
        
    edgeWidth=[]
    for i in filtered_author_author_dict.values():
        edgeWidth.append(i/5)
    
    print(len(edgeWidth))

    #plt.figure(figsize=(16, 9))#图片比例尺，跟dpi合并计算后就是图片的分辨率，注意figure要放在画图开始前
    g=nx.MultiGraph()
    g.add_edges_from(filtered_author_author_dict.keys())
    d=dict(g.degree)

    #nx.draw_circular(g,nodelist=d.keys(),node_size=[v*50 for v in d.values()],node_color=range(35),cmap=plt.cm.Paired,
    nx.draw_circular(g,nodelist=d.keys(),node_size = 80, node_color=range(46),cmap=plt.cm.Paired,
                     with_labels=True,edge_color=range(len(filtered_author_author_dict)),edge_cmap=plt.cm.Dark2,alpha=1.0,width=edgeWidth)
    # node_color，要使用报错提醒的数字，edge_color使用len(edgewidth),但直接引用报错。
    #nodelist节点名称，node_size节点大小，node_color&cmap节点颜色的映射，edge_color&edge_cmap线颜色的映射，width宽度的值

    plt.savefig('图3' +".pdf")
    plt.savefig('图3' +".jpg")
    plt.close()
        
    # pos=nx.circular_layout(G)          # 生成圆形节点布局
    # pos=nx.random_layout(G)            # 生成随机节点布局
    # pos=nx.shell_layout(G)             # 生成同心圆节点布局
    # pos=nx.spring_layout(G)            # 利用Fruchterman-Reingold force-directed算法生成节点布局
    # pos=nx.spectral_layout(G)          # 利用图拉普拉斯特征向量生成节点布局
    # pos=nx.kamada_kawai_layout(G)      #使用Kamada-Kawai路径长度代价函数生成布局        
         


    
def keyword_analysis(result_list):   
    
    year_keywordList_dict = {}

    workbook=xlwt.Workbook(encoding='gb18030')
    sheet = workbook.add_sheet("年度关键词频统计")
    title_list = ['年份', '关键词及其频率']
    i = 0
    for index in range(len(title_list)):
        sheet.write(i, index, title_list[index])
    i += 1      
    for line_list in result_list:
        
        if line_list[-1] == '否':
            continue
        SrcDatabase,Title,Author,Organ,Source,Keyword,Summary,PubTime,FirstDuty,Fund,Year,Volume,Period,PageCount,CLC,URL,DOI,journal= line_list            
        actul_year = PubTime[:PubTime.find('-')]

        Keyword = Keyword.strip('"')
        Keyword_list = Keyword.split(';')
        
        if actul_year not in year_keywordList_dict:
            year_keywordList_dict[actul_year] = Keyword_list
        else:
            year_keywordList_dict[actul_year]+= Keyword_list
            
    for year in year_keywordList_dict:
        
        key_word_str = ''
        keyword_num_set = set()
        for keyword in year_keywordList_dict[year]:
            if keyword == '':
                continue
                
            keyword_num_set.add((keyword, year_keywordList_dict[year].count(keyword)))
        
        sorted_keyword_list = sorted(list(keyword_num_set), key=(lambda x : x[1]), reverse=True)
        
        for keyword, num in sorted_keyword_list[:5]:
            
            key_word_str+= keyword+'='+str(num)+';'
            
        write_list = [year, key_word_str]
        for index in range(len(write_list)):
            sheet.write(i, index, write_list[index])
        i += 1           
        
    workbook.save("附件11-年度关键词频统计.xls")        

    
    
    
def main():

    #step<1>Input dir
    input_dir = os.getcwd()
    input_file_path = input_dir+'\\'+'Input_Data_1-Included_Literature\\'
    journal_data_path = input_dir+'\\' + "Input_Data_2-Core_Journal_Data\\"
    

    #step<2>Data structure
    journal_list = get_journal_list(journal_data_path)
    paperName_infoList_dict = get_paperName_infoList_dict(input_file_path)
    
    #step<3> Filtering data
    result_list = output_result(journal_list, paperName_infoList_dict)
    all_year_paperNum_dict, \
    year_paperNum_dict,\
    first_organ_list, \
    found_list, \
    author_paperNum_dict, author_list, \
    keyWords_num_dict, Keyword_set, all_keywords_list = get_year_paperNum_dict(result_list)
    
    #step<4>Histogram
    Histogram(year_paperNum_dict, all_year_paperNum_dict)
    Organ_caculate(first_organ_list)
    Found_caculate(found_list)
    
    core_author_set = Author_caculate(author_paperNum_dict, author_list)
    plot_list = KeyWord_caculate(keyWords_num_dict, Keyword_set)
    Origin_input_file(Keyword_set, all_keywords_list, plot_list)
    journal_pie_plot(result_list)
    Author_network(core_author_set, result_list)
    keyword_analysis(result_list)
    
       
    

if __name__ == "__main__":
    main()