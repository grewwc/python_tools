from distutils.command import build
from typing import Union


class TreeNode:
    def __init__(self, value, left=None, right=None) -> None:
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f'TreeNode({self.value},{self.left},{self.right})'


def build_tree_node(s: Union[str, list]) -> Union[TreeNode, None]:
    """
    s = [1,2,4, null, 5]
    """
    if isinstance(s, str):
        s = s.strip().strip('[').strip(']')
        nodes = [e.strip() for e in s.split(',')]
    else:
        nodes = s
    if not nodes:
        return None
    q = [TreeNode(nodes[0])]
    nodes.pop(0)
    root = q[0]
    while q and nodes:
        curr = q.pop(0)
        left = TreeNode(nodes[0]) if nodes[0] != 'null' else None
        nodes.pop(0)
        curr.left = left
        if left:
            q.append(left)
        right = TreeNode(nodes[0]) if nodes[0] != 'null' else None
        nodes.pop(0)
        curr.right = right
        if right:
            q.append(right)
    return root


def in_order_print(root: Union[TreeNode, None]):
    if not root:
        return
    in_order_print(root.left)
    print(root.value)
    in_order_print(root.right)


def in_order_traverse(root: Union[TreeNode, None]):
    res = []
    if not root:
        return res
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.value)
        curr = curr.right
    return res


def pre_order_traverse(root: Union[TreeNode, None]):
    res = []
    if not root:
        return res
    stack = []
    curr = root
    while curr or stack:
        while curr:
            res.append(curr.value)
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        curr = curr.right

    return res


def post_order_traverse(root: Union[TreeNode, None]):
    res = []
    if not root:
        return res
    stack = []
    curr = root
    prev = None
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack[-1]
        if curr.right and prev != curr.right:
            curr = curr.right
        else:
            curr = stack.pop()
            res.append(curr.value)
            prev = curr
            curr = None

    return res


if __name__ == '__main__':
    t = build_tree_node([1, 2, 4, 'null', 5])
    t = build_tree_node('[1,2,null,3,null,null,4]')
    t = build_tree_node('[1,2,3,4,5,6,7,8,null,null,null,null,null,null, 12]')
    print(pre_order_traverse(t))
    print(post_order_traverse(t))
