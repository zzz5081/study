#题型：递归
#关键点：接两个节点比对左右子树
#我踩的坑：用中序遍历拿完再比较，这样会漏掉结构信息

from tree_utils import TreeNode, build, to_list, preorder

class Solution:
    def isSymmetric(self, root: TreeNode | None) -> bool:
        if not root:
            return True
        def check(a,b):
            if a is None and b is None:
                return True
            elif a is None or b is None:
                return False
            return a.val == b.val and check(a.left,b.right) and check(a.right,b.left)
        return check(root.left,root.right)

if __name__ == "__main__":
    s = Solution()
    assert s.isSymmetric(build([1,2,2,3,4,4,3])) == True
    assert s.isSymmetric(build([])) == True
    assert s.isSymmetric(build([1])) == True
    assert s.isSymmetric((build([1,2,2,3,3]))) == False
    assert s.isSymmetric(build([1,2,2,None,3,None,3])) == False
    # ★ 反例：中序是回文，但结构不对称 —— 专门用来抓"遍历对比"类的错误解法
    assert s.isSymmetric(build([1, 2, 3, None, 3, None, 2])) == False
    print("通过")