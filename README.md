# Intuitionistic Backup

[English](./README.md) | [中文](./README_CN.md)

## Platform

-   Linux

## Usage

Install & Run:

```sh
git clone https://github.com/JohanChane/intuit-backup.git --depth 1
# config ~/.config/intuitbackup/config.toml
cd intuit-backup
sudo ./intuitbackup      # Because backing up some system files requires root privileges, it is best to use sudo
```

Files related to intuit-backup:

-   config: ~/.config/intuitbackup/config.toml
    -   dest_dir: Directory where the backup archive files are stored.
    -   record_dir: Directory containing the record files of files to be backed up.
    -   info_dir: Directory containing system information files to be backed up. The `info_cmd` file in this directory is used to generate the necessary system information.
    -   password: Password for extracting the backup archive. Keep it safe.

Options:

-   backup: Back up files listed in a record file.
-   extract: Extract a backup archive.
-   restore: Restore files from a backup archive. Note: This will overwrite existing files.
-   list_files: List the files in a backup archive.
-   check_record: Check the files listed in a record file. For example: to verify if the files exist.
-   cat_record: View the contents of a record file.
-   backup_info: Backup system information. About `cmd_info`.

For example: `~/IntuitBackup/Records/sys`。Lines starting with `#` are comments.

```
# ## System
/etc/fstab
/boot/grub/grub.cfg
/etc/default/grub
/etc/mkinitcpio.conf
/etc/sudoers
/etc/sudoers.d/my
/etc/environment
/usr/local/bin
/etc/hosts

# ## User
~/.profile
~/.xprofile
~/.xinitrc
~/.local/bin
~/.config/systemd/user
```

For example: `~/IntuitBackup/Records/apps`

```
# ## zsh
~/.zshrc

# ## nvim
~/.config/nvim
```

## Doc

[Doc](./Doc)
