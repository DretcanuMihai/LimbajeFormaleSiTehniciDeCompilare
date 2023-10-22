from CFG import CFG


class LR1Analyzer:
    new_start = ":start:"
    sentence_end = ":$:"
    dot = ":.:"

    @staticmethod
    def for_cfg(cfg):
        analyzer = LR1Analyzer()
        analyzer.cfg = cfg
        analyzer.__enrich_grammar()
        analyzer.__build_first1()
        analyzer.__build_states()
        analyzer.__build_table()
        return analyzer

    def __init__(self):
        self.cfg = None
        self.first1 = dict()
        self.states = list()
        self.table = list()

    def __enrich_grammar(self):
        self.cfg.non_terminals.insert(0, LR1Analyzer.new_start)
        self.cfg.terminals.append(LR1Analyzer.sentence_end)
        self.cfg.rules.insert(0, CFG.Rule(LR1Analyzer.new_start, [self.cfg.get_start()]))

    def __build_first1(self):
        cfg = self.cfg
        self.__initialize_first1()

        while True:
            next_first1 = dict()
            for non_terminal in cfg.non_terminals:
                next_first1[non_terminal] = list()

            for rule in cfg.rules:
                symbol, production = rule.symbol, rule.production
                production_first1 = self.__get_first1_of_sequence(production)
                for production_first1_elem in production_first1:
                    if production_first1_elem not in next_first1[symbol]:
                        next_first1[symbol].append(production_first1_elem)

            self.__add_terminals_to_first1(next_first1)
            if self.first1 == next_first1:
                break
            self.first1 = next_first1

    def __initialize_first1(self):
        cfg = self.cfg
        for non_terminal in cfg.non_terminals:
            self.first1[non_terminal] = list()
        for rule in cfg.rules:
            symbol, production = rule.symbol, rule.production
            prefix = production[0:1]
            if len(prefix) != 0 and prefix[0] in cfg.non_terminals:
                continue
            if prefix not in self.first1[symbol]:
                self.first1[symbol].append(prefix)

        self.__add_terminals_to_first1(self.first1)

    def __add_terminals_to_first1(self, first1):
        cfg = self.cfg
        for terminal in cfg.terminals:
            first1[terminal] = list()
            first1[terminal].append([terminal])

    def __get_first1_of_sequence(self, sequence):
        output = list()
        has_epsilon = True
        for token in sequence:
            has_epsilon = False
            for first1_element in self.first1[token]:
                if len(first1_element) == 0:
                    has_epsilon = True
                elif first1_element not in output:
                    output.append(first1_element)
            if not has_epsilon:
                break
        if has_epsilon:
            output.append([])
        return output

    class LR1Rule:
        def __init__(self, cfg, rule_index, dot_index, following):
            self.cfg = cfg
            self.rule_index = rule_index
            self.dot_index = dot_index
            self.following = following

        def get_after_dot(self):
            rule = self.cfg.rules[self.rule_index]
            return rule.production[self.dot_index:]

        def get_rule(self):
            return self.cfg.rules[self.rule_index]

        def __str__(self):
            output = "(" + str(self.rule_index) + ")" + "\t"
            rule = self.cfg.rules[self.rule_index]
            output += str(rule.symbol) + " -> "
            for token in rule.production[:self.dot_index]:
                output += token + " "
            output += LR1Analyzer.dot + " "
            for token in rule.production[self.dot_index:]:
                output += token + " "
            output += "| following = " + str(self.following)
            return output

        def __hash__(self):
            return hash(self.rule_index) ^ hash(self.dot_index) ^ hash(self.following)

        def __eq__(self, other):
            if not isinstance(other, LR1Analyzer.LR1Rule):
                return False
            return other.rule_index == self.rule_index \
                   and other.dot_index == self.dot_index \
                   and other.following == self.following

    def __build_states(self):
        state_queue = [self.__get_initial_first_state()]
        while len(state_queue) != 0:
            state = state_queue.pop(0)
            self.states.append(state)

            for lr1rule in state:
                prod_af_dot = lr1rule.get_after_dot()
                if len(prod_af_dot) == 0:
                    continue
                symbol = prod_af_dot[0]

                new_state = self.__get_goto(state, symbol)
                if len(new_state) == 0:
                    continue

                if self.__get_state_index(new_state) != -1:
                    continue
                state_queue.append(new_state)

    def __get_initial_first_state(self):
        cfg = self.cfg
        initial_state = [LR1Analyzer.LR1Rule(cfg,
                                             0,
                                             0,
                                             LR1Analyzer.sentence_end
                                             )]
        self.__apply_closure(initial_state)
        return initial_state

    def __apply_closure(self, state):
        cfg = self.cfg

        rule_queue = []
        for rule in state:
            rule_queue.append(rule)

        while len(rule_queue) != 0:
            rule = rule_queue.pop(0)

            production_af_dot = rule.get_after_dot()
            if len(production_af_dot) == 0:
                continue
            first_symbol_after_dot = production_af_dot[0]
            if first_symbol_after_dot not in cfg.non_terminals:
                continue

            production_af_nt_w_following = production_af_dot[1:]
            production_af_nt_w_following.append(rule.following)
            following_values = self.__get_first1_of_sequence(production_af_nt_w_following)

            for cfg_rule_index in range(len(cfg.rules)):
                following_rule = cfg.rules[cfg_rule_index]
                if following_rule.symbol != first_symbol_after_dot:
                    continue
                for following_symbol in following_values:
                    new_rule = LR1Analyzer.LR1Rule(cfg,
                                                   cfg_rule_index,
                                                   0,
                                                   following_symbol[0]
                                                   )
                    if new_rule not in state:
                        state.append(new_rule)
                        rule_queue.append(new_rule)

    def __get_goto(self, state, symbol):
        cfg = self.cfg

        new_state = []
        for lr1rule in state:
            prod_af_dot = lr1rule.get_after_dot()
            if len(prod_af_dot) == 0:
                continue
            if prod_af_dot[0] == symbol:
                new_state.append(LR1Analyzer.LR1Rule(
                    cfg,
                    lr1rule.rule_index,
                    lr1rule.dot_index + 1,
                    lr1rule.following
                ))
        self.__apply_closure(new_state)
        return new_state

    def __get_state_index(self, state):
        for index in range(len(self.states)):
            if set(state) == set(self.states[index]):
                return index
        return -1

    # shift, reduce, accept, error
    class Action:
        def __init__(self, action_type, action_info=None):
            self.action_type = action_type
            self.action_info = action_info

        def __str__(self):
            output = ""
            output += self.action_type
            if self.action_info is not None:
                output += "-" + str(self.action_info)
            return output

        def __eq__(self, other):
            if not isinstance(other, LR1Analyzer.Action):
                return False
            return other.action_type == self.action_type \
                   and other.action_info == self.action_info

    def __build_table(self):
        states = self.states

        for state_index in range(len(states)):
            state = states[state_index]
            row = dict()

            for lr1rule in state:
                rule = lr1rule.get_rule()
                prod_af_dot = lr1rule.get_after_dot()

                if len(prod_af_dot) != 0:
                    symbol_af_dot = prod_af_dot[0]
                    state_goto = self.__get_goto(state, symbol_af_dot)
                    key_symbol = symbol_af_dot
                    cell_value = LR1Analyzer.Action("shift", self.__get_state_index(state_goto))
                elif rule.symbol != LR1Analyzer.new_start:
                    key_symbol = lr1rule.following
                    cell_value = LR1Analyzer.Action("reduce", lr1rule.rule_index)
                else:
                    key_symbol = LR1Analyzer.sentence_end
                    cell_value = LR1Analyzer.Action("accept")

                if key_symbol in row.keys() and row[key_symbol] != cell_value:
                    raise Exception("Grammar isn't LR(1) compatible")
                row[key_symbol] = cell_value

            self.table.append(row)

    def check_sequence(self, sequence, logging_enabled=True):
        cfg = self.cfg
        table = self.table

        for elem in sequence:
            if elem not in cfg.terminals:
                raise Exception("Unknown symbol in sequence")

        logging_info = [logging_enabled, 0]
        work_stack, input_queue, output_queue = LR1Analyzer.__get_initial_automata(sequence)
        while True:
            LR1Analyzer.__log_automata(logging_info, work_stack, input_queue, output_queue)
            action = table[work_stack[-1]].get(input_queue[0]) or LR1Analyzer.Action("error")
            LR1Analyzer.__log_action(logging_info, action)
            if action.action_type == "accept":
                LR1Analyzer.__log_accept_output(logging_info, output_queue)
                return True
            elif action.action_type == "error":
                return False
            elif action.action_type == "reduce":
                rule = cfg.rules[action.action_info]
                symbol = rule.symbol
                production = rule.production
                if len(production) != 0:
                    work_stack = work_stack[:(-2) * len(production)]
                input_queue.insert(0, symbol)
                output_queue.insert(0, action.action_info)
            elif action.action_type == "shift":
                work_stack.append(input_queue[0])
                input_queue.pop(0)
                work_stack.append(action.action_info)
            else:
                raise Exception("Error: Unknown Action: " + action.action_type)

    @staticmethod
    def __log_automata(logging_info, work_stack, input_queue, output_queue):
        if logging_info[0]:
            print("Step: " + str(logging_info[1]))
            print("\t|Work Stack: " + str(work_stack))
            print("\t|Input Queue: " + str(input_queue))
            print("\t|Output Queue: " + str(output_queue))
            logging_info[1] += 1

    @staticmethod
    def __log_action(logging_info, action):
        if logging_info[0]:
            print("\tAction -> " + str(action))

    @staticmethod
    def __log_accept_output(logging_info, output_queue):
        if logging_info[0]:
            print("Step: Accepted\n\t|Output Queue: " + str(output_queue))

    @staticmethod
    def __get_initial_automata(sequence):
        sequence.append(LR1Analyzer.sentence_end)
        return [LR1Analyzer.sentence_end, 0, ], sequence, []

    def __str__(self):
        output = "LR1 Analyzer:"
        output += ("\n" + str(self.cfg)).replace("\n", "\n\t")
        output += "First1:\n"
        for non_terminal in self.cfg.non_terminals:
            output += "\t" + "\t" + non_terminal + " -> " + str(self.first1[non_terminal]) + "\n"

        output += "\t" + "States:\n"
        for state_index in range(len(self.states)):
            state = self.states[state_index]
            output += "\t" + "\t" + "State(" + str(state_index) + "):\n"
            for lr1rule in state:
                output += "\t" + "\t" + "\t" + str(lr1rule) + "\n"

        output += "\t" + "Table:\n"
        for state_index in range(len(self.states)):
            output += "\t" + "\t" + "State(" + str(state_index) + "):\n"
            for input_symbol in self.table[state_index].keys():
                action = self.table[state_index][input_symbol]
                output += "\t" + "\t" + "\t" + "Input Symbol: " + input_symbol + "\t|\t" + str(action) + "\n"

        return output
