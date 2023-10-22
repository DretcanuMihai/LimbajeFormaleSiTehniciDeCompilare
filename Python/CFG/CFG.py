class CFG:
    @staticmethod
    def from_file(filename):
        with open(filename) as grammar_file:
            text = grammar_file.read()
            return CFG.from_text(text)

    @staticmethod
    def from_text(text):
        tokens = list(filter(lambda token: token != "", text.replace("\n", " ").replace("\t", " ").split(" ")))
        cfg = CFG()
        cfg.__parse_tokens(tokens)
        return cfg

    class Rule:
        def __init__(self, symbol, production):
            self.symbol = symbol
            self.production = production

        def __str__(self):
            output = self.symbol + " -> "
            for token in self.production:
                output += token + " "
            return output

    @staticmethod
    def __list_to_rule(rule):
        return CFG.Rule(rule[0], rule[1])

    def __parse_tokens(self, tokens):
        rule = []
        for token in tokens:
            if (token == "|" or token == ";") and len(rule) != 2:
                raise Exception("Invalid Input File")
            elif len(rule) == 0:
                rule.append(token)
                if token not in self.non_terminals:
                    self.non_terminals.append(token)
                    if token in self.terminals:
                        self.terminals.remove(token)
            elif len(rule) == 1:
                if token != ":":
                    raise Exception("Invalid Input File")
                rule.append([])
            elif token == "|":
                self.rules.append(CFG.__list_to_rule(rule))
                rule = [rule[0], []]
            elif token == ";":
                self.rules.append(CFG.__list_to_rule(rule))
                rule = []
            else:
                rule[1].append(token)
                if token not in self.non_terminals and token not in self.terminals:
                    self.terminals.append(token)
        if len(rule) != 0:
            raise Exception("Invalid Input File")

    def __init__(self):
        self.non_terminals = list()
        self.terminals = list()
        self.rules = list()

    def get_start(self):
        return self.rules[0].symbol

    def __str__(self):
        output = "Context Free Grammar\n"
        output += "\t" + "Terminals:\n"
        for terminal in self.terminals:
            output += "\t" + "\t" + terminal + "\n"

        output += "\t" + "Non-Terminals:\n"
        for non_terminal in self.non_terminals:
            output += "\t" + "\t" + non_terminal + "\n"

        output += "\t" + "Rules:\n"
        for rule, index in zip(self.rules, range(len(self.rules))):
            output += "\t" + "\t" + "(" + str(index) + ")" + "\t" + str(rule)
            output += "\n"

        return output
