"""
PLACING ALL TEXT INTO 1 LINE THEN INSERTING NEWLINE CHAR AT ./!/?/) IS INEFFECTIVE SINCE THE PUNCTUATION OF ORIGINAL TEXT IS MESSY.
MOREOVER, THERE ARE NO ALTERNATIVES TO THE SITE USED TO DOWNLOAD TED SUBTITLES
"""
import regex as re
with open('TED_eng_1.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    pattern = re.compile('.!\)\]?')
    text = re.sub(pattern, "$0\n", text)
with open('TED_eng_2.txt', 'w', encoding='utf-8') as g:
    g.write(text)