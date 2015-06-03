Shortcuts:

* mu st         = Nice status message for all repos (always in parallel)
* mu co branch  = git checkout branch
* mu mu-patch   = git diff --cached --full-index > output to file for each repo
* mu mu-branch  = git rev-parse --abbrev-ref HEAD (print current branch)
* mu up         = git fetch origin curr_branch:refs/remotes/origin/curr_branch
* mu upd | sync = up/diff incoming changes
* mu a          = git add -A
* mu c msg      = git commit -m "Message" (the message must always be passed)
* mu ac msg     = git add -A & git commit -m (the message must always be passed)
* mu acp msg    = same as 'mu ac' + git push origin current branch.
* mu p          = git push origin current branch.
* mu rb         = git rebase origin/current branch.
* mu shell      = On msysgit, call sh --login -i (linux-like env)
* mu dd         = Creates a folder structure and diffs it with WinMerge or meld (edited files are synched back)

Any other command is passed directly to git for each repository, for example:

    mu pull
    mu fetch
    mu push
    mu checkout release


DIFFING MULTIPLE REPOSITORIES
-----------------------------

The command ``mu dd`` provides the means to diff the multiple repository structures 
with winmerge (Windows) or meld (Linux) so that the file can be changed 
while seeing the differences of the working copy with the head in the repository.

It's similar to what would be achieved in the Eclipse synchronize view (where the 
file may be edited to change the original file -- as the structure is created with 
links to the original files, so files edited in winmerge/meld will properly change the 
original files).


