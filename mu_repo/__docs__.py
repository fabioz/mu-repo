'''Commands:

* ${START_COLOR}mu register repo1 repo2:${RESET_COLOR} Registers repo1 and repo2 to be tracked.
* ${START_COLOR}mu register --all:${RESET_COLOR} Registers all subdirs with .git (non-recursive).
* ${START_COLOR}mu register --current:${RESET_COLOR} Registers all subdirs with .git (non-recursive).
* ${START_COLOR}mu register --recursive:${RESET_COLOR} Registers all subdirs with .git (recursive).
* ${START_COLOR}mu unregister repo1 repo2 | --all:${RESET_COLOR} Stops tracking some repository.
* ${START_COLOR}mu list:${RESET_COLOR} Lists the currently tracked repositories.
* ${START_COLOR}mu set-var git=d:/bin/git/bin/git.exe:${RESET_COLOR} Set git location to be used.
* ${START_COLOR}mu set-var serial=0|1:${RESET_COLOR} Set commands to be executed serially or in parallel.
* ${START_COLOR}mu get-vars:${RESET_COLOR} Prints the configuration file.
* ${START_COLOR}mu fix-eol:${RESET_COLOR} Changes end of lines to '\\n' on all changed files.
* ${START_COLOR}mu find-branch [-r] *pat*:${RESET_COLOR}
    Finds all branches matching a given pattern (or simply mu fb).
* ${START_COLOR}mu git-init-config:${RESET_COLOR} Initial git configuration (username, log, etc.)
* ${START_COLOR}mu --version:${RESET_COLOR} Prints its version
* ${START_COLOR}mu auto-update:${RESET_COLOR} Automatically updates mu-repo
  (using git -- if it was installed from the repo as in the instructions).

* ${START_COLOR}mu dd:${RESET_COLOR}
     Creates a directory structure with working dir vs head and opens
     WinMerge with it (doing mu ac will commit exactly what's compared in this
     situation).

     Also accepts a parameter to compare with a different commit/branch. I.e.:
     mu dd HEAD^^
     mu dd 9fd88da
     mu dd development

* ${START_COLOR}mu sh <command line>${RESET_COLOR}
   Allows calling any command line in the registered repositories
   e.g.: ${START_COLOR}mu sh ls -la${RESET_COLOR} will call ${START_COLOR}ls -la${RESET_COLOR} on all registered repositories.

* ${START_COLOR}mu clone:${RESET_COLOR} Cloning multiple repos from a base url.
  Use mu clone --help to open browser with more details.

* ${START_COLOR}mu <command> repo:<repo1>,<repo2>${RESET_COLOR}
   Allows specifying target repositories for a single command:
   e.g.: ${START_COLOR}mu st repo:repo1,repo2${RESET_COLOR}: Will do st on repo1 and repo2.

* ${START_COLOR}mu group:${RESET_COLOR} Repository grouping

  * ${START_COLOR}mu group add <name> [--empty]:${RESET_COLOR}
      Creates new group with current repositories, unless --empty is given
  * ${START_COLOR}mu group rm <name>:${RESET_COLOR} Removes a group
  * ${START_COLOR}mu group switch <name>:${RESET_COLOR} Switches to an existing group
  * ${START_COLOR}mu group reset:${RESET_COLOR} Stops using the current group (uses all repos again).
  * ${START_COLOR}mu group:${RESET_COLOR} With no parameters, just lists current groups

  Use ${START_COLOR}mu register${RESET_COLOR} normally to add repositories to the current group
  Use ${START_COLOR}mu list${RESET_COLOR} to list repositories in the current group

Shortcuts:

${START_COLOR}mu st         ${RESET_COLOR}= Nice status message for all repos (always in parallel)
${START_COLOR}mu co branch  ${RESET_COLOR}= git checkout branch
${START_COLOR}mu mu-branch  ${RESET_COLOR}= git rev-parse --abbrev-ref HEAD (print current branch)
${START_COLOR}mu up         ${RESET_COLOR}= git fetch origin curr_branch:refs/remotes/origin/curr_branch
${START_COLOR}mu up --all   ${RESET_COLOR}= git fetch origin (always in parallel)
${START_COLOR}mu upd | sync ${RESET_COLOR}= up/diff incoming changes
${START_COLOR}mu a          ${RESET_COLOR}= git add -A
${START_COLOR}mu c msg      ${RESET_COLOR}= git commit -m "Message" (the message must always be passed)
${START_COLOR}mu ac msg     ${RESET_COLOR}= git add -A & git commit -m (the message must always be passed)
${START_COLOR}mu acp msg    ${RESET_COLOR}= same as 'mu ac' + git push origin current branch.
${START_COLOR}mu p          ${RESET_COLOR}= git push origin current branch.
${START_COLOR}mu rb         ${RESET_COLOR}= git rebase origin/current branch.
${START_COLOR}mu shell      ${RESET_COLOR}= On msysgit, call sh --login -i (linux-like env)
${START_COLOR}mu fb [-r] pat${RESET_COLOR}= Shortcut for find-branch

Any other command is passed directly to git for each repository:
I.e.:

${START_COLOR}mu pull            ${RESET_COLOR}
${START_COLOR}mu fetch           ${RESET_COLOR}
${START_COLOR}mu push            ${RESET_COLOR}
${START_COLOR}mu checkout release${RESET_COLOR}

Note: Actions considered safe may always be executed in parallel (i.e.: mu st)

Note: Passing --timeit in any command will print the time for the command.
'''
