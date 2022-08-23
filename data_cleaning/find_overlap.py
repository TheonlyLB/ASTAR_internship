"""
USE OS/GLOB WITH ARGPARSE TO SET ROOT FOLDER SO NO NEED TO HARDCODE FILE PATHS
CAUTION: DELETING COMMON LINES DESTROYS LINE ALIGNMENT FOR DATASETS W THAI EQUIVALENT
NOTE: SINCE INTERSECTION ONLY RETURNS UNIQUE ELEMENTS,
DUPLICATES OF COMMON LINES ARE NOT CONSIDERED IN CALCULATING PERCENTAGE OVERLAP

MEMORY ERROR:
1. INCREASE ALLOCATED MEMORY IN PYCHARM (done)
2. gc.collect() to clear unused variables (done)
3. generator functions

545,000KB is the limit for MemoryError
PYCHARM ALLOCATED MEMORY: 102400MB
EDIT CUSTOM VM OPTIONS:
-Xms512m
-Xmx102400m
-XX:ReservedCodeCacheSize=480m
"""
import pandas as pd
import gc
import openpyxl
filename_list = ["OpenSubtitles.txt",
                 "data_cleaned.txt",
                 "prachatai_test_text.txt",
                 "prachatai_test_title.txt",
                 "prachatai_train_text_000001.txt",
                 "prachatai_train_text_000002.txt",
                 "prachatai_train_title.txt",
                 "prachatai_validation_text.txt",
                 "prachatai_validation_title.txt",
                 "test_text.txt",
                 "test_title.txt",
                 "th_ (1).txt",
                 "th_ (2).txt",
                 "th_ (3).txt",
                 "th_ (4).txt",
                 "th_ (5).txt",
                 "th_ (6).txt",
                 "th_ (7).txt",
                 "th_ (8).txt",
                 "th_ (9).txt",
                 "th_ (10).txt",
                 "th_ (11).txt",
                 "th_ (12).txt",
                 "th_ (13).txt",
                 "th_ (14).txt",
                 "th_ (15).txt",
                 "th_ (16).txt",
                 "th_ (17).txt",
                 "th_ (18).txt",
                 "th_ (19).txt",
                 "th_ (20).txt",
                 "th_ (21).txt",
                 "th_ (22).txt",
                 "th_ (23).txt",
                 "th_ (24).txt",
                 "th_ (25).txt",
                 "th_ (26).txt",
                 "th_ (27).txt",
                 "th_ (28).txt",
                 "th_ (29).txt",
                 "th_ (30).txt",
                 "th_ (31).txt",
                 "th_ (32).txt",
                 "th_ (33).txt",
                 "th_ (34).txt",
                 "th_ (35).txt",
                 "th_ (36).txt",
                 "th_ (37).txt",
                 "th_ (38).txt",
                 "th_ (39).txt",
                 "th_ (40).txt",
                 "th_ (41).txt",
                 "th_ (42).txt",
                 "th_ (43).txt",
                 "th_ (44).txt",
                 "th_ (45).txt",
                 "th_ (46).txt",
                 "th_ (47).txt",
                 "th_ (48).txt",
                 "th_ (49).txt",
                 "th_ (50).txt",
                 "th_ (51).txt",
                 "th_ (52).txt",
                 "th_ (53).txt",
                 "th_ (54).txt",
                 "th_ (55).txt",
                 "th_ (56).txt",
                 "th_ (57).txt",
                 "th_ (58).txt",
                 "th_ (59).txt",
                 "th_ (60).txt",
                 "th_ (61).txt",
                 "th_ (62).txt",
                 "th_ (63).txt",
                 "th_ (64).txt",
                 "th_ (65).txt",
                 "th_ (66).txt",
                 "th_ (67).txt",
                 "th_ (68).txt",
                 "th_ (69).txt",
                 "th_ (70).txt",
                 "th_ (71).txt",
                 "th_ (72).txt",
                 "th_ (73).txt",
                 "th_ (74).txt",
                 "th_ (75).txt",
                 "th_ (76).txt",
                 "th_ (77).txt",
                 "th_ (78).txt",
                 "th_ (79).txt",
                 "th_ (80).txt",
                 "th_ (81).txt",
                 "th_ (82).txt",
                 "th_ (83).txt",
                 "th_ (84).txt",
                 "th_ (85).txt",
                 "th_ (86).txt",
                 "th_ (87).txt",
                 "th_ (88).txt",
                 "th_ (89).txt",
                 "th_ (90).txt",
                 "th_ (91).txt",
                 "th_ (92).txt",
                 "th_ (93).txt",
                 "th_ (94).txt",
                 "th_ (95).txt",
                 "th_ (96).txt",
                 "th_ (97).txt",
                 "th_ (98).txt",
                 "th_ (99).txt",
                 "th_ (100).txt",
                 "th_ (101).txt",
                 "th_ (102).txt",
                 "th_ (103).txt",
                 "th_ (104).txt",
                 "th_ (105).txt",
                 "th_ (106).txt",
                 "th_ (107).txt",
                 "th_ (108).txt",
                 "th_ (109).txt",
                 "th_ (110).txt",
                 "th_ (111).txt",
                 "th_ (112).txt",
                 "th_ (113).txt",
                 "th_ (114).txt",
                 "th_ (115).txt",
                 "th_ (116).txt",
                 "th_ (117).txt",
                 "th_ (118).txt",
                 "th_ (119).txt",
                 "th_ (120).txt",
                 "th_ (121).txt",
                 "th_ (122).txt",
                 "th_ (123).txt",
                 "th_ (124).txt",
                 "th_ (125).txt",
                 "th_ (126).txt",
                 "th_ (127).txt",
                 "th_ (128).txt",
                 "th_ (129).txt",
                 "th_ (130).txt",
                 "th_ (131).txt",
                 "th_ (132).txt",
                 "th_ (133).txt",
                 "th_ (134).txt",
                 "th_ (135).txt",
                 "th_ (136).txt",
                 "th_ (137).txt",
                 "th_ (138).txt",
                 "th_ (139).txt",
                 "th_ (140).txt",
                 "th_ (141).txt",
                 "th_ (142).txt",
                 "th_ (143).txt",
                 "th_ (144).txt",
                 "th_ (145).txt",
                 "th_ (146).txt",
                 "th_ (147).txt",
                 "th_ (148).txt",
                 "th_ (149).txt",
                 "th_ (150).txt",
                 "th_ (151).txt",
                 "th_ (152).txt",
                 "th_ (153).txt",
                 "th_ (154).txt",
                 "th_ (155).txt",
                 "th_ (156).txt",
                 "th_ (157).txt",
                 "th_ (158).txt",
                 "th_ (159).txt",
                 "thaisum_0_text_0.txt",
                 "thaisum_0_text_1.txt",
                 "thaisum_0_title.txt",
                 "thaisum_1_text_0.txt",
                 "thaisum_1_text_1.txt",
                 "thaisum_1_title.txt",
                 "thaisum_2_text_0.txt",
                 "thaisum_2_text_1.txt",
                 "thaisum_2_title.txt",
                 "thaisum_3_text.txt",
                 "thaisum_3_title.txt",
                 "thaiwikitext.txt",
                 "validation_text.txt",
                 "validation_title.txt",
                 "VISTEC_cleaned.txt",
                 "CCAligned_th_000001_2.txt",
                 "CCAligned_th_000002_2.txt",
                 "CCAligned_th_000003_2.txt",
                 "CCAligned_th_000004_2.txt",
                 "CCAligned_th_000005_2.txt",
                 "CCAligned_th_000006_2.txt",
                 "CCAligned_th_000007_2.txt",
                 "CCAligned_th_000008_2.txt",
                 "QED.en-th2.th",
                 "Tanzil.en-th.th",
                 "Tatoeba.en-th_cleaned.th",
                 "wikimedia.en-th2.th",
                 "XLEnt.en-th_cleaned.th"
                 ]
# Create DF
df = pd.DataFrame(columns = filename_list, index = filename_list)
#list() to edit list while iterating over it
for file1 in list(filename_list):
    # form set of all lines in file 1
    with open(file1, 'r', encoding='utf-8') as f:
        file1_lines = []
        for line in f:
            file1_lines.append(line.strip())
    # CONVERT TO SET
    file1_lines = set(file1_lines)
    # remove file1 from filename_list
    filename_list.remove(file1)
    i = 1

    # iterate through all previous files
    for file2 in filename_list:
        print('FILE ',i)
        # form set of all lines in file 2
        with open(file2,'r', encoding='utf-8') as g:
            file2_lines = []
            for line in g:
                file2_lines.append(line.strip())
        # CONVERT TO SET
        file2_lines = set(file2_lines)
        # if line in file 1 and file 2, print line/delete line from file 1
        common_lines = file1_lines.intersection(file2_lines)

        """
        num_of_common_lines = 0
        for line in list(file1_lines):
            if line in file2_lines:
                num_of_common_lines += 1
                print(line)
                
                # delete line from file 1
                file1_lines.remove(line)

        with open(file1,'w', encoding='utf-8') as f:
            for line in file1_lines:
                f.write(line)
                f.write('\n')
        """
        # find percentage overlap
        percentage_overlap_1 = len(common_lines)/len(file1_lines) * 100
        print(percentage_overlap_1,'%')
        # FILL CORRECT CELL
        df.at[file1,file2] = percentage_overlap_1

        # find percentage overlap
        percentage_overlap_2 = len(common_lines)/len(file2_lines) * 100
        print(percentage_overlap_2,'%')
        # FILL CORRECT CELL
        df.at[file2,file1] = percentage_overlap_2
        i+=1

    # add file1 to filename_list
    filename_list.append(file1)

    # clear memory
    del file1_lines
    del file2_lines
    del common_lines
    gc.collect()

# convert DF to excel
df.to_excel('file_percentage_overlap_th.xlsx')







