import time
import datetime
from utils.utils import get_redis, get_option_from_config


class F2BParser:
    def __init__(self, f2b_logfile_path=None, ips_file_path=None):
        self.redis = get_redis()
        self.f2b_logfile_path = get_option_from_config(
            ["F2B_logfile_path"]) if f2b_logfile_path is None else f2b_logfile_path
        self.ips_file_path = get_option_from_config(["IPs_logfile_path"]) if ips_file_path is None else ips_file_path
        print(self.f2b_logfile_path, 1)
        self.main_loop()

    def main_loop(self):
        while True:
            self.__update_ips_logfile()
            time.sleep(3)

    def test(self):
        pass

    def __update_ips_logfile(self):
        current_ips = self.__get_ips_log()
        banned_ips = self.__get_banned_ips_from_f2b_log()
        unbanned_ips = self.__get_unbanned_ips_from_f2b_log()

        for ip in banned_ips:
            if ip not in current_ips:
                try:
                    if unbanned_ips[ip] < banned_ips[ip]:
                        self.__add_ip(ip=ip)
                except KeyError:
                    self.__add_ip(ip=ip)
        for ip in unbanned_ips:
            if ip in current_ips:
                try:
                    if unbanned_ips[ip] > banned_ips[ip]:
                        self.__delete_ip(ip=ip)
                except KeyError:
                    self.__delete_ip(ip=ip)

    def __get_f2b_log(self):
        with open(self.f2b_logfile_path, 'r') as f:
            lines = f.readlines()
        return lines

    def __get_ips_log(self):
        try:
            with open(self.ips_file_path, 'r') as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            return []
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

    def __delete_ip(self, ip: str):
        print(f"Removing {ip} from list")
        lines = self.__get_ips_log()
        with open(self.ips_file_path, "w") as f:
            for line in lines:
                if line.strip("\n") != ip:
                    f.write(line + '\n')

    def __add_ip(self, ip: str):
        print(f"Adding {ip} to list")
        with open(self.ips_file_path, 'a') as f:
            f.write(ip + '\n')


parser = F2BParser()
