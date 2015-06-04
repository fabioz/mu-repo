### Shortcuts:

* `mu st`         = Nice status message for all repos (always in parallel)

* `mu co branch`  = git checkout branch

* `mu mu-branch`  = git rev-parse --abbrev-ref HEAD (print current branch)

* `mu up`         = git fetch origin curr_branch:refs/remotes/origin/curr_branch (also see [mu upd on Commands](commands.md)) for fetch/diff at once. 

* `mu rb`         = git rebase origin/current branch.

* `mu a`          = git add -A

* `mu c msg`      = git commit -m "Message" (the message must always be passed)

* `mu ac msg`     = git add -A & git commit -m (the message must always be passed)

* `mu acp msg`    = same as 'mu ac' + git push origin current branch.

* `mu p`          = git push origin current branch.

* `mu shell`      = On msysgit, call sh --login -i (linux-like env)

##### Regular commands:

Any other command is passed directly to git for each repository, for example:

    mu pull
    mu fetch
    mu push
    mu checkout release

Also see:

* [Commands](commands.md)
* [Tips & Tricks](tips_and_tricks.md)
