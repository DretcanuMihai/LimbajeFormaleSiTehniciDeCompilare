import re

KEYWORDS = {
    "#include": 2,
    "<iostream>": 3,
    "using": 4,
    "namespace": 5,
    "std": 6,
    "int": 7,
    "main": 8,
    "return": 9,
    "while": 10,
    "struct": 11,
    "bool": 12,
    "double": 13,
    "cout": 14,
    "cin": 15,
    "if": 16
}

OPERATORS = {
    "<<": 17,
    "=": 18,
    "!": 19,
    "+": 20,
    "-": 21,
    "*": 22,
    "/": 23,
    "%": 24,
    "&&": 25,
    "||": 26,
    "<": 27,
    ">": 28,
    "!=": 29,
    "==": 30,
    ">>": 31
}

SEPARATORS = {
    "(": 32,
    ")": 33,
    "{": 34,
    "}": 35,
    ";": 36
}

CONST_STRING = "CONST"
ID_STRING = "ID"
KEYWORD_STRING = "KEYWORD"
OPERATOR_STRING = "OPERATOR"
SEPARATOR_STRING = "SEPARATOR"


def preprocessing_format(text):
    text = text.replace("\n", " ") \
        .replace("\t", " ") \
        .replace("\"", " \" ")
    for separator in SEPARATORS:
        text = text.replace(separator, " " + separator + " ")
    return text


def is_id(text):
    return re.search("^[a-zA-Z]+([.][a-zA-Z]+)?$", text) is not None


def is_bool(text):
    return text == "true" or text == "false"


def is_int(text):
    return text == "0" or \
           re.search("^[+-]?[1-9][0-9]{0,4}$", text) is not None


def is_double(text):
    return re.search("^[+-]?[1-9][0-9]{0,4}[.][0-9]{1,5}$", text) is not None \
           or re.search("^[+-]?0[.][0-9]{1,5}$", text) is not None


def is_text(text):
    if len(text) < 2 or text[0] != "\"" or text[-1] != "\"":
        return False
    text = text[1:-1]
    return text == "\\n" or re.search("^[:a-zA-Z0-9 ]+$", text) is not None


def is_const(text):
    return is_bool(text) \
           or is_int(text) \
           or is_double(text) \
           or is_text(text)


def classify_atom(atom):
    if atom in KEYWORDS:
        atom_class = KEYWORD_STRING
    elif atom in OPERATORS:
        atom_class = OPERATOR_STRING
    elif atom in SEPARATORS:
        atom_class = SEPARATOR_STRING
    elif is_id(atom):
        atom_class = ID_STRING
    elif is_const(atom):
        atom_class = CONST_STRING
    else:
        raise Exception("Error: can't identify nature of:\n" + atom)
    return atom, atom_class


def parse(text):
    result = []
    text = preprocessing_format(text)
    text_array = text.split(" ")
    buffer = []
    is_inside_quotes = False
    for atom in text_array:
        if not is_inside_quotes:
            if atom == "":
                continue
            elif atom == "\"":
                is_inside_quotes = True
            else:
                result.append(classify_atom(atom))
        else:
            if atom != "\"":
                buffer.append(atom)
            else:
                quoted_atom = "\""
                for elem in buffer[:-1]:
                    quoted_atom += elem + " "
                quoted_atom += buffer[-1] + "\""
                result.append(classify_atom(quoted_atom))
                buffer = []
                is_inside_quotes = False
    if len(buffer) != 0:
        raise Exception("Error: unterminated string:\n" + str(buffer))
    return result
