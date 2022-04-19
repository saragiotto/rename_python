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

## Find Replace interno dos arquivos
grep_old_name_in_files_cmd = 'grep -rl $ .'
sed_regex_cmd = 's/$/$/g'
sed_file_cmd = 'sed -i \"\" -e \"$\" $'
git_diff_color_cmd = 'git diff --color | cat'
git_restore_cmd = 'git restore -- .'

## Rename do nome dos arquivos
find_files_to_rename_cmd = 'find . -type f -name \"*$*\"'

## Rename de diretorios
find_directories_to_rename_cmd = 'find . -type d | grep $'

def log_msg(msg):
    if verbose_mode:
        print(msg)

# Detecta se o script está em modo dry_run, somente apresenta as alterações mas não realiza nada nos arquivos e diretórios
def detect_dry_run_and_verbose(arg_list):
    global dry_run, verbose_mode, help_mode
    result = []
    for arg in arg_list:
        if arg == verbose_param:
            verbose_mode = True
        elif arg == dry_run_param:
            dry_run = True
        else:
            result.append(arg)

    return result

# Valida se os inputs estão corretos
def validate_inputs(arg_list):
    global old_name, new_name, script_name
    script_name = arg_list[0]
    old_name = arg_list[1]
    new_name = arg_list[2]

    if len(old_name) == 0:
        sys.exit('Old name empty')

    if len(new_name) == 0:
        sys.exit('New name empty')

def initialize():
    global old_name, new_name, script_name, sed_regex_cmd, sed_file_cmd

    arg_list = detect_dry_run_and_verbose(sys.argv)

    log_msg('Rename files script initialize\n')
    if dry_run:
        log_msg('*** Dry run detected, no changes will be made ***\n')

    validate_inputs(arg_list)

    sed_regex_cmd = sed_regex_cmd.replace('$', old_name, 1).replace('$', new_name, 1)
    sed_file_cmd = sed_file_cmd.replace('$', sed_regex_cmd, 1)

    log_msg('Old name: ' + old_name)
    log_msg('New name: ' + new_name + '\n')

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
    for file in find_files_to_rename():
        rename_file_or_directory(file)

def find_directories_to_rename():
    cmd = find_directories_to_rename_cmd.replace('$', old_name, 1)
    return exec_sheel_cmd(cmd)

def remove_duplicate_and_reverse_order(dir_list):
    return list(dict.fromkeys(dir_list)).reverse()

def process_rename_directories():
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

def printHelp():
    print('Rename files content, files name and folders recursively')
    print('v1.0')
    print('Leonardo Saragiotto - leonardo.saragiotto@gmail.com')
        
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
