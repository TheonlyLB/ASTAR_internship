'''
remove:
blank lines - done
duplicates - done
lines w no translation - done
thai line has no thai - done
eng line has no eng - done
eng line w thai - done
lines 3x longer than their translation - done
remove unmatched brackets - done
check line alignment
'''


import regex as re
def clean_eng(text):
    # has thai
    pattern = re.compile('[\u0E00-\u0E7F]')
    if pattern.search(text):
        text = ''
    # remove non-eng
    pattern = re.compile('^(?!.*[\u0000-\u05C0\u2100-\u214F].*).+$')
    text = re.sub(pattern, '', str(text))
    # remove emojis
    pattern = re.compile('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
    text = re.sub(pattern, '', str(text))
    # remove blank spaces
    pattern = re.compile('\s*')
    text = re.sub(pattern, '', str(text))

    return text

def clean_th(text):
    # remove non-thai
    pattern = re.compile('^(?!.*[\u0E00-\u0E7F].*).+$')
    text = re.sub(pattern, '', str(text))
    # remove emojis
    pattern = re.compile('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
    text = re.sub(pattern, '', str(text))
    # remove blank spaces
    pattern = re.compile('\s*')
    text = re.sub(pattern, '', str(text))

    return text
#wikimedia.en-th.en
with open("CCAligned_en_000008.txt", "r", encoding= 'utf-8') as f:
    eng_list = []
    for line in f:
        # removes unmatched brackets
        # You cannot find unmatched parentheses with regex
        st = []
        for char in line:
            # if opening bracket then push into stack
            if char == '(':
                st.append(char)
            # if char is closing bracket ')'
            elif char == ')':
                # If this closing bracket is unmatched
                if len(st) == 0:
                    # Note: cannot remove char in str while iterating over it
                    line = line.replace(')','sushikia',1)
                else:
                    # replace all opening and closing brackets
                    line = line.replace(')', "hurzhen", 1)
                    line = line.replace('(', "zonliew", 1)
                    # remove 1 from stack
                    st.pop()
        # if stack is not empty then remove opening bracket and pop out all elements
        while len(st) != 0:
            line = line.replace('(','sushikia',1)
            st.pop()
        line = line.replace('zonliew','(')
        line = line.replace('hurzhen',')')
        # remove unmatched parentheses
        line = line.replace('sushikia','')

        stripped_line = line.strip()
        eng_list.append(stripped_line)

with open("CCAligned_th_000008.txt", "r", encoding='utf-8') as f:
    th_list = []

    for line in f:
        # You cannot find unmatched parentheses with regex
        st = []
        for char in line:
            # if opening bracket then push into stack
            if char == '(':
                st.append(char)
            # if char is closing bracket ')'
            elif char == ')':
                # If this closing bracket is unmatched
                if len(st) == 0:
                    # Note: cannot remove char in str while iterating over it
                    line = line.replace(')','sushikia',1)
                else:
                    # replace all opening and closing brackets
                    line = line.replace(')', "hurzhen", 1)
                    line = line.replace('(', "zonliew", 1)
                    # remove 1 from stack
                    st.pop()
        # if stack is not empty then remove opening bracket and pop out all elements
        while len(st) != 0:
            line = line.replace('(','sushikia',1)
            st.pop()
        line = line.replace('zonliew','(')
        line = line.replace('hurzhen',')')
        # remove unmatched parentheses
        line = line.replace('sushikia','')

        stripped_line = line.strip()
        th_list.append(stripped_line)

result = list(zip(eng_list,th_list))
# cannot remove from list while iterating through it
i = 0



#list(result) creates a copy
tuples_seen = set()
for tuple in list(result):
    if clean_eng(tuple[0]) == '' or clean_th(tuple[1]) == '' or len(tuple[0])/len(tuple[1]) >=3 or len(tuple[0])/len(tuple[1]) <= 1/3:
        result.remove(tuple)
    # remove duplicate tuples
    elif tuple in tuples_seen:
        result.remove(tuple)
    else:
        tuples_seen.add(tuple)
    i+=1
    print('a%d'%i)



list_of_lists = [[i for i, j in result], [j for i, j in result]]
eng_list = list_of_lists[0]
th_list = list_of_lists[1]

with open("CCAligned_en_000008_2.txt", "a", encoding= 'utf-8') as f:
    i = 0
    for items in eng_list:
        f.write('%s\n' %items)
        i+=1
        print('b%d'% i)

with open("CCAligned_th_000008_2.txt", "a", encoding= 'utf-8') as f:
    i = 0
    for items in th_list:
        f.write('%s\n' %items)
        i+=1
        print('c%d'%i)