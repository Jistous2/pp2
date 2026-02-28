#RegEx Introduction
#RegEx Syntax and Metacharacters (., *, +, ?, ^, $, [], |, (), \)
#Special Sequences (\d, \w, \s, \D, \W, \S, \A, \Z)
#Sets and Character Classes
#Quantifiers ({n}, {n,}, {n,m})
#re.search() - Find first match
#re.findall() - Find all matches
#re.split() - Split strings
#re.sub() - Replace patterns
#re.match() - Match at beginning
#Flags (re.IGNORECASE, re.MULTILINE, etc.)


                            #REGULAR EXPRESSIONS (RegEx) IN PYTHON

import re

print("=== BASIC SEARCH ===")
text = "My phone is 87071234567"
result = re.search(r"\d+", text)
print(result.group())  # 87071234567


                                #MetaCharacters
                                """
                                .   - любой символ кроме новой строки
                                *   - 0 или более повторений
                                +   - 1 или более повторений
                                ?   - 0 или 1 повтор
                                ^   - начало строки
                                $   - конец строки
                                []  - набор символов
                                |   - логическое ИЛИ
                                ()  - группировка
                                \   - экранирование
                                """

print("\n=== DOT (.) ===")
print(re.findall(r"a.c", "abc axc a9c"))  # ['abc', 'axc', 'a9c']

print("\n=== STAR (*) ===")
print(re.findall(r"ab*", "a ab abb abbb"))  # ['a', 'ab', 'abb', 'abbb']

print("\n=== PLUS (+) ===")
print(re.findall(r"ab+", "a ab abb abbb"))  # ['ab', 'abb', 'abbb']

print("\n=== QUESTION (?) ===")
print(re.findall(r"colou?r", "color colour"))  # ['color', 'colour']

print("\n=== START (^) and END ($) ===")
print(re.findall(r"^Hello", "Hello world"))
print(re.findall(r"world$", "Hello world"))

print("\n=== SETS [] ===")
print(re.findall(r"[aeiou]", "hello world"))
print(re.findall(r"[0-9]", "a1b2c3"))

print("\n=== OR (|) ===")
print(re.findall(r"cat|dog", "cat dog mouse"))

print("\n=== GROUPING () ===")
match = re.search(r"(\d{3})-(\d{2})", "123-45")
print(match.group(1))  # 123
print(match.group(2))  # 45

print("\n=== ESCAPING (\\) ===")
print(re.findall(r"\.", "file.txt"))  # ['.']


                                    #Sequences
                                    """
                                    \d  - цифра
                                    \D  - не цифра
                                    \w  - буква, цифра, _
                                    \W  - не буква/цифра
                                    \s  - пробел
                                    \S  - не пробел
                                    \A  - начало всей строки
                                    \Z  - конец всей строки
                                    """

print("\n=== SPECIAL SEQUENCES ===")
print(re.findall(r"\d", "abc123"))  # ['1', '2', '3']
print(re.findall(r"\w+", "Hello_123"))
print(re.findall(r"\s", "a b c"))


#Classes
print("\n=== LETTERS ONLY ===")
print(re.findall(r"[A-Za-z]", "Hello123"))

print("\n=== NEGATION [^] ===")
print(re.findall(r"[^0-9]", "abc123"))


                                    #Quantifiers
"""
{n}     - ровно n
{n,}    - минимум n
{n,m}   - от n до m
"""

print("\n=== {n} ===")
print(re.findall(r"\d{3}", "123 45 6789"))

print("\n=== {n,} ===")
print(re.findall(r"\d{2,}", "1 22 333 4444"))

print("\n=== {n,m} ===")
print(re.findall(r"\d{2,4}", "1 22 333 44444"))


                                    #Functions
print("\n=== re.search() ===")
res = re.search(r"\d+", "abc123xyz456")
print(res.group())  # 123

print("\n=== re.findall() ===")
print(re.findall(r"\d+", "abc123xyz456"))  # ['123', '456']

print("\n=== re.split() ===")
print(re.split(r"\s+", "Hello   world  Python"))

print("\n=== re.sub() ===")
print(re.sub(r"\d+", "NUMBER", "abc123xyz456"))

print("\n=== re.match() ===")
print(re.match(r"\d+", "123abc"))  # match object
print(re.match(r"\d+", "abc123"))  # None


                            #Flags
                            #re.IGNORECASE  - игнорировать регистр
                            #re.MULTILINE   - ^ и $ работают построчно
                            #re.DOTALL      - . включает \n

print("\n=== IGNORECASE ===")
print(re.findall(r"hello", "Hello HELLO", re.IGNORECASE))

print("\n=== MULTILINE ===")
multi_text = "Hello\nWorld"
print(re.findall(r"^World", multi_text, re.MULTILINE))


                                    #Email validation
pattern = r"^[\w.-]+@[\w.-]+\.\w+$"
email = "test@mail.com"

if re.match(pattern, email):
    print("Valid email")
else:
    print("Invalid email")
