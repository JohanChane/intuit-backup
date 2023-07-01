# Intuitionistic backup

Language: [English](./README.md) | [中文](./README_CN.md)

## Platform

-   Linux

## Usage

Install & Start:

```sh
git clone https://github.com/JohanChane/intuit-backup.git
cd intuit-backup
./intuitbackup
```

Files related to intuit-backup:

-   config: ~/.config/intuitbackup/intuitbackup.conf
    -   dest_dir: Directory to store backup files in compressed format.
    -   record_dir: Directory to store the record files of files to be backed up.
    -   info_dir: Directory to store system information to be backed up. It also contains info_cmd files for generating system information to be backed up.

Options:

-   backup: Backup a file recorded in the record file.
-   extract: Extract a backup compressed file.
-   restore: Restore files from a backup compressed file.
-   list_files: List the files in a backup compressed file.
-   check_record: Check the record file. For example, whether the file exists.
-   cat_record: View the contents of the record file.
-   backup_info: Backup system information.
