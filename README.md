# Rename Script

Rename files content, files name and folders recursively.

### Usage

```bash
$ python3 /Path/To/rename.py oldNameToFind newNameToReplace
```

#### Arguments

- -fc        Changes only files content
- -fn        Changes only files names
- -dn        Changes only directories names

- --dry-run  No changes will be made, only printed to sysout.
- -v         Super detailed information and all changes are printed on the terminal.

If none of the above arguments is informed, all the changes will be executed.

Ex:

```bash
$ python3 /Path/To/rename.py OldControllerName NewControllerName -v
```

The same effect occur with this command
```bash
$ python3 /Path/To/rename.py OldControllerName NewControllerName -v -fc -fn -dn
```

This command will print all detected changes but none will be applied

```bash
$ python3 /Path/To/rename.py OldControllerName NewControllerName -v --dry-run
```

### Execution Process

- Find and replace all files content that match given string
- Find and replace all files name that match given string
- Find and replace all folders and subfolders that match given string, from the nested level all the way up until the top folder

This steps will occur in this order.

Ex.
Given this folder and file location:
`src/controller/OldNameController/OldNameControllerHelper/OldNameHelper.js`

After the execution, the result will be this:
`src/controller/NewLongNameController/NewLongNameControllerHelper/NewLongNameHelper.js`

## Add Texto to Fire Hooks

This should fire some new webhooks.
