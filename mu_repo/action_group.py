from __future__ import with_statement
from mu_repo import Status, backwards
from mu_repo.print_ import Print
from mu_repo.backwards import raw_input

#===================================================================================================
# Run
#===================================================================================================
def Run(params):
    '''
    Actions for mu group.
    '''
    args = params.args
    config_file = params.config_file
    config = params.config

    msgs = []
    command = args[1] if len(args) > 1 else None
    group_name = args[2] if len(args) > 2 else None

    clean_new_group = '--clean' in args or '--empty' in args

    if command != 'add' and clean_new_group:
        msg = '--clean and --empty only for "add" command'
        Print(msg)
        return Status(msg, False)

    if not command:
        if not config.groups:
            msg = 'No groups registered. Use "add" to add a new one.'
            Print(msg)
            msgs.append(msg)
        else:
            for group_name in config.groups:
                if group_name == config.current_group:
                    msg = '* %s' % group_name
                else:
                    msg = '  %s' % group_name
                Print(msg)
                msgs.append(msg)

    elif command == 'add':
        if group_name is None:
            msg = 'Group name not given.'
            Print(msg)
            return Status(msg, False)

        if group_name in config.groups:
            msg = 'Group ${START_COLOR}%s${RESET_COLOR} already exists.' % group_name
            Print(msg)
            return Status(msg, False)

        if clean_new_group:
            config.groups[group_name] = []
        else:
            config.groups[group_name] = config.repos

        config.current_group = group_name

    elif command in ('rm', 'del', 'switch', 'sw'):
        if group_name is None:

            header_msg = 'Please choose which group you want to switch to:'

            while True:
                Print(header_msg)
                groups = set()
                i_to_group = {}
                lines = []
                for i, (group, group_contents) in enumerate(sorted(backwards.iteritems(config.groups))):
                    groups_desc = ', '.join(group_contents)
                    lines.append(('[${START_COLOR}%s${RESET_COLOR}]: %s' % (i, group), groups_desc))
                    
                    i_to_group[str(i)] = group
                    groups.add(group)
                    
                discount_len = len('${START_COLOR}') + len('${RESET_COLOR}')
                
                max_part_0 = 0
                for line in lines:
                    max_part_0 = max(max_part_0, len(line[0])-discount_len) 
                max_part_0+= 1
                    
                    
                max_cols = 80
                remainder = max_cols - max_part_0
                if remainder < 20:
                    remainder = 20
                
                part0_size = max_cols - remainder
                    
                for part0, part1 in lines:
                    if (len(part0) - discount_len) < part0_size:
                        part0 += ' ' * (part0_size - (len(part0) - discount_len))  
                        
                    if len(part1) > remainder:
                        part1 = part1[:remainder-3] + '...'
                    
                    Print(part0+part1)
                    

                Print('\n[${START_COLOR}C${RESET_COLOR}]: Cancel')

                try:
                    user_entered = raw_input('\nSelect: ').strip()
                except KeyboardInterrupt:
                    return Status('Cancelled', False)

                if user_entered in i_to_group:
                    group_name = i_to_group[user_entered]
                    break

                if user_entered in groups:
                    group_name = user_entered
                    break

                if user_entered in ('C', 'c'):
                    return Status('Cancelled', False)

                header_msg = 'Did not match. Please choose again:'


        if group_name not in config.groups:
            msg = 'Group "%s" does not exist.' % group_name
            Print(msg)
            return Status(msg, False)

        if command in ('switch', 'sw'):
            msg = 'Switched to group ${START_COLOR}%s${RESET_COLOR}' % group_name
            config.current_group = group_name
        else:
            msg = 'Group ${START_COLOR}%s${RESET_COLOR} removed' % group_name
            if config.current_group == group_name:
                config.current_group = None
                msg += ' (no current group)'

            msg += '.'
            del config.groups[group_name]

        Print(msg)
        msgs.append(msg)

    elif command == 'reset':
        config.current_group = None

        msg = 'Group reset. No current group.'
        Print(msg)
        msgs.append(msg)

    else:
        msg = 'Unknown group command: %s' % command
        Print(msg)
        return Status(msg, False)

    with open(config_file, 'w') as f:
        f.write(str(config))

    return Status('\n'.join(msgs), True, config)



