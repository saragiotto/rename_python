# Rename Script

Rename files content, files name and folders recursivily.

### Usage

```bash
$ python3 rename.py oldName=NameToFind newName=NameToReplace
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
`src/controler/NewLongNameController/NewLongNameControllerHelper/NewLongNameHelper.js`
