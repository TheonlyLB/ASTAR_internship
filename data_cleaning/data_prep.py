# To prep data for Thai translation engine
# 1. load data from file
# 2. preprocess/normalize text
# 3. save parallel data to text file as .en and .th respectively
# also contains methods to concatenate text files, and for train-valid-test split


import argparse
from pathlib import Path
import csv
import os
import glob
import pandas as pd
import numpy as np
from text_normalization import compose_processing

def list_directory_files(directory, extension=None):
    if extension is None:
        return [f for f in glob.glob(f"{directory}/*")]
    else:
        return [f for f in glob.glob(f"{directory}/*.{extension}")]

def load_csvfile(filename, column=None):
    """opens text file and return sentences in a list. Specify a column header if required."""
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')
        if column is not None:
            lines = [row[column] for row in reader]
        else:
            lines = [row for row in reader]
    return lines

def load_textfile(filename):
    with open(filename, encoding="utf-8-sig") as f: #utf-8-sig
        #lines = f.readlines()
        lines = [l for l in (line.strip() for line in f) if l] #skips empty line
    return lines

def read_en_th(filename):
    en_lines = load_csvfile(filename, 'en_text')
    th_lines = load_csvfile(filename, 'th_text')
    return en_lines, th_lines

def write_lines_to_file(lines,outdir,filename,outname):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    open(f"{outdir}/{filename}{outname}", 'w', encoding='utf-8').writelines(l.strip()+'\n' for l in lines)

#PROCESS SCB
def process_scb(args):
    if args.dir is not None:
        files_list = list_directory_files(args.dir, 'csv')
    else:
        files_list = args.filename
    for input_file in files_list:
        basename = os.path.splitext(os.path.basename(input_file))[0]
        print(f"Now processing: {basename}")
        en_lines, th_lines = read_en_th(input_file)
        print("Before text normalization",en_lines[:5])
        print("Before text normalization",th_lines[:5])

        en_lines = [compose_processing(line) for line in en_lines]
        th_lines = [compose_processing(line) for line in th_lines]

        write_lines_to_file(en_lines,args.outdir,basename,'.en')
        write_lines_to_file(th_lines,args.outdir,basename,'.th')
        print("After text normalization",en_lines[:5])
        print("After text normalization",th_lines[:5])
        print("en lines", len(en_lines))
        print("th lines", len(th_lines))
        print(th_lines[:5])


#PROCESS BBC
def read_excel(filename, sheet_name=0, **kwargs):
    """"Process excel file given filename, sheetname
    columns are assumed to be Eng and Thai"""
    df = pd.read_excel(filename, sheet_name, engine='openpyxl', **kwargs)
    print(df.head())
    headers = ['Eng', 'Thai']
    df = remove_empty_entries_in_df(df, headers)
    en_lines = df[headers[0]].astype('string').tolist()
    th_lines = df[headers[1]].astype('string').tolist()
    print("Before text normalization",en_lines[:5])
    print("Before text normalization",th_lines[525:530])

    en_lines = [compose_processing(line) for line in en_lines]
    th_lines = [compose_processing(line) for line in th_lines]
    print("After text normalization",en_lines[:5])
    print("After text normalization",th_lines[525:530])
    print("en lines", len(en_lines))
    print("th lines", len(th_lines))
    return en_lines, th_lines

def process_bbc(args):
    en_lines, th_lines = read_excel(args.filename[0],'BBC_Paragraph')
    write_lines_to_file(en_lines,args.outdir,'BBC_Paragraph','.en')
    write_lines_to_file(th_lines,args.outdir,'BBC_Paragraph','.th')

def remove_empty_entries_in_df(df, headers):
    """headers is a list of column names"""
    ori_rows = len(df.index)
    print("original rows",ori_rows)
    for name in headers:
        #drop rows with NaNs
        df = df.dropna(subset=[name])
        #drop rows with empty cells
        df[df[name].str.strip().astype(bool)]
        #drop rows containing values
        values = [u'\xa0']
        df = df[df[name].isin(values) == False]

    rows_removed = ori_rows - len(df.index)
    print("Empty rows removed",rows_removed)
    return df


#PROCESS SOFTWARE ENGINEERING GROUP TASK1
def process_articles(args):
    if args.dir is not None:
        files_list = list_directory_files(args.dir)
    else:
        files_list = args.filename
    for input_file in files_list:
        basename = os.path.splitext(os.path.basename(input_file))[0]
        ext = os.path.splitext(os.path.basename(input_file))[1]
        print(f"Now processing: {basename}")
        lines = load_textfile(input_file)
        print('lines',len(lines))
        print("Before text normalization",lines[:5])
        normalized_lines = [compose_processing(line) for line in lines]
        print("After text normalization",normalized_lines[:5])
        #empty_lines = [921561, 936125, 936448, 936500, 936751, 2232914, 2233473]
        #for line_no, line in enumerate(normalized_lines):
        #    if not line.strip():
        #        empty_lines.append(line_no)
        #print(empty_lines)
        #for i in reversed(empty_lines): #read list backwards so indexing of future things to delete doesn't change
        #    del normalized_lines[i]
        print('lines',len(normalized_lines))
        write_lines_to_file(normalized_lines,args.outdir,basename,ext)

def process_magazine(args):
    en_lines, th_lines = read_excel(args.filename[0], names=['Eng','Thai'])
    write_lines_to_file(en_lines,args.outdir,'magazine','.en')
    write_lines_to_file(th_lines,args.outdir,'magazine','.th')


def read_excel_batch(filename, headers, *args, **kwargs):
    assert len(headers)*2 == len(args), f"headers {len(headers)}, args {len(args)*2}"
    xls = pd.ExcelFile(filename)
    # Now you can list all sheets in the file
    datasets = xls.sheet_names
    print(datasets)
    args = list(args)
    for dataset in datasets:
        args = process_excel_sheet(filename, dataset, headers, args)
    return args

def process_excel_sheet(filename, sheetname, headers, args):
    print(f"Now processing: {sheetname}")
    df = pd.read_excel(filename, sheet_name=sheetname, engine='openpyxl') #xlrd
    print(df.head())
    df = df[headers]
    #df_headers = df.columns.values.tolist()
    df = remove_empty_entries_in_df(df, headers)
    no_of_columns = len(headers)

    for i, header in enumerate(headers):
        lines, len_lines = process_df_column(df, header)
        args[i].extend(lines)
        args[i+no_of_columns] += len_lines
    return args

def process_df_column(df, header):
    lines = df[header].astype('string').tolist()
    normalized_lines = [compose_processing(line) for line in lines]
    print(f"{header} lines", len(normalized_lines), normalized_lines[:3])
    return normalized_lines, len(normalized_lines)

#PROCESS SOFTWARE ENGINEERING GROUP TASK2
def process_seg2_task1(args):
    """1 en line, 3 th translations"""
    column_headers = ['original sentence (EN)', 'translated sentence 1 (TH)', 'translated sentence 2 (TH)', 'translated sentence 3 (TH)']
    all_en_lines = []
    all_thai_lines_1 = [] #ref 1
    all_thai_lines_2 = [] #ref 2
    all_thai_lines_3 = [] #ref 3
    en_line_count = 0
    th1_line_count = 0
    th2_line_count = 0
    th3_line_count = 0
    all_en_lines, all_thai_lines_1, all_thai_lines_2, all_thai_lines_3, en_line_count, th1_line_count, th2_line_count, th3_line_count = read_excel_batch(
                                                                                        args.filename[0],column_headers,all_en_lines,
                                                                                        all_thai_lines_1,all_thai_lines_2,all_thai_lines_3,
                                                                                        en_line_count,th1_line_count,th2_line_count,
                                                                                        th3_line_count)
    print(en_line_count)
    print(th1_line_count)
    print(th2_line_count)
    print(th3_line_count)
    print(len(all_en_lines))
    print(len(all_thai_lines_1))
    print(len(all_thai_lines_2))
    print(len(all_thai_lines_3))
    write_lines_to_file(all_en_lines,args.outdir,'task1','.en.1')
    write_lines_to_file(all_en_lines,args.outdir,'task1','.en.2')
    write_lines_to_file(all_en_lines,args.outdir,'task1','.en.3')
    write_lines_to_file(all_thai_lines_1,args.outdir,'task1','.th.1')
    write_lines_to_file(all_thai_lines_2,args.outdir,'task1','.th.2')
    write_lines_to_file(all_thai_lines_3,args.outdir,'task1','.th.3')

def process_seg2_task2(args):
    """1 th line, 3 en translations"""
    column_headers = ['original sentence (TH)', 'translated sentence 1 (EN)', 'translated sentence 2  (EN)', 'translated sentence 3 (EN)']
    all_th_lines = []
    all_en_lines_1 = [] #ref 1
    all_en_lines_2 = [] #ref 2
    all_en_lines_3 = [] #ref 3
    th_line_count = 0
    en1_line_count = 0
    en2_line_count = 0
    en3_line_count = 0
    all_th_lines, all_en_lines_1, all_en_lines_2, all_en_lines_3, th_line_count, en1_line_count, en2_line_count, en3_line_count = read_excel_batch(
                                                                                        args.filename[0],column_headers, all_th_lines, all_en_lines_1,
                                                                                        all_en_lines_2, all_en_lines_3, th_line_count,
                                                                                        en1_line_count, en2_line_count, en3_line_count)
    print(th_line_count)
    print(en1_line_count)
    print(en2_line_count)
    print(en3_line_count)
    print(len(all_th_lines))
    print(len(all_en_lines_1))
    print(len(all_en_lines_2))
    print(len(all_en_lines_3))
    write_lines_to_file(all_th_lines,args.outdir,'task2','.th.1')
    write_lines_to_file(all_th_lines,args.outdir,'task2','.th.2')
    write_lines_to_file(all_th_lines,args.outdir,'task2','.th.3')
    write_lines_to_file(all_en_lines_1,args.outdir,'task2','.en.1')
    write_lines_to_file(all_en_lines_2,args.outdir,'task2','.en.2')
    write_lines_to_file(all_en_lines_3,args.outdir,'task2','.en.3')

def process_seg2_task3(args):
    """1 th line, 1 en translation"""
    column_headers = ['original sentence (EN)', 'translated sentence (TH)']
    all_th_lines = []
    all_en_lines = [] #ref 1
    th_line_count = 0
    en_line_count = 0
    all_en_lines, all_th_lines, en_line_count, th_line_count = read_excel_batch(
                                                                args.filename[0],column_headers, all_en_lines, all_th_lines,
                                                                en_line_count, th_line_count)
    print(th_line_count)
    print(en_line_count)
    print(len(all_th_lines))
    print(len(all_en_lines))
    write_lines_to_file(all_th_lines,args.outdir,'task4','.th.1')
    write_lines_to_file(all_en_lines,args.outdir,'task4','.en.1')

#process BBC test set
def process_bbc_test(args):
    """1 th line, 1 en translation"""
    column_headers = ['BBC News_English', 'BBC News_Thai']
    all_th_lines = []
    all_en_lines = [] #ref 1
    th_line_count = 0
    en_line_count = 0
    all_en_lines, all_th_lines, en_line_count, th_line_count = read_excel_batch(
                                                                args.filename[0],column_headers, all_en_lines, all_th_lines,
                                                                en_line_count, th_line_count)
    print(th_line_count)
    print(en_line_count)
    print(len(all_th_lines))
    print(len(all_en_lines))
    write_lines_to_file(all_th_lines,args.outdir,'BBC_test','.th')
    write_lines_to_file(all_en_lines,args.outdir,'BBC_test','.en')

#process ALT
def process_textfile(args, outname, outextention=None):
    """e.g. to process asian language treebank thai-en"""
    if args.dir is not None:
        files_list = list_directory_files(args.dir)
    else:
        files_list = args.filename
    for input_file in files_list:
        basename = os.path.splitext(os.path.basename(input_file))[0]
        if outextention is None:
            outextention = os.path.splitext(os.path.basename(input_file))[1]
        print(f"Now processing: {basename}")
        lines = load_textfile(input_file)
        print('lines',len(lines))
        print("Before text normalization",lines[:5])
        normalized_lines = [compose_processing(line) for line in lines]
        print("After text normalization",normalized_lines[:5])
        print('lines',len(normalized_lines))
        write_lines_to_file(normalized_lines,args.outdir,outname,outextention)


def concat_text_files(args, extension, outname):
    import shutil

    file_list = list_directory_files(args.dir, extension)
    print(file_list)

    with open(f'{args.outdir}/{outname}','wb',encoding='utf-8') as wfd:
        for f in file_list:
            with open(f,'rb',encoding='utf-8') as fd:
                shutil.copyfileobj(fd, wfd)

def train_valid_test_split(args, validlines, testlines, seed=1):
    """validlines  testlines can be float between 0 and 1
    representing proportion of dataset to include in each,
    or an int representing actual no of lines"""
    from sklearn.model_selection import train_test_split

    assert len(args.filename) == 2, "load source and target files!"
    basename1 = os.path.splitext(os.path.basename(args.filename[0]))[0]
    outextention1 = os.path.splitext(os.path.basename(args.filename[0]))[1]
    print(f"Now loading: {basename1}")
    lines1 = load_textfile(args.filename[0])
    print('total lines',len(lines1))
    basename2 = os.path.splitext(os.path.basename(args.filename[1]))[0]
    outextention2 = os.path.splitext(os.path.basename(args.filename[1]))[1]
    print(f"Now loading: {basename2}")
    lines2 = load_textfile(args.filename[1])
    print('total lines',len(lines2))
    assert len(lines1) == len(lines2), "No. of lines do not match!"

    if validlines < 1:
        assert testlines < 1, "Either provide a fraction between 0.0 and 1.0 or an int for number of lines!"
        validation_ratio = validlines
        test_ratio = testlines
        train_ratio = 1 - validation_ratio - test_ratio
    else:
        assert testlines >= 1, "Either provide a fraction between 0.0 and 1.0 or an int for number of lines!"
        validation_ratio = validlines/len(lines1)
        test_ratio = testlines/len(lines1)
        train_ratio = 1 - validation_ratio - test_ratio
    print(f"train:valid:test split = {train_ratio}:{validation_ratio}:{test_ratio}")

    x_train, x_test_valid, y_train, y_test_valid = train_test_split(lines1, lines2, test_size=1-train_ratio, random_state=seed)
    x_val, x_test, y_val, y_test = train_test_split(x_test_valid, y_test_valid, test_size=test_ratio/(test_ratio + validation_ratio), shuffle=False)
    write_lines_to_file(x_train,args.outdir,'train',outextention1)
    write_lines_to_file(y_train,args.outdir,'train',outextention2)
    write_lines_to_file(x_val,args.outdir,'valid',outextention1)
    write_lines_to_file(y_val,args.outdir,'valid',outextention2)
    write_lines_to_file(x_test,args.outdir,'test',outextention1)
    write_lines_to_file(y_test,args.outdir,'test',outextention2)



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", nargs='+', type=str)
    parser.add_argument("--dir", "-d", type=str, default=None)
    parser.add_argument("--outdir", "-o", type=str, default=None, help="Output directory")
    args = parser.parse_args()
    #args.filename = C:/Users/Lenovo/news-please-repo/data/data.txt
    #args.outdir = C:/Users/Lenovo/news-please-repo/data
    process_textfile(args, "output")
    #concat_text_files(args,'en','all_thai_parallel_data.en')
    #train_valid_test_split(args, 30000, 50000)


if __name__ == '__main__':
    main()