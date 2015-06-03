from mu_repo.print_ import Print
from mu_repo.backwards import raw_input

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    This is the first action that should be run in a new mu installation. It'll ask for common
    things to configure git properly.
    
    Things not done here but which the user should still do:
    
    Set: GIT_SSH to point to plink.exe (and have pageant with the key already loaded).
    '''
    git = params.config.git or 'git'
    from mu_repo.execute_command import ExecuteCommand

    #--- Name
    user_name = raw_input('User name:').strip()
    if user_name:
        ExecuteCommand([git] + 'config --global user.name'.split() + [user_name], '.')
    else:
        Print('Skipping user.name configuration.')


    #--- E-mail
    user_email = raw_input('\nUser e-mail:').strip()
    if user_email:
        ExecuteCommand([git] + 'config --global user.email'.split() + [user_email], '.')
    else:
        Print('Skipping user.email configuration.')


    #--- Auto-crlf
    auto_crlf = raw_input('\nAuto-crlf handling (default false, options: false, true, input):').strip().lower()
    if not auto_crlf:
        auto_crlf = 'false'

    if auto_crlf in ('false', 'true', 'input'):
        ExecuteCommand([git] + 'config --global core.autocrlf'.split() + [auto_crlf], '.')
    else:
        Print('Skipping core.autocrlf configuration (input: "%s" not recognized).' % (auto_crlf,))


    config_date = raw_input('\nConfig format.pretty for one line and set default to short? (default: y, options: y, n)').strip().lower()
    if not config_date:
        config_date = 'y'
    if config_date == 'y':
        ExecuteCommand([git] + ['config', '--global', 'format.pretty', '%h %ad %Cgreen%aN%Creset %s'], '.')
        ExecuteCommand([git] + 'config --global log.date short'.split(), '.')


    wrap = raw_input('\nShow logs wrapped? (i.e.: set less -r): (default: y, options: y, n)').strip().lower()
    if not wrap:
        wrap = 'y'
    if wrap == 'y':
        ExecuteCommand([git, 'config', '--global', 'core.pager', 'less -r'], '.')

    wrap = raw_input('\nCreate "git st" and "git create-branch" aliases? (default: y, options: y, n)').strip().lower()
    if not wrap:
        wrap = 'y'
    if wrap == 'y':
        ExecuteCommand([git, 'config', '--global', 'alias.st', 'status -s'], '.')
        ExecuteCommand([git, 'config', '--global', 'alias.create-branch', 'checkout -b    '], '.')
