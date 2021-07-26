
import os 
import subprocess
import sys 


# 21，141，160，206，234，203
# game of life 


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# def reverse(head):
#     cur = head 
#     prev, next = None, None
#     while cur:
#         next = cur.next 
#         cur.next = prev 
#         prev = cur 
#         cur = next 
#     return prev 

def print_node(head):
    while head:
        print(head.val, end=', ')
        head = head.next
    print()

def reverse(head):
    # 递归的终止条件
    if (not head) or (not head.next):
        return head

    temp = head.next  # 1->2->3->4->5  ;  temp = 2； 记录反转后的链表的末尾
    reversed_list = reverse(head.next)  # 反转 2->3->4->5 之后
                                        # reversed_list：5->4->3->2
    temp.next = head   # temp = 2, 此时在 reversed_list 的最末尾
    head.next = None   # head 应该是 最后一个Node，所以 head.next = None
    return reversed_list

n1 = ListNode(1)
n2 = ListNode(2)
n3 = ListNode(3)
n4 = ListNode(4)
n5 = ListNode(5)

n1.next = n2 
n2.next = n3 
n3.next = n4 
n4.next = n5 

print_node(n1)


res = reverse(n1)
print_node(res)