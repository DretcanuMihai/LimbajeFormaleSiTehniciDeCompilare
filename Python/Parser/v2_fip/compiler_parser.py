import re
from TS import TS
from FIP import FIP

CONST_STRING = "CONST"
ID_STRING = "ID"
KEYWORD_STRING = "KEYWORD"
OPERATOR_STRING = "OPERATOR"
SEPARATOR_STRING = "SEPARATOR"

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

ENCODINGS = dict({ID_STRING: 0, CONST_STRING: 1}, **KEYWORDS, **OPERATORS, **SEPARATORS)


def preprocessing_format(text):
    text = text.replace("\n", " \n ")
    text = text.replace("\t", " ") \
        .replace("\"", " \" ")
    for separator in SEPARATORS:
        text = text.replace(separator, " " + separator + " ")
    return text


def is_id(text):
    return len(text) < 250 and re.search("^[a-zA-Z]+([.][a-zA-Z]+)?$", text) is not None


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
        return KEYWORD_STRING
    if atom in OPERATORS:
        return OPERATOR_STRING
    if atom in SEPARATORS:
        return SEPARATOR_STRING
    if is_id(atom):
        return ID_STRING
    if is_const(atom):
        return CONST_STRING
    raise Exception("Can't identify nature of:\n" + atom)


def convert_buffer(buffer):
    quoted_atom = "\""
    for elem in buffer[:-1]:
        quoted_atom += elem + " "
    quoted_atom += buffer[-1] + "\""
    return quoted_atom


def parse(text):
    text = preprocessing_format(text)
    text_array = text.split(" ")

    ts = TS()
    fip = FIP()

    def classify_and_treat_atom(atom_val):
        atom_class = classify_atom(atom_val)
        if atom_class == ID_STRING:
            index = ts.get_index(atom_val)
            fip.insert_atom(ENCODINGS.get(ID_STRING), index)
        elif atom_class == CONST_STRING:
            index = ts.get_index(atom_val)
            fip.insert_atom(ENCODINGS.get(CONST_STRING), index)
        else:
            fip.insert_atom(ENCODINGS.get(atom_val))

    line = 1
    buffer = []
    is_inside_quotes = False
    try:
        for atom in text_array:
            if not is_inside_quotes:
                if atom == "\n":
                    line += 1
                    continue
                elif atom == "":
                    continue
                elif atom == "\"":
                    is_inside_quotes = True
                else:
                    classify_and_treat_atom(atom)
            else:
                if atom == "\n":
                    raise Exception("Unterminated string:\n" + convert_buffer(buffer))
                elif atom != "\"":
                    buffer.append(atom)
                else:
                    quoted_atom = convert_buffer(buffer)
                    classify_and_treat_atom(quoted_atom)
                    buffer = []
                    is_inside_quotes = False
        if is_inside_quotes:
            raise Exception("Unterminated string:\n" + convert_buffer(buffer))
    except Exception as e:
        message = "Error at line " + str(line) + "\n"
        # message += str(e)
        raise Exception(message)
    return ts, fip
