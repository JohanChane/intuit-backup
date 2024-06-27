#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time
import toml
from dataclasses import dataclass

@dataclass
class Config:
    dest_dir: str
    record_dir: str
    info_dir: str
    password: str

class IntuitBackup():
    def __init__(self):
        self.__username = os.getenv('SUDO_USER') or os.getenv('USER')
        if not self.__username:
            sys.stderr.write("Failed to get username\n")
            sys.exit(1)
        elif self.__username == "root":
            self.__home_dir = "/root"
        else:
            self.__home_dir = os.path.join("/home", self.__username)

        config_path = os.path.join(self.__home_dir, ".config", "intuitbackup", "config.toml")
        
        with open(config_path, 'r') as file:
            config_dict = toml.load(file)
        self.__config = Config(**config_dict)
        
        self.__config.dest_dir = self.__expanduser(self.__config.dest_dir)
        self.__config.record_dir = self.__expanduser(self.__config.record_dir)
        self.__config.info_dir = self.__expanduser(self.__config.info_dir)

        if os.geteuid() != 0:
            os.makedirs(self.__config.dest_dir, exist_ok=True)
            os.makedirs(self.__config.record_dir, exist_ok=True)
            os.makedirs(self.__config.info_dir, exist_ok=True)

        return

    def backup(self, record_name):
        archive_name = record_name + '-' + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + ".tar.gz"
        archive_path = os.path.join(self.__config.dest_dir, archive_name)
        record_path = os.path.join(self.__config.record_dir, record_name)
        files = self.__get_files(record_path)
        self.backup_helper(archive_path, files)
        print(f'Backup successfully: "{archive_path}"')

    def backup_helper(self, archive_path, files):
        files_with_quote = []
        for f in files:
            files_with_quote.append(f'"{f}"')
        #cmd = f'tar -acvP -f "{archive_path}" {" ".join(files_with_quote)}'
        cmd = f"tar -acvP -f - {' '.join(files_with_quote)} | gpg --batch --yes --symmetric --cipher-algo AES256 --passphrase '{self.__config.password}' --output '{archive_path}.gpg'"
        os.system(cmd)

    def check_record(self, record_name):
        record_path = os.path.join(self.__config.record_dir, record_name)
        files = self.__get_files(record_path)
        for f in files:
            if not os.path.exists(f):
                print(f'"{f}" is not exist.')

    def cat_record(self, record_name):
        record_path = os.path.join(self.__config.record_dir, record_name)
        files = self.__get_files(record_path)
        print("\n".join(files))

    def extract(self, archive_name):
        oldwd = os.getcwd()
        os.chdir(self.__config.dest_dir)

        file_name_no_suffix = archive_name.split(".")[0]
        os.mkdir(file_name_no_suffix)
        archive_path = os.path.join(self.__config.dest_dir, archive_name)
        #cmd = f'tar -xv -p --same-owner -f "{archive_path}" -C "{file_name_no_suffix}"'
        cmd = f"gpg --batch --yes --passphrase '{self.__config.password}' -d {archive_path} | tar -xv -p --same-owner -f - -C '{file_name_no_suffix}'"
        os.system(cmd)

        os.chdir(oldwd)

    def restore(self, archive_name):
        archive_path = os.path.join(self.__config.dest_dir, archive_name)
        #cmd = f'tar -xvP -p --same-owner -f {archive_path}'
        cmd = f"gpg --batch --yes --passphrase '{self.__config.password}' -d {archive_path} | tar -xvP -p --same-owner -f -"
        os.system(cmd)

    def list_files(self, archive_name):
        archive_path = os.path.join(self.__config.dest_dir, archive_name)
        #cmd = f'tar -tv -f {archive_path}'
        cmd = f"gpg --batch --yes --passphrase '{self.__config.password}' -d {archive_path} | tar -tv -f -"
        os.system(cmd)
    
    def backup_info(self):
        oldwd = os.getcwd()
        os.chdir(self.__config.info_dir)

        cmd = f'cd "{self.__config.info_dir}"; ./info_cmd'
        print(cmd)
        os.system(cmd)

        os.chdir(oldwd)

        record_name = "cmd_info"
        archive_name = record_name + '-' + time.strftime('%Y%m%d_%H%M%S', time.localtime()) + ".tar.gz"
        archive_path = os.path.join(self.__config.dest_dir, archive_name)
        self.backup_helper(archive_path, [self.__config.info_dir])
        print(f'Backup successfully: "{archive_path}"')

    def get_dest_dir(self):
        return self.__config.dest_dir
    def get_record_dir(self):
        return self.__config.record_dir
    def get_username(self):
        return self.__username
    def get_home_dir(self):
        return self.__home_dir

    def __get_files(self, record_path):
        # get files from the record
        files = []
        with open(record_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                files.append(self.__expanduser(line))
        return files

    def __expanduser(self, path):
        if path.startswith("~"):
            return self.__home_dir + path[1:]
        return path
