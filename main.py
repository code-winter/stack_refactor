

class MyStack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        if len(self.items) == 0:
            return True
        else:
            return False

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return 'Stack is empty'
        else:
            return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


def main():
    stack = MyStack()
    query = '()([[[]]])({})[]'
    for char in query:
        if stack.is_empty():
            stack.push(char)
        else:
            top = stack.peek()
            if (char == ')' and top == '(') or (char == ']' and top == '[') or (char == '}' and top == '{'):
                stack.pop()
            else:
                stack.push(char)
    if stack.is_empty():
        print('Сбалансированно')
    else:
        print('Несбалансированно')


if __name__ == '__main__':
    main()
