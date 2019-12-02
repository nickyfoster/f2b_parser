import time
import datetime
from utils.utils import get_redis, get_option_from_config
import json


class F2BParser:
    def __init__(self, f2b_logfile_path=None, ips_file_path=None):
        self.redis = get_redis()
        self.f2b_logfile_path = get_option_from_config(
            ["F2B_logfile_path"]) if f2b_logfile_path is None else f2b_logfile_path
        self.main_loop()

    def main_loop(self):
        while True:
            self.__update_ips_logfile()
            time.sleep(1)

    def __update_ips_logfile(self):
        banned_ips = self.__get_banned_ips_from_f2b_log()
        unbanned_ips = self.__get_unbanned_ips_from_f2b_log()
        for ip in banned_ips:
            if not self.redis.exists(ip):
                try:
                    if unbanned_ips[ip] < banned_ips[ip]:
                        self.__add_ip(ip=ip, ts=banned_ips[ip])
                except KeyError:
                    self.__add_ip(ip=ip, ts=banned_ips[ip])
        for ip in unbanned_ips:
            if self.redis.exists(ip):
                try:
                    if unbanned_ips[ip] > banned_ips[ip]:
                        self.__delete_ip(ip=ip)
                except KeyError:
                    self.__delete_ip(ip=ip)

    def __add_ip(self, ip, ts):
        print(f"Adding {ip}")
        self.redis.set(ip, ts)

    def __delete_ip(self, ip):
        print(f"Deleting {ip}")
        self.redis.delete(ip)

    def __get_f2b_log(self):
        with open(self.f2b_logfile_path, 'r') as f:
            lines = f.readlines()
        return lines

    def __get_banned_ips_from_f2b_log(self):
        lines = self.__get_f2b_log()
        banned_ips_list = dict()
        for line in lines:
            if 'Ban' in line and 'Restore' not in line:
                ip_timestamp = str(line.split()[0] + " " + line.split()[1])
                ip_timestamp = time.mktime(datetime.datetime.strptime(ip_timestamp, "%Y-%m-%d %H:%M:%S,%f").timetuple())
                banned_ips_list[line.split()[-1]] = ip_timestamp
        return banned_ips_list

    def __get_unbanned_ips_from_f2b_log(self):
        lines = self.__get_f2b_log()
        unbanned_ips_list = dict()
        for line in lines:
            if "Unban" in line:
                ip_timestamp = str(line.split()[0] + " " + line.split()[1])
                ip_timestamp = time.mktime(datetime.datetime.strptime(ip_timestamp, "%Y-%m-%d %H:%M:%S,%f").timetuple())
                unbanned_ips_list[line.split()[-1]] = ip_timestamp
        return unbanned_ips_list


parser = F2BParser()
