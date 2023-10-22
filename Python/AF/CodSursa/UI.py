from AF import AF


class UI:
    def __init__(self):
        self.__AF = None
        self.__running = True
        self.__commands_dict = self.__create_commands()

    def __create_commands(self):
        return {
            "exit": self.__exit,
            "menu": self.__menu,
            "read_file": self.__read_af_from_file,
            "read_keyboard": self.__read_af_from_keyboard,
            "print": self.__print_af,
            "sequence": self.__check_sequence,
            "prefix": self.__find_longest_prefix
        }

    def __execute_command(self, command):
        try:
            if command not in self.__commands_dict.keys():
                raise Exception("Error: Unknown command - Use 'menu' for commands")
            self.__commands_dict[command]()
        except Exception as ex:
            print(str(ex))

    def __exit(self):
        self.__running = False

    def __menu(self):
        menu = "Menu:\n"
        for command in self.__commands_dict.keys():
            menu += command + "\n"
        print(menu)

    def __read_af_from_file(self):
        filename = input("Filename:")
        self.__AF = AF.from_file(filename)

    def __read_af_from_keyboard(self):
        print("Enter AF:")
        text = ""
        line_index = 1
        while True:
            current_line = input("Line " + str(line_index) + ":")
            if current_line == ";;":
                break
            text += current_line + "\n"
            line_index += 1
        text = text[:-1]
        self.__AF = AF.from_text(text)

    def __print_af(self):
        if self.__AF is None:
            raise Exception("Error: AF is uninitialized")
        print(str(self.__AF))

    def __check_sequence(self):
        if self.__AF is None:
            raise Exception("Error: AF is uninitialized")
        sequence = input("Sequence:")
        print("Sequence is accepted:" + str(self.__AF.sequence_is_accepted(sequence)))

    def __find_longest_prefix(self):
        if self.__AF is None:
            raise Exception("Error: AF is uninitialized")
        sequence = input("Sequence:")
        longest_prefix = self.__AF.find_longest_accepted_prefix(sequence)
        if longest_prefix is None:
            print("Sequence has no longest accepted prefix")
        else:
            print("Longest prefix is:\n" + longest_prefix)

    def run(self):
        while self.__running:
            command = input(">>")
            self.__execute_command(command)
        print("Exiting...")
