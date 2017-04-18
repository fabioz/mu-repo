The `mu open-url` action may be used to open the web-browser to open urls for the modified repositories compared to some **dest** branch
(commonly used to create pull reviews in multiple repositories).

To use:
========

`mu open-url main-pattern --dest=dest_branch`

The main-pattern may use the following keywords:

* `repo`: the repository name

* `source`: the source branch

* `dest`: the repository destination name


So, given the following situations, it may be used to create pull requests by using:

Github pattern: `https://github.com/user/project/compare/old_development...master`

    mu open-url https://github.com/user/{repo}/compare/{source}...{dest} --dest=master

Bitbucket pattern: `https://bitbucket.org/user/project/branch/source_branch?dest=master`

    mu open-url https://bitbucket.org/user/{repo}/branch/{source}?dest={dest} --dest=master

Stash pattern: `https://custom.domain.com/stash/projects/container/repos/repo_name/compare/commits?sourceBranch=sourceBranch&targetBranch=master`

    mu open-url "https://custom.domain.com/stash/projects/container/repos/{repo}/compare/commits?sourceBranch={source}&targetBranch={dest}" --dest=master

Note that currently the base url/pattern must be the same for all the repos (it's not possible
to have one repository hosted in one place and another in another place for the current code
to work -- for this we'd need to store the url per repository).