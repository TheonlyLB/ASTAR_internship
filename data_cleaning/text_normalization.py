#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TEXTACY IN PYCHARM DIFFERS FROM TEXTACY FOR COMMAND LINE
import re
import textacy.preprocessing as tnorm

def _replace_urls(text):
    """
    strip urls and replace with <URL> token
    AttributeError: module 'textacy.preprocessing.replace' has no attribute 'urls'

    """
    corrected = str(text)
    #url_regex = r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'
    #corrected = re.sub(url_regex, "<URL>", corrected)
    corrected = tnorm.replace.urls(corrected, repl="<URL>")
    return corrected

def _simplify_punctuation(text):
    """
    This function simplifies doubled or more complex punctuation. The exception is '...'.
    """
    corrected = str(text)
    corrected = re.sub(r'([!?,;:])\1+', r'\1', corrected)
    corrected = re.sub(r'\.{2,}', r'...', corrected)
    return corrected

def _normalize_whitespace(text):
    """
    This function normalizes whitespaces, removing duplicates.
    """
    corrected = str(text)
    corrected = re.sub(u'\xa0', u' ', corrected)
    corrected = re.sub(r"//t",r"\t", corrected)
    corrected = re.sub(r"( )\1+",r"\1", corrected)
    corrected = re.sub(r"(\n)\1+",r"\1", corrected)
    corrected = re.sub(r"(\r)\1+",r"\1", corrected)
    corrected = re.sub(r"(\t)\1+",r"\1", corrected)
    corrected = ''.join(corrected.splitlines()) #remove linebreaks in middle of line
    return corrected.strip(" ")

def _normalize_quotation(text):
    """
    replace fancy quotation marks with ascii equivalents
    """
    return tnorm.normalize.quotation_marks(text)

def _remove_comma_in_numbers(text):
    """
    2,500 -> 2500
    """
    corrected = str(text)
    corrected = re.sub('(?<=\d),(?=\d)', '', corrected)
    return corrected

def _remove_eol_tag(text):
    """
    remove </eol> or <eol> tags in text
    """
    corrected = str(text)
    corrected  = re.sub(r'</eol>|<eol>', '', corrected)
    return corrected

def _remove_start_end_square_brackets(text):
    """remove square bracket/parentheses if it spans the entire line.
    This occurs in some subtitles dataset
    IndexError: string index out of range
    """
    corrected = str(text)
    corrected = re.sub(r'[\[\]]', '', corrected)
    if corrected[0] == "(" and corrected[-1] == ")":
    #print(corrected)
        corrected = corrected.strip('()') #re.sub(r'[()]', '', corrected)
    #print(corrected)
    #corrected = re.sub(r'/^\[(.+)\]$/','$1', corrected)
    return corrected

def _normalize_bullet_points(text):
    """standardize bullet points"""
    return tnorm.normalize.bullet_points(text)

def _remove_text_before_tab(text):
    """used for asian language treebank dataset to remove a part of text"""
    corrected = str(text)
    corrected = re.sub(r'^.*?\t', '', corrected)
    return corrected

def _remove_consecutive_punctuation(text):
    # remove consecutive punctuation
    pattern = re.compile('([-/\\\\()!"+=_#*@$%,&\'.-]{2,})')
    corrected = re.sub(pattern, '', str(text))
    return corrected

def _remove_control_codes(text):
    pattern = re.compile('(?!\r|\n|\t)[\x80-\x9f]')
    corrected = re.sub(pattern, '', str(text))
    return corrected

def _remove_blank_lines(text):
    # Different regex needed for different line endings. Can use Notepad++ built-in function: Edit > Line Operations> Remove Blank Lines
    pattern = re.compile('^(?:[\t ]*(?:\r?\n|\r))+')
    corrected = re.sub(pattern, '', str(text))
    return corrected

def _remove_nonthai_lines(text):
    pattern = re.compile('^(?!.*[\u0E00-\u0E7F].*).+$')
    corrected = re.sub(pattern, '', str(text))
    return corrected

def _remove_emoticons(text):
    pattern = re.compile('(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])')
    corrected = re.sub(pattern, '', str(text))
    return corrected



def compose_processing(text):
    #text = _remove_text_before_tab(text)
    text = _replace_urls(text)
    text = _remove_eol_tag(text)
    text = _simplify_punctuation(text)
    text = _normalize_quotation(text)
    text = _remove_comma_in_numbers(text)
    # text = _remove_start_end_square_brackets(text)
    text = _normalize_bullet_points(text)
    text = _normalize_whitespace(text)
    text = _remove_consecutive_punctuation(text)
    #text = _remove_control_codes(text)
    # text = _remove_nonthai_lines(text)
    #text = _remove_emoticons(text)
    text = _remove_blank_lines(text)
    return text

"""
write list into txt file, 1 element per line
"""

