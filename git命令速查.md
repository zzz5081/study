# Git 命令速查（2026-09，第一次完整实战版）

> 按用途分类，忘了就回来翻。每条命令都亲手跑过 ✅

## 一、日常四件套

| 命令 | 人话解释 |
|---|---|
| `git status` | **看状态**：有没有改动、在哪个分支、还差什么没提交。不知道干嘛先跑它 |
| `git add 文件` | 把改动**打包**进暂存区（`-A` = 全部文件） |
| `git commit -m "说明"` | **正式存档**，生成存档点，以后能回到这 |
| `git push` | 把本地存档**上传 GitHub**（云备份） |

## 二、分支命令

| 命令 | 人话解释 |
|---|---|
| `git branch` | 列出所有分支，`*` = 当前所在 |
| `git checkout -b 名字` | 一个命令干两件事：**新建**分支 + **切换**过去 |
| `git checkout 名字` | 只**切换**到已有分支 |
| `git merge 名字` | 把那个分支的存档**合并进当前分支** |
| `git branch -d 名字` | **删除**分支（`-d` 只在已合并时允许删，防误删） |

## 三、查看命令

| 命令 | 人话解释 |
|---|---|
| `git log --oneline` | 看**存档历史**，每行一个存档点（新的在上） |
| `git remote -v` | 看**远程仓库地址**（origin = 推送到哪） |

## 四、输出黑话翻译

| 术语 | 意思 |
|---|---|
| `HEAD` | 你现在**站在哪**（当前位置/分支） |
| `origin` | 远程仓库的**代称**（默认名） |
| `main -> main` | 本地 main 推到**远程** main 成功 |
| `ahead by 1` | 本地比 GitHub **多 1 个存档**（还没 push） |
| `fast-forward` | **快进合并**：主线没动过，直接挪指针（最顺利的合并） |
| `working tree clean` | **干净状态**：所有改动都存档了 |
| `untracked` | 文件夹里有但 git 还没**登记**过的文件 |
| `Changes to be committed` | 已 add 打包，等待 commit 存档 |
| `up to date with 'origin/main'` | 本地和 GitHub **完全同步** |

## 五、核心概念（理解比背命令重要）

### 存档流程 = 三步
```
工作区（你改代码）
  → git add（打包）
  → git commit（本地存档）
  → git push（上云）
```
commit 只存**本地**，push 才上**云**——电脑坏了，只有 push 过的才救得回来。

### 三个区
- **工作区**：你正在改的文件
- **暂存区**：add 之后（打包待发）
- **仓库**：commit 之后（已存档）

### 分支 = 平行世界
- `main` = 主线；分支 = 从主线复制一条副本线随便折腾
- 分支上的提交不影响 main；`merge` 后收编进主线
- 已合并的分支可以安全 `-d` 删除

### 远程配置在哪
推送到哪记在仓库隐藏文件 `.git\config` 里（`[remote "origin"]`），
`git remote -v` 可查看。克隆仓库时自动带上。

## 六、完整实战流程回顾（2026-09 第一次跑通）

```powershell
git status                          # 看状态：一堆 untracked 练习文件
git add -A                          # 全部打包
git commit -m "归档:8-9月练习文件"    # 存档 14006cb
git push                            # 上云

git checkout -b feature-git         # 开平行世界并进入
# 新建 git_demo.py → add → commit   # 在平行世界存档 f7f3008
git checkout main                   # 回主线（git_demo.py 消失）
git merge feature-git               # 合并（fast-forward，文件回来）
git push                            # 上云
git branch -d feature-git           # 平行世界已合并，删除
git branch                          # 只剩 main，干净收尾
```

## 七、下一步想学的（以后补）

- `git clone`：从 GitHub 把仓库拉到自己电脑（换电脑/开新环境用）
- `git pull`：把别人/别的电脑 push 的更新拉下来
- `git diff`：看具体改了什么内容
- 解决 merge 冲突（两人改了同一处代码时）
