class FIP:
    class Row:
        def __init__(self, atom_code, ts_code):
            self.atom_code = atom_code
            self.ts_code = ts_code

        def __str__(self):
            message = str(self.atom_code)
            if self.ts_code is not None:
                # message += " - " + str(self.ts_code)
                message += "\n" + str(self.ts_code)
            return message

    def __init__(self):
        self.__encoding = []

    def insert_atom(self, atom_code, ts_code=None):
        self.__encoding.append(FIP.Row(atom_code, ts_code))

    def get_as_list(self):
        return self.__encoding

    def __str__(self):
        message = "FIP:\n"
        # for i in range(len(self.__encoding)):
        #     message += str(i + 1) + " -> " + str(self.__encoding[i]) + "\n"
        for elem in self.__encoding:
            message += str(elem)+"\n"
        return message


def test_fip():
    print("Testing fip.py...")
    fip = FIP()
    fip.insert_atom(2)
    fip.insert_atom(3)
    fip.insert_atom(0, 5)
    fip.insert_atom(0, 5)
    fip.insert_atom(1, 2)
    fip.insert_atom(10)
    print(str(fip))
    print("Finished testing fip.py;")
