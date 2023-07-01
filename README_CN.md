# Intuitionistic backup

[English](./README.md) | [中文](./README_CN.md)

## 平台

-   Linux

## 使用

安装 & 运行:

```sh
git clone https://github.com/JohanChane/intuit-backup.git --depth 1
# 配置 ~/.cofnig/intuitbackup/config.toml
cd intuit-backup
./intuitbackup
```

intuit-backup 的相关文件:

-   config: ~/.config/intuitbackup/config.toml
    -   dest_dir: 存放备份的文件的压缩包。
    -   record_dir: 存放需要备份的文件的记录文件。
    -   info_dir: 存放需要备份的系统信息。还有其下的 info_cmd 文件用于生成需要备份的系统信息。
    -   password: 压缩包的解压密码。注意保管。

选项:

-   backup: 备份一个 record 记录的文件。
-   extract: 解压一个备份压缩包。
-   restore: 从一个备份压缩包中恢复文件。注意: 会覆盖已有的文件。
-   list_files: 列出备份压缩包的文件。
-   check_record: 检查 record 记录的文件。比如: 文件是否存在。
-   cat_record: 查看 record 文件的内容
-   gen_info: 生成系统信息。

For example: `~/IntuitBackup/Records/confs`

`#` 开头是注释。

```
# ## IntuitBackup
# 备份 gen_info 生成的系统信息
~/IntuitBackup/Info
~/.config/intuitbackup
~/IntuitBackup/Records

# ## system config files
/etc/fstab
/boot/grub/grub.cfg
/etc/default/grub
/etc/sudoers
/etc/environment
~/.xinitrc
~/.xprofile
~/.profile

# ## zsh
~/.zshrc
```

## Doc

[Doc](./Doc)
