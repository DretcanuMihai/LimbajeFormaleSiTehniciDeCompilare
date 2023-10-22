from OrderedList import OrderedList


class TS:
    class Row:
        def __init__(self, value, code):
            self.value = value
            self.code = code

        def __eq__(self, other):
            return self.value == other.value

        def __lt__(self, other):
            return self.value < other.value

        def __gt__(self, other):
            return self.value > other.value

        def __le__(self, other):
            return self.value <= other.value

        def __str__(self):
            return str(self.code) + ":" + str(self.value)

    def __init__(self):
        self.__elements = OrderedList()

    def get_index(self, elem):
        new_index = self.__elements.get_size()
        element = self.__elements.search_or_insert(TS.Row(elem, new_index))
        return element.code

    def __str__(self):
        message = "TS:\n"

        elems = self.__elements.get_array()
        elems = filter(lambda el: el is not None, elems)
        elems = sorted(elems, key=lambda el: el.code)

        for elem in elems:
            message += str(elem) + "\n"

        # elems = self.__elements.get_array()
        # for i in range(len(elems)):
        #     message += str(i) + " -> " + str(elems[i]) + "\n"

        return message


def test_ts():
    print("Testing ts.py...")
    ts = TS()
    assert ts.get_index("salut") == 0
    assert ts.get_index("sal") == 1
    assert ts.get_index("alut") == 2
    assert ts.get_index("sal") == 1
    assert ts.get_index("alut") == 2
    assert ts.get_index("salut") == 0
    print(str(ts))
    print("Finished testing ts.py;")
