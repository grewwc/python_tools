

class ListNode:
    def __init__(self, value, next=None) -> None:
        self.value = value
        self.next = None


def reverse(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
    return prev


def build_list(*args):
    dummy = ListNode(0)
    curr = dummy
    for arg in args:
        new = ListNode(arg, None)
        curr.next = new
        curr = new
    return dummy.next


def print_list(head: ListNode):
    while head:
        print(head.value, end=', ')
        head = head.next
    print()


def test():
    head = build_list(1, 2, 4, 5, 100)
    print_list(head)
    head = reverse(head)
    print_list(head)


if __name__ == '__main__':
    test()
