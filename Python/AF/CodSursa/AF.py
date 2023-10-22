class AF:
    __class_key = object()

    __translator = {
        "nl": "\n",
        "sc": ";",
        "pipe": "|"
    }

    @staticmethod
    def from_file(filename):
        with open(filename) as af_file:
            text = af_file.read()
            return AF.from_text(text)

    @staticmethod
    def __pre_format(text):
        while "\n\n" in text:
            text = text.replace("\n\n", "\n")
        text = text.replace(";\n", ";")
        text = text.replace("|\n", ";")
        return text

    @staticmethod
    def from_text(text):
        text = AF.__pre_format(text)
        text_lines = text.split("\n")
        if len(text_lines) < 5:
            raise Exception("Error: The text doesn't have enough sections to represent an AF")
        af = AF(AF.__class_key)
        af.__read_alphabet(text_lines[0])
        af.__read_states(text_lines[1])
        af.__read_initial_state(text_lines[2])
        af.__read_final_states(text_lines[3])
        af.__read_transitions(text_lines[4:])
        return af

    @staticmethod
    def __convert_to_alphabet_element(string_sequence):
        if string_sequence in AF.__translator.keys():
            return AF.__translator[string_sequence]
        if len(string_sequence) == 1:
            return string_sequence
        raise Exception("Error: String is not a valid element of the alphabet:\n" + string_sequence)

    def __init__(self, key):
        if key is not AF.__class_key:
            raise Exception("Error: Create AF by static methods")
        self.__alphabet = set()
        self.__states = set()
        self.__initial_state = None
        self.__final_states = set()
        self.__transitions = dict()

    def __read_alphabet(self, alphabet_payload):
        alphabet_elements = alphabet_payload.split(";")
        if len(alphabet_elements) == 0:
            raise Exception("Error: The alphabet must not be empty")
        for string in alphabet_elements:
            to_add = self.__convert_to_alphabet_element(string)
            self.__alphabet.add(to_add)

    def __read_states(self, states_payload):
        states = states_payload.split(";")
        if len(states) == 0:
            raise Exception("Error: States must not be empty")
        for state in states:
            if len(state) == 0:
                raise Exception("Error: State must not be empty string")
            self.__states.add(state)

    def __read_initial_state(self, initial_state_payload):
        initial_state = initial_state_payload
        if initial_state not in self.__states:
            raise Exception("Error: Initial state is not a declared state:\n" + initial_state)
        self.__initial_state = initial_state

    def __read_final_states(self, final_states_payload):
        final_states = final_states_payload.split(";")
        if len(final_states) == 0:
            raise Exception("Error: Final states must not be empty")
        for final_state in final_states:
            if final_state not in self.__states:
                raise Exception("Error: Final state is not a declared state:\n" + final_state)
            self.__final_states.add(final_state)

    def __read_transitions(self, transitions_payload):
        for transition_payload in transitions_payload:
            line_elements = transition_payload.split("|")
            if len(line_elements) != 3:
                raise Exception("Error: Transition line should have 3 elements")
            initial_states = line_elements[0].split(";")
            alphabet_elements = line_elements[1].split(";")
            final_states = line_elements[2].split(";")

            if len(initial_states) < 1:
                raise Exception("Error: Transition initial states doesn't have enough elements")
            if len(alphabet_elements) < 1:
                raise Exception("Error: Transition alphabet elements doesn't have enough elements")
            if len(final_states) < 1:
                raise Exception("Error: Transition final states doesn't have enough elements")

            for initial_state in initial_states:
                for alphabet_element in alphabet_elements:
                    for final_state in final_states:
                        self.__add_transition(initial_state, alphabet_element, final_state)

    def __add_transition(self, initial_state, alphabet_element, final_state):
        if initial_state not in self.__states:
            raise Exception("Error: State is not registered:\n" + initial_state)
        if alphabet_element not in self.__alphabet:
            raise Exception("Error: Element is not registered in alphabet:\n" + alphabet_element)
        if final_state not in self.__states:
            raise Exception("Error: State is not registered:\n" + final_state)

        if initial_state not in self.__transitions.keys():
            self.__transitions[initial_state] = dict()
        if alphabet_element not in self.__transitions[initial_state].keys():
            self.__transitions[initial_state][alphabet_element] = set()
        self.__transitions[initial_state][alphabet_element].add(final_state)

    def __is_determinist(self):
        for state in self.__states:
            if state in self.__transitions.keys():
                transitions = self.__transitions[state]
                for alphabet_element in transitions.keys():
                    target_states = transitions[alphabet_element]
                    if len(target_states) > 1:
                        return False
        return True

    def sequence_is_accepted(self, string):
        return string == self.find_longest_accepted_prefix(string)

    def find_longest_accepted_prefix(self, string):
        if not self.__is_determinist():
            raise Exception("Error: Unsupported for non-determinist AF")
        return self.__find_longest_accepted_prefix(string, self.__initial_state)

    def __get_next_state(self, character_to_consume, state):
        if character_to_consume not in self.__alphabet:
            return set()
        if state not in self.__transitions.keys():
            return set()
        state_transitions = self.__transitions[state]
        if character_to_consume not in state_transitions.keys():
            return set()
        return state_transitions[character_to_consume]

    def __find_longest_accepted_prefix(self, string, current_state):

        def treat_cant_advance():
            if current_state in self.__final_states:
                return ""
            else:
                return None

        if len(string) == 0:
            return treat_cant_advance()
        else:
            character_to_consume = string[0]
            next_states = self.__get_next_state(character_to_consume, current_state)

            if len(next_states) == 0:
                return treat_cant_advance()

            next_state = list(next_states)[0]

            result = self.__find_longest_accepted_prefix(string[1:], next_state)
            if result is None:
                return treat_cant_advance()
            else:
                return character_to_consume + result

    def __str__(self):
        text = ""
        text += "alphabet:" + str(sorted(self.__alphabet)) + "\n"
        text += "states:" + str(sorted(self.__states)) + "\n"
        text += "initial state:" + self.__initial_state + "\n"
        text += "final states:" + str(sorted(self.__final_states)) + "\n"
        text += "transitions:\n"
        for state in sorted(self.__transitions.keys()):
            text += state + " -> " + str(self.__transitions[state]) + "\n"
        return text


AF_ID = AF.from_file("./afs/id.txt")
AF_INT = AF.from_file("./afs/integer.txt")
AF_DOUBLE = AF.from_file("./afs/double.txt")
AF_TEXT = AF.from_file("./afs/text.txt")
AF_BOOL = AF.from_file("./afs/bool.txt")


def test_AF():
    print("Testing AF...")
    test_ID()
    test_INT()
    test_DOUBLE()
    test_TEXT()
    print("Finished testing AF")


def test_ID():
    print("Testing AF_ID...")
    assert AF_ID.sequence_is_accepted("a")
    assert AF_ID.sequence_is_accepted("asd")
    assert not AF_ID.sequence_is_accepted(".")
    assert not AF_ID.sequence_is_accepted("a.")
    assert not AF_ID.sequence_is_accepted(".a")
    assert AF_ID.sequence_is_accepted("a.a")
    print("Finished testing AF_ID")


def test_INT():
    print("Testing AF_INT...")
    assert (AF_INT.sequence_is_accepted("0"))
    assert (AF_INT.sequence_is_accepted("-0"))

    assert (AF_INT.sequence_is_accepted("0b10"))
    assert (AF_INT.sequence_is_accepted("+0b10"))
    assert (not AF_INT.sequence_is_accepted("0b2"))

    assert (AF_INT.sequence_is_accepted("012345670"))
    assert (AF_INT.sequence_is_accepted("-012345670"))
    assert (not AF_INT.sequence_is_accepted("08"))
    assert (not AF_INT.sequence_is_accepted("+08"))

    assert (AF_INT.sequence_is_accepted("0x123456789ABCDEF0"))
    assert (not AF_INT.sequence_is_accepted("00x123456789ABCDEF0"))

    assert (AF_INT.sequence_is_accepted("1234567890"))

    assert (AF_INT.sequence_is_accepted("1'234'5678'90uLl"))
    assert (not AF_INT.sequence_is_accepted("1'234'5678'90uU"))

    print("Finished testing AF_INT")


def test_DOUBLE():
    print("Testing AF_DOUBLE...")

    assert (AF_DOUBLE.sequence_is_accepted("0.0"))
    assert (AF_DOUBLE.sequence_is_accepted("-0.0"))

    assert (AF_DOUBLE.sequence_is_accepted("0E123"))
    assert (AF_DOUBLE.sequence_is_accepted("12E123"))
    assert (not AF_DOUBLE.sequence_is_accepted("12"))
    assert (not AF_DOUBLE.sequence_is_accepted("12e"))

    assert (AF_DOUBLE.sequence_is_accepted("0x123.12P1"))
    assert (AF_DOUBLE.sequence_is_accepted("0x123.1Fp1"))
    assert (not AF_DOUBLE.sequence_is_accepted("0x123.1Fp1E"))
    assert (not AF_DOUBLE.sequence_is_accepted("0x123.1pF"))
    assert (not AF_DOUBLE.sequence_is_accepted("0x123.1Fp1E"))

    assert (AF_DOUBLE.sequence_is_accepted("0x12'3.1'Fp1"))
    assert (AF_DOUBLE.sequence_is_accepted("0x12'3.1'Fp1l"))
    assert (AF_DOUBLE.sequence_is_accepted("0x12'3.1'Fp1F"))
    print("Finished testing AF_DOUBLE")


def test_TEXT():
    print("Testing AF_TEXT...")

    assert AF_TEXT.sequence_is_accepted("\"asd\"")
    assert not AF_TEXT.sequence_is_accepted("asd\"")
    assert not AF_TEXT.sequence_is_accepted("\"asd")

    assert AF_TEXT.sequence_is_accepted("\"\\n\"")
    assert not AF_TEXT.sequence_is_accepted("\"\\a\"")
    assert AF_TEXT.sequence_is_accepted("\"salut: tu\"")

    print("Finished testing AF_TEXT")
