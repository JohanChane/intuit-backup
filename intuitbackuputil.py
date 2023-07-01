#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, configparser

class IntuitBackup():
    def __init__(self):
        self.__username = os.getenv('SUDO_USER') or os.getenv('USER')
        if self.__username == "root":
            self.__home_dir = "/root"
        else:
            self.__home_dir = os.path.join("/home", self.__username)

        config_path = os.path.join(self.__home_dir, ".config", "intuitbackup", "intuitbackup.conf")
        config = configparser.ConfigParser()
        config.read(config_path)
        self.__dest_dir = config.get("base", "dest_dir").strip()
        if self.__dest_dir.startswith("~"):
            self.__dest_dir = self.__home_dir + self.__dest_dir[1:]
        self.__record_dir = config.get("base", "record_dir").strip()
        if self.__record_dir.startswith("~"):
            self.__record_dir = self.__home_dir + self.__record_dir[1:]
        self.__info_dir = config.get("base", "info_dir").strip()
        if self.__info_dir.startswith("~"):
            self.__info_dir = self.__home_dir + self.__info_dir[1:]

    def backup(self, record_name):
        archive_name = record_name + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + ".tar.gz"
        archive_path = os.path.join(self.__dest_dir, archive_name)

        record_path = os.path.join(self.__record_dir, record_name)
        files = self.__get_files(record_path)
        files_with_quote = []
        for f in files:
            files_with_quote.append(f'"{f}"')
        cmd = f'tar -cvP -f "{archive_path}" {" ".join(files_with_quote)}'
        os.system(cmd)
        print(f'Backup successfully: "{archive_path}"')

    def check_record(self, record_name):
        record_path = os.path.join(self.__record_dir, record_name)
        files = self.__get_files(record_path)
        for f in files:
            if not os.path.exists(f):
                print(f'"f" is not exist.')

    def cat_record(self, record_name):
        record_path = os.path.join(self.__record_dir, record_name)
        files = self.__get_files(record_path)
        print("\n".join(files))

    def extract(self, archive_name):
        oldwd = os.getcwd()
        os.chdir(self.__dest_dir)

        file_name_no_suffix = archive_name.split(".")[0]
        os.mkdir(file_name_no_suffix)
        archive_path = os.path.join(self.__dest_dir, archive_name)
        cmd = f'tar -xv -f "{archive_path}" -C "{file_name_no_suffix}"'
        os.system(cmd)

        os.chdir(oldwd)

    def restore(self, archive_name):
        archive_path = os.path.join(self.__dest_dir, archive_name)
        cmd = f'tar -xvP -f {archive_path}'
        os.system(cmd)

    def list_files(self, archive_name):
        archive_path = os.path.join(self.__dest_dir, archive_name)
        cmd = f'tar -tv -f {archive_path}'
        os.system(cmd)
    
    def backup_info(self):
        oldwd = os.getcwd()
        os.chdir(self.__info_dir)

        cmd = f'cd "{self.__info_dir}"; ./info_cmd'
        print(cmd)
        os.system(cmd)

        os.chdir(oldwd)

    def get_dest_dir(self):
        return self.__dest_dir
    def get_record_dir(self):
        return self.__record_dir
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
                elif line.startswith("~"):
                    line = self.__home_dir + line[1:]
                files.append(line)
        return files
    
