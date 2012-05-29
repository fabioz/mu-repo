'''
Created on 17/05/2012

@author: Fabio Zadrozny
'''
from mu_repo.print_ import Print
import os.path
from mu_repo import Status
from mu_repo.execute_git_command_in_thread import ExecuteGitCommandThread
from mu_repo.on_output_thread import ExecuteThreadsHandlingOutputQueue




#===================================================================================================
# Run
#===================================================================================================
def Run(params, on_output=Print):
    args = params.args
    config = params.config
    import Queue
    output_queue = Queue.Queue()

    arg0 = args[0]
    if arg0 == 'st':
        args[0] = 'status'
        if len(args) == 1:
            args.insert(1, '--porcelain')

    elif arg0 == 'co':
        args[0] = 'checkout'

    elif len(args) == 1:

        if arg0 == 'mu-branch':
            args[0] = 'rev-parse'
            args.insert(1, '--abbrev-ref')
            args.insert(2, 'HEAD')
            def OnOutput(output):
                stdout = output.stdout
                if stdout.strip():
                    Print('Writing diff --cached for: ', output.repo)
                    with open('__diff__.' + output.repo + '.patch', 'w') as f:
                        f.write(stdout)
                else:
                    Print('EMPTY diff --cached for: ', output.repo)
            on_output = OnOutput


        elif arg0 == 'mu-patch':
            args[0] = 'diff'
            args.insert(1, '--cached')
            args.insert(2, '--full-index')
            config.serial = False #Always exec in parallel mode!
            def OnOutput(output):
                stdout = output.stdout
                if stdout.strip():
                    Print('Writing diff --cached for: ', output.repo)
                    with open('__diff__.' + output.repo + '.patch', 'w') as f:
                        f.write(stdout)
                else:
                    Print('EMPTY diff --cached for: ', output.repo)
            on_output = OnOutput

    if not config.repos:
        msg = 'No repository registered. Use mu register repo_name to register repository.'
        Print(msg)
        return Status(msg, True, config)

    threads = []
    for repo in config.repos:
        if not os.path.exists(repo):
            Print('%s does not exist' % (repo,))
        else:
            t = ExecuteGitCommandThread(
                repo, args, config, output_queue)

            threads.append(t)

    if config.serial:
        for t in threads:
            t.run(serial=True) #When serial will print as is executing.
    else:
        ExecuteThreadsHandlingOutputQueue(threads, output_queue, on_output)

    return Status('Finished', True)

