import os
import shutil
import sys

dry_run = False
dry_run_param = '--dry-run'
verbose_mode = False
verbose_param = '-v'
script_name = ""
old_name = ""
new_name = ""
change_everything = True
change_files_content = False
change_files_names = False
change_folders_names = False
change_files_content_param = '-fc'
change_files_names_param = '-fn'
change_folders_names_param = '-dn'
old_name_param = '-o'
new_name_param = '-n'

grep_old_name_in_files_cmd = 'grep -rl $ . --exclude-dir=.git'
sed_regex_cmd = 's/$/$/g'
sed_file_cmd = 'sed -i \"\" -e \"$\" $'
git_diff_color_cmd = 'git diff --color | cat'
git_restore_cmd = 'git restore -- .'

find_files_to_rename_cmd = 'find . -type f -name \"*$*\"'

find_directories_to_rename_cmd = 'find . -type d | grep $'

def log_msg(msg):
    if verbose_mode:
        print(msg)

def detect_dry_run_and_verbose(arg_list):
    global dry_run, verbose_mode

    result = []
    for arg in arg_list:
        if arg == verbose_param:
            verbose_mode = True
        elif arg == dry_run_param:
            dry_run = True
        else:
            result.append(arg)

    return result

def set_parameters(arg_list):
    global change_files_names, change_files_content, change_folders_names, change_everything

    result = []
    for arg in arg_list:
        if arg == change_files_content_param:
            change_everything = False
            change_files_content = True
        elif arg == change_files_names_param:
            change_everything = False
            change_files_names = True
        elif arg == change_folders_names_param:
            change_everything = False
            change_folders_names = True
        else:
            result.append(arg)

    return result

def validate_inputs(arg_list):
    global old_name, new_name, script_name, sed_regex_cmd, sed_file_cmd
    script_name = arg_list[0]
    old_name = arg_list[1]
    new_name = arg_list[2]

    if len(old_name) == 0:
        sys.exit('Old name empty')

    if len(new_name) == 0:
        sys.exit('New name empty')

    sed_regex_cmd = sed_regex_cmd.replace('$', old_name, 1).replace('$', new_name, 1)
    sed_file_cmd = sed_file_cmd.replace('$', sed_regex_cmd, 1)

def show_params_status():
    log_msg('Rename files script initialize')
    log_msg('')
    log_msg('Dry run     : ' + str(dry_run))
    log_msg('Verbose     : ' + str(verbose_mode))
    log_msg('File Content: ' + str(change_files_content))
    log_msg('File Names  : ' + str(change_files_names))
    log_msg('Dirs Names  : ' + str(change_folders_names))
    log_msg('Change All  : ' + str(change_everything))
    log_msg('Old name    : ' + old_name)
    log_msg('New name    : ' + new_name)
    log_msg('')

def initialize():
    arg_list = detect_dry_run_and_verbose(sys.argv)
    arg_list = set_parameters(arg_list)
    validate_inputs(arg_list)
    show_params_status()

def exec_sheel_cmd(cmd):
    log_msg('exec sheel cmd: ' + cmd)
    stream = os.popen(cmd)
    result_list = []

    for line in stream:
        result_list.append(line.strip())

    stream.close()
    if verbose_mode:
        log_msg('result --> ')
        for line in result_list:
            log_msg(line)
    return result_list

def grep_old_name():
    cmd = grep_old_name_in_files_cmd.replace('$', old_name)
    return exec_sheel_cmd(cmd)

def change_file_content(file_path):
    cmd = sed_file_cmd.replace('$', repr(file_path), 1)
    os.system(cmd)

def git_diff():
    os.system(git_diff_color_cmd)

def git_restore():
    os.system(git_restore_cmd)

def process_file_content():
    if change_everything == False:
        if change_files_content == False:
            return
    
    for file in grep_old_name():
        change_file_content(file)

    if verbose_mode:
        git_diff()

    if dry_run:
        git_restore()

def find_files_to_rename():
    cmd = find_files_to_rename_cmd.replace('$', old_name, 1)
    return exec_sheel_cmd(cmd)

def rename_file_or_directory(old_path):
    index = old_path.rfind(old_name)
    if index < 0:
        return
        
    new_path = old_path[:index] + old_path[index:].replace(old_name, new_name, 1)
    log_msg('from: ' + old_path)
    log_msg('to:   ' + new_path + '\n')
    if dry_run == False:
        shutil.move(old_path, new_path)

def process_rename_files():
    if change_everything == False:
        if change_files_names == False:
            return

    for file in find_files_to_rename():
        rename_file_or_directory(file)

def find_directories_to_rename():
    cmd = find_directories_to_rename_cmd.replace('$', old_name, 1)
    return exec_sheel_cmd(cmd)

def remove_duplicate_and_reverse_order(dir_list):
    return list(dict.fromkeys(dir_list)).reverse()

def process_rename_directories():
    if change_everything == False:
        if change_folders_names == False:
            return

    final_list = []
    for dir in find_directories_to_rename():
        index = dir.rfind(old_name)
        last_path = dir[index:].find(r'/')
        if last_path > 0:
            destination = dir[:index+last_path]
            final_list.append(destination)
        elif index > 0:
            final_list.append(dir)

    ordered_list = list(dict.fromkeys(final_list))
    ordered_list.reverse()
    
    for dir in ordered_list:
        rename_file_or_directory(dir)

def process():
    process_file_content()
    process_rename_files()
    process_rename_directories()

def finalize():
    log_msg('Rename files script end')

def main():
    initialize()
    process()
    finalize()

main()
