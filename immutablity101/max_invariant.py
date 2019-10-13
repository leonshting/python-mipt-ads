from immutablity101.stacks import Stack, ImmutableStack
from immutablity101.queues import ImmutableQueue


class MaxStack:
    def __init__(self):
        self._main_stack = Stack()
        self._max_stack = Stack()

    def push(self, value):
        self._main_stack.push(value)
        self._max_stack.push(value)

    def pop(self):
        self._max_stack.pop()
        return self._main_stack.pop()

    def get_max(self):
        return self._max_stack.head_value()

    def head_value(self):
        return self._main_stack.head_value()


class ImmutableMaxStack:
    def __init__(self, main_stack=None, max_stack=None):
        self._main_stack = main_stack or ImmutableStack()
        self._max_stack = max_stack or ImmutableStack()

    def push(self, value):
        new_main = self._main_stack.push(value)
        if self._max_stack.empty():
            new_max = self._max_stack.push(value)
        else:
            new_max = self._max_stack.push(max(self._max_stack.head_value(), value))
        return self.__class__(new_main, new_max)

    def pop(self):
        new_max = self._max_stack.pop()
        new_main = self._main_stack.pop()
        return self.__class__(new_main, new_max)

    def get_max(self):
        return self._max_stack.head_value()

    def head_value(self):
        return self._main_stack.head_value()

    def empty(self):
        return self._main_stack.empty()


class ImmutableMaxQueue(ImmutableQueue):

    def __init__(self, tail_stack=None, head_stack=None):
        tail = tail_stack or ImmutableMaxStack()
        head = head_stack or ImmutableMaxStack()

        super(ImmutableMaxQueue, self).__init__(tail_stack=tail, head_stack=head)

    def _tail_to_head(self):
        return super(ImmutableMaxQueue, self)._tail_to_head()

    def enqueue(self, value):
        return super(ImmutableMaxQueue, self).enqueue(value)

    def get_max(self):
        if self._head_stack.empty():
            return self._tail_stack.get_max()
        elif self._tail_stack.empty():
            return self._head_stack.get_max()
        else:
            return max(self._tail_stack.get_max(), self._head_stack.get_max())
