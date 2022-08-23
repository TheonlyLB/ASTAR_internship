

import regex as re
def clean(text):
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
#XLEnt.en-th.en
with open("XLEnt.en-th.en", "r", encoding= 'utf-8') as f:
    eng_list = []

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
        eng_list.append(stripped_line)

with open("XLEnt.en-th.th", "r", encoding='utf-8') as f:
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
for tuple in list(result):
    if clean(tuple[1]) == '' or len(tuple[0])/len(tuple[1]) >=3 or len(tuple[0])/len(tuple[1]) <= 1/3:
        result.remove(tuple)
    i+=1
    print('a%d'%i)



list_of_lists = [[i for i, j in result], [j for i, j in result]]
eng_list = list_of_lists[0]
th_list = list_of_lists[1]

with open("XLEnt.en-th2.en", "a", encoding= 'utf-8') as f:
    i = 0
    for items in eng_list:
        f.write('%s\n' %items)
        i+=1
        print('b%d'% i)

with open("XLEnt.en-th2.th", "a", encoding= 'utf-8') as f:
    i = 0
    for items in th_list:
        f.write('%s\n' %items)
        i+=1
        print('c%d'%i)