# Week 2 Interview Prep

## Day 1 - Feb 2

### Problem 1: LeetCode 104 - Maximum Depth of Binary Tree
- **Approach:** [DFS/BFS]
- **Time Complexity:** O(n)(O(number of nodes))
- **Space Complexity:** O(h)(O(height of tree))
- **Key Learning:** [Initialize a variable which keeps count of max depth and return that. Send that variable in every call to function and compare it with the depth of that call.]
- **Link:** https://leetcode.com/problems/maximum-depth-of-binary-tree/

```CPP

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    void find(TreeNode* root, int &r, int d){
        if(root){
            d+=1;
            r=max(r, d);
            if(root->left){
                find(root->left, r, d);
            }
            if(root->right){
                find(root->right, r, d);
            }
        }
    }

    int maxDepth(TreeNode* root) {
        int r=0;
        find(root, r, 0);
        return r;
    }
};

```

### Problem 2: LeetCode 100 - Same Tree
- **Approach:** [Recursively checking every node]
- **Time Complexity:** O(n)
- **Space Complexity:** O(h)
- **Key Learning:** [Checking for every node using a separate function called recursively.]
- **Link:** https://leetcode.com/problems/same-tree/

```CPP

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool check(TreeNode* p, TreeNode* q){
        if(!p && !q){
            return true;
        }
        if((p && q) && (p->val == q->val) && check(p->left, q->left) && check(p->right, q->right)){
            return true;
        }
        return false;
    }
    bool isSameTree(TreeNode* p, TreeNode* q) {
        return check(p, q);
    }
};

```

---