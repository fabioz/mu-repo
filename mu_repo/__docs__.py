'''mu-repo is a command-line utility to deal with multiple git repositories.
        
It works with a .mu_repo file in the current working dir which provides the 
configuration of the directories that should be tracked on commands
(it may also be used as a git replacement on directories containing a 
.git dir).

Commands:

* ${START_COLOR}mu register repo1 repo2:${RESET_COLOR} Registers repo1 and repo2 to be tracked.
* ${START_COLOR}mu register --all:${RESET_COLOR} Registers all subdirs with .git.
* ${START_COLOR}mu list:${RESET_COLOR} Lists the currently tracked repositories.
* ${START_COLOR}mu set-var git=d:/bin/git/bin/git.exe:${RESET_COLOR} Set git location to be used.
* ${START_COLOR}mu set-var serial=0|1:${RESET_COLOR} Set commands to be executed serially or in parallel.
* ${START_COLOR}mu get-vars:${RESET_COLOR} Prints the configuration file.
* ${START_COLOR}mu github-request:${RESET_COLOR} Gets a request from github.
* ${START_COLOR}mu fix-eol:${RESET_COLOR} Changes end of lines to '\\n' on all changed files.
* ${START_COLOR}mu install:${RESET_COLOR} Initial configuration git (username, log, etc.)
* ${START_COLOR}mu auto-update:${RESET_COLOR} Automatically updates mu-repo 
  (using git -- must have been pulled from git as in the instructions).

* ${START_COLOR}mu dd:${RESET_COLOR}
     Creates a directory structure with working dir vs head and opens 
     WinMerge with it (doing mu ac will commit exactly what's compared in this
     situation).
     
     Also accepts a parameter to compare with a different commit/branch. I.e.:
     mu dd HEAD^^
     mu dd 9fd88da
     mu dd development

Shortcuts:

${START_COLOR}mu st         ${RESET_COLOR}= Nice status message for all repos (always in parallel)
${START_COLOR}mu co branch  ${RESET_COLOR}= git checkout branch
${START_COLOR}mu mu-patch   ${RESET_COLOR}= git diff --cached --full-index > output to file for each repo 
${START_COLOR}mu mu-branch  ${RESET_COLOR}= git rev-parse --abbrev-ref HEAD (print current branch)
${START_COLOR}mu up         ${RESET_COLOR}= git fetch origin curr_branch:refs/remotes/origin/curr_branch 
${START_COLOR}mu upd | sync ${RESET_COLOR}= up/diff incoming changes
${START_COLOR}mu a          ${RESET_COLOR}= git add -A
${START_COLOR}mu c msg      ${RESET_COLOR}= git commit -m "Message" (the message must always be passed)
${START_COLOR}mu ac msg     ${RESET_COLOR}= git add -A & git commit -m (the message must always be passed) 
${START_COLOR}mu acp msg    ${RESET_COLOR}= same as 'mu ac' + git push origin current branch.
${START_COLOR}mu p          ${RESET_COLOR}= git push origin current branch.
${START_COLOR}mu shell      ${RESET_COLOR}= On msysgit, call sh --login -i (linux-like env)

Any other command is passed directly to git for each repository:
I.e.:

${START_COLOR}mu pull            ${RESET_COLOR}
${START_COLOR}mu fetch           ${RESET_COLOR}
${START_COLOR}mu push            ${RESET_COLOR}
${START_COLOR}mu checkout release${RESET_COLOR}

Note: Some actions considered 'safe' may always be executed in parallel (i.e.: mu st)

Note: Passing --timeit in any command will print the time it took
      to execute the command.
'''
