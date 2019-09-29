from immutablity101.stack import ImmutableStack


class Queue:
    def __init__(self):
        self._storage = []

    def enqueue(self, value):
        self._storage.append(value)

    def deque(self):
        return self._storage.pop(0)

    def empty(self):
        return len(self._storage) == 0


class ImmutableQueue:
    def __init__(self, tail_stack=None, head_stack=None):
        self._tail_stack = tail_stack or ImmutableStack()
        self._head_stack = head_stack or ImmutableStack()

    def _tail_to_head(self):
        # define behaviour when head is empty
        pass

    def enqueue(self, value):
        self._tail_stack = self._tail_stack.push(value)
        if self._head_stack.empty():  # define behaviour when head is empty
            return self._tail_to_head()
        return ImmutableQueue(self._tail_stack, self._head_stack)

    def head_value(self):
        if self._head_stack.empty():
            return None
        else:
            return self._head_stack.head_value()

    def deque(self):
        self._head_stack = self._head_stack.pop()
        if self._head_stack.empty():  # define behaviour when head is empty
            return self._tail_to_head()
        else:
            return ImmutableQueue(self._tail_stack, self._head_stack)

    def empty(self):
        return self._tail_stack.empty() and self._head_stack.empty()


if __name__ == '__main__':
    queue = Queue()

    for i in range(10):
        queue.enqueue(i)

    for i in range(5):
        queue.deque()

    for i in range(10):
        queue.enqueue(i)

    print('\ntesting generic queue')
    while not queue.empty():
        print(queue.deque(), end=' ')

    im_queue = ImmutableQueue()

    for i in range(10):
        im_queue.enqueue(i)

    for i in range(5):
        im_queue.deque()

    for i in range(10):
        im_queue.enqueue(i)

    print('\ntesting immutable queue')
    while not im_queue.empty():
        print(im_queue.head_value(), end=' ')
        im_queue.deque()
