class Node:
    def __init__(self, value, prev=None):
        self.value = value
        self.prev = prev


class Stack:
    def __init__(self):
        self._storage = []

    def push(self, value):
        self._storage.append(value)

    def pop(self):
        return self._storage.pop()

    def empty(self):
        return len(self._storage) == 0

    def head_value(self):
        if len(self._storage):
            return self._storage[-1]
        else:
            return None


class ImmutableStack:
    def __init__(self, head=None):
        self.head = head

    def push(self, value):
        return self.__class__(Node(value, self.head))

    def head_value(self):
        if self.head:
            return self.head.value
        else:
            return None

    def pop(self):
        if self.head:
            return self.__class__(self.head.prev)
        else:
            return self

    def empty(self):
        return self.head is None


if __name__ == '__main__':
    stack = Stack()
    for i in range(10):
        stack.push(i)

    print('\ntesting generic stack')
    while not stack.empty():
        print(stack.pop(), end=' ')

    im_stack = ImmutableStack()
    for i in range(10):
        im_stack = im_stack.push(i)

    print('\ntesting immutable stack')
    while not im_stack.empty():
        print(im_stack.head_value(), end=' ')
        im_stack = im_stack.pop()
