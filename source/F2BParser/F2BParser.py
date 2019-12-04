import threading
import time
from source.utils.utils import get_redis, get_option_from_config, convert_str_datetime_to_ts


class F2BParser:
    """
    Class for scanning f2b logfile and adding/removing data to redis db
    """

    def __init__(self, f2b_logfile_path=None, db=0):
        """

        :param f2b_logfile_path: [Optional] Fail2Ban logfile path
        :param db: [Optional] redis database number
        """
        self.redis = get_redis(db=db)
        self.f2b_logfile_path = get_option_from_config(
            ["F2B_logfile_path"]) if f2b_logfile_path is None else f2b_logfile_path
        self.running = True

    def main_loop(self):
        """
        Main loop, where constant monitoring happens
        :return: None
        """
        thread = threading.Thread(target=self.__update_ips_logfile, args=())
        thread.start()

    def __update_ips_logfile(self):
        """
        Add/remove with ip addresses from redis db
        :return: None
        """
        while self.running:
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
            time.sleep(1)

    def __add_ip(self, ip: str, ts: float):
        """
        Add ip to redis db
        :param ip: string, ip address
        :param ts: float, timestamp, when ip was added to f2b log
        :return: None
        """
        print(f"Adding {ip}")
        self.redis.set(ip, ts)

    def __delete_ip(self, ip: str):
        """
        Delete ip from redis db
        :param ip: string, ip address
        :return: None
        """
        print(f"Deleting {ip}")
        self.redis.delete(ip)

    def __get_f2b_log(self):
        """
        Get f3b logfile
        :return: list, f2b logfile lines
        """
        with open(self.f2b_logfile_path, 'r') as f:
            lines = f.readlines()
        return lines

    def __get_banned_ips_from_f2b_log(self):
        """
        Get banned ip addresses from f2b logfile
        :return: list, banner ip addresses
        """
        lines = self.__get_f2b_log()
        banned_ips_list = dict()
        for line in lines:
            if 'Ban' in line and 'Restore' not in line:
                ip_timestamp = str(line.split()[0] + " " + line.split()[1])
                ip_timestamp = convert_str_datetime_to_ts(ip_timestamp)
                banned_ips_list[line.split()[-1]] = ip_timestamp
        return banned_ips_list

    def __get_unbanned_ips_from_f2b_log(self):
        """
        Get unbanned ip addresses from f2b logfile
        :return: list, unbanner ip addresses
        """
        lines = self.__get_f2b_log()
        unbanned_ips_list = dict()
        for line in lines:
            if "Unban" in line:
                ip_timestamp = str(line.split()[0] + " " + line.split()[1])
                ip_timestamp = convert_str_datetime_to_ts(ip_timestamp)
                unbanned_ips_list[line.split()[-1]] = ip_timestamp
        return unbanned_ips_list


if __name__ == "__main__":
    parser = F2BParser()
