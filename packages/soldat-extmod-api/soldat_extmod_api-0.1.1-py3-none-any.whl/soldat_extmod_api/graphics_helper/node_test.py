class Node:
    last_node: 'Node' = None
    def __init__(self, base_addr: int) -> None:
        self.base_addr = base_addr
        self.next: Node = None
        self.previous: Node = None
        if Node.last_node:
            self.previous = Node.last_node
            Node.last_node.next = self
        Node.last_node = self

    def destroy(self):
        if Node.last_node == self:
            Node.last_node = self.previous
            if self.previous:
                self.previous.next = None
        if self.previous and self.next:
            self.previous.next = self.next
            self.next.previous = self.previous

    def __str__(self) -> str:
        return str(self.base_addr)
    
    @staticmethod
    def traverse(first: 'Node'):
        current = first
        while current:
            print(current)
            current = current.next
        print()

    def insert_after(self, node: 'Node'):
        if Node.last_node == node:
            Node.last_node = node.previous
            node.previous.next = None
        if Node.last_node == self:
            Node.last_node = node
        node.next = self.next
        node.previous = self
        self.next.previous = node
        self.next = node

a = Node(1)
b = Node(2)
c = Node(3)
d = Node(4)
x = Node(5)

Node.traverse(a)

b.insert_after(x)
Node.traverse(a)
