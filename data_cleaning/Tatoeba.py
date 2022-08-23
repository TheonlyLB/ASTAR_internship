


import regex as re
def clean(text):
    pattern = re.compile('.+?(?=1.)')
    text = re.sub(pattern, '', str(text))
    return text

with open("Tatoeba.en-th.en", "r", encoding= 'utf-8') as f:
    eng_list = []

    for line in f:
        stripped_line = line.strip()
        eng_list.append(stripped_line)

with open("Tatoeba.en-th.th", "r", encoding='utf-8') as f:
    th_list = []

    for line in f:
        stripped_line = line.strip()
        th_list.append(stripped_line)

result = list(zip(eng_list,th_list))

for tuple in result:
    if tuple[1] == '1. มันคือของขวัญ 2. พูดเมื่อเราทำอะไรที่คนอื่นทำไม่ได้ เพื่อที่จะเน้นว่า ฉันทำได้เพราะฉันมีความสามารถพิเศษที่ติดตัวมา':
        print(tuple[0])


