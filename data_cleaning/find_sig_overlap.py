import pandas as pd

df = pd.read_excel('file_percentage_overlap_en.xlsx')
print(df.head, '\n')
filepair_list = []
for rowIndex, row in df.iterrows(): #iterate over rows
    for columnIndex, value in row.items():
        try:
            if value >= 5:
                filepair_tuple = (str(value), ' row: ',str(row[0]),' column: ',str(columnIndex))
                filepair_list.append(filepair_tuple)
        except TypeError:
            continue
filepair_list.sort(reverse=True)
for i in filepair_list:
    str = ''.join(i)
    print(str)

