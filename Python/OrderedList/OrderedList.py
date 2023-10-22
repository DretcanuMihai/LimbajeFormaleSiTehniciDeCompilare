class OrderedList:
    def __init__(self):
        self.__size = 0
        self.__capacity = 2
        self.__elements = [None, None]

    def __widen(self):
        new_capacity = 2 * self.__capacity
        new_elements = [None for _ in range(new_capacity)]
        for i in range(0, self.__capacity):
            new_elements[i] = self.__elements[i]
        self.__elements = new_elements
        self.__capacity = new_capacity

    def __search_pos(self, elem):
        if self.__size == 0:
            return 0
        start = 0
        finish = self.__size
        while finish - start != 1:
            middle = (start + finish) // 2
            if elem < self.__elements[middle]:
                finish = middle
            elif elem > self.__elements[middle]:
                start = middle
            else:
                return middle
        if elem <= self.__elements[start]:
            return start
        return finish

    def __insert_on_position(self, position, value):
        new_size = self.__size + 1
        if new_size > self.__capacity:
            self.__widen()
        for i in range(self.__size, position, -1):
            self.__elements[i] = self.__elements[i - 1]
        self.__elements[position] = value
        self.__size = new_size

    def search(self, elem):
        pos = self.__search_pos(elem)
        if pos < self.__size and self.__elements[pos] == elem:
            return self.__elements[pos]
        return None

    def insert(self, elem):
        pos = self.__search_pos(elem)
        self.__insert_on_position(pos, elem)

    def get_size(self):
        return self.__size

    """
    Helpful
    """

    def search_or_insert(self, elem):
        pos = self.__search_pos(elem)
        if pos < self.__size and self.__elements[pos] == elem:
            return self.__elements[pos]
        self.__insert_on_position(pos, elem)
        return elem

    def get_array(self):
        return self.__elements


def test_ordered_list():
    print("Testing ordered_list.py...")
    my_list = OrderedList()

    elems_to_add = [50, 60, 10, 40, 20, 30]
    for elem in elems_to_add:
        my_list.insert(elem)
    assert my_list.get_size() == 6

    for i in range(0, 3):
        assert my_list.search(i) is None
    for elem in elems_to_add:
        assert my_list.search(elem) == elem

    for elem in elems_to_add:
        val = elem * 2
        assert my_list.search_or_insert(val) == val
    assert my_list.get_size() == 9

    print("Finished testing ordered_list.py;")
