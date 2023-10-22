from AF import AF_ID, AF_INT, AF_DOUBLE, AF_TEXT, AF_BOOL
from TS import TS
from FIP import FIP

CONST_STRING = "CONST"
ID_STRING = "ID"
KEYWORD_STRING = "KEYWORD"
OPERATOR_STRING = "OPERATOR"
SEPARATOR_STRING = "SEPARATOR"

KEYWORDS = {
    "#include": 2,
    "iostream": 3,
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
    ">>": 18,
    "!=": 19,
    "==": 20,
    "&&": 21,
    "||": 22,
    "+": 23,
    "-": 24,
    "*": 25,
    "/": 26,
    "%": 27,
    "<": 28,
    ">": 29,
    "=": 30,
    "!": 31,
}

SEPARATORS = {
    "(": 32,
    ")": 33,
    "{": 34,
    "}": 35,
    ";": 36
}

ENCODINGS = dict(**KEYWORDS, **OPERATORS, **SEPARATORS)
ENCODINGS_FULL = dict({ID_STRING: 0, CONST_STRING: 1}, **ENCODINGS)

FILTERS = sorted(ENCODINGS.keys(), key=len, reverse=True)
TEXTUAL_SEPARATORS = list(dict(**OPERATORS, **SEPARATORS, **{" ": -1, "\n": -1, "\t": -1}).keys())


def parse(text):
    ts = TS()
    fip = FIP()
    line = 1

    def treat_atom(atom_val, atom_class):
        if atom_class == ID_STRING:
            index = ts.get_index(atom_val)
            fip.insert_atom(ENCODINGS_FULL.get(ID_STRING), index)
        elif atom_class == CONST_STRING:
            index = ts.get_index(atom_val)
            fip.insert_atom(ENCODINGS_FULL.get(CONST_STRING), index)
        else:
            fip.insert_atom(ENCODINGS_FULL.get(atom_val))

    def apply_AF(text_to_check, my_AF, tag):
        longest = my_AF.find_longest_accepted_prefix(text_to_check)
        if longest is not None:
            remaining_text = shorten(text_to_check, longest)
            if len(remaining_text) == 0 or remaining_text[0] in TEXTUAL_SEPARATORS:
                treat_atom(longest, tag)
            else:
                longest = None
                remaining_text = text_to_check
        else:
            remaining_text = text_to_check
        return longest, remaining_text

    def shorten(text, ot_text):
        return text[len(ot_text):]

    try:
        while len(text) != 0:
            if text[0] == "\n" or text[0] == "\t" or text[0] == " ":
                if text[0] == "\n":
                    line += 1
                text = shorten(text, text[0])
                continue

            advance = False

            for keyword in FILTERS:
                if text.startswith(keyword):
                    if keyword in SEPARATORS:
                        advance = True
                        treat_atom(keyword, SEPARATOR_STRING)
                        text = shorten(text, keyword)
                        break
                    elif keyword in OPERATORS:
                        # if keyword in ["+", "-"]:
                        #     current_state = fip.get_as_list()
                        #     if len(current_state) == 0 or current_state[-1].atom_code not in [0, 1]:
                        #         break
                        advance = True
                        treat_atom(keyword, OPERATOR_STRING)
                        text = shorten(text, keyword)
                        break
                    else:
                        text_aux = shorten(text, keyword)
                        if len(text_aux) == 0 or \
                                (text_aux[0] in SEPARATORS or text_aux[0] in OPERATORS or text_aux[0] in [" ", "\t",
                                                                                                          "\n"]):
                            advance = True
                            treat_atom(keyword, KEYWORD_STRING)
                            text = text_aux
            if advance:
                continue

            word, text = apply_AF(text, AF_BOOL, CONST_STRING)
            if word is not None:
                continue

            word, text = apply_AF(text, AF_ID, ID_STRING)
            if word is not None:
                if len(word) > 250:
                    raise Exception("Id has to be less than 250 characters long:\n" + text[0])
                continue

            word, text = apply_AF(text, AF_DOUBLE, CONST_STRING)
            if word is not None:
                continue

            word, text = apply_AF(text, AF_INT, CONST_STRING)
            if word is not None:
                continue

            word, text = apply_AF(text, AF_TEXT, CONST_STRING)
            if word is not None:
                continue

            raise Exception("Can't find nature of atom")

    except Exception as e:
        message = "Error at line " + str(line)
        # message = "Error at line " + str(line) + ":" + "\n"
        # message += str(e)
        raise Exception(message)
    return ts, fip
