# -*- coding: utf-8 -*-
"""
二叉树题的公共工具（所有树题都从这里 import，不要每题重写一遍）

用法：
    from tree_utils import TreeNode, build, to_list, preorder

    assert to_list(build([3,9,20,None,None,15,7])) == [3,9,20,None,None,15,7]
"""
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """把 LeetCode 的层序列表（用 None 表示空位）变成真正的树。

    例：build([1,2,3,None,4])  →
            1
           / \\
          2   3
           \\
            4
    """
    if not vals:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


def to_list(node: Optional[TreeNode]) -> List[Optional[int]]:
    """把树按层序拍平成列表（末尾的 None 去掉），用于 assert 比对。

    ⚠️ 为什么要用它：TreeNode 没定义 __eq__，
       所以 TreeNode(1) == TreeNode(1) 是 False（比的是内存地址）。
       要比"内容"，必须拍平成可比的东西。
    """
    if node is None:
        return []
    out, queue = [], [node]
    while queue:
        n = queue.pop(0)
        if n is None:
            out.append(None)
            continue
        out.append(n.val)
        queue.append(n.left)
        queue.append(n.right)
    while out and out[-1] is None:
        out.pop()
    return out


def preorder(node: Optional[TreeNode]) -> List[int]:
    """前序遍历（调试用，看结构更直观）"""
    if node is None:
        return []
    return [node.val] + preorder(node.left) + preorder(node.right)


if __name__ == "__main__":
    # 自测：确认这个工具本身是好的（"验证你的验证工具"）
    assert build([]) is None
    assert to_list(build([1])) == [1]
    assert to_list(build([1, 2, 3])) == [1, 2, 3]
    assert to_list(build([1, 2, None, 3])) == [1, 2, None, 3]
    # 右斜：1 →右→ 2 →右→ 3   （写成 [1,None,2,None,3]，不是多塞几个 None）
    assert to_list(build([1, None, 2, None, 3])) == [1, None, 2, None, 3]
    assert to_list(build([3, 9, 20, None, None, 15, 7])) == [3, 9, 20, None, None, 15, 7]
    assert preorder(build([1, 2, 3])) == [1, 2, 3]
    # 左斜：1 →左→ 2 →左→ 3
    assert to_list(build([1, 2, None, 3])) == [1, 2, None, 3]
    print("✅ tree_utils 自身全部通过")
