import time


# TODO add redis
# TODO fix ban/unban lock
class F2BParser:
    def __init__(self, f2b_logfile_path, ips_file_path):

        self.f2b_logfile_path = f2b_logfile_path
        self.ips_file_path = ips_file_path

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
        for ip in banned_ips:
            if ip not in current_ips:
                print(f"Adding {ip} to list")
                self.__add_ip(ip=ip)

        unbanned_ips = self.__get_unbanned_ips_from_f2b_log()
        for ip in unbanned_ips:
            if ip in current_ips:
                print(f"Removing {ip} from list")
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
        banned_ips_list = [line.split()[-1] for line in lines if 'Ban' in line and 'Restore' not in line]
        return banned_ips_list

    def __get_unbanned_ips_from_f2b_log(self):
        lines = self.__get_f2b_log()
        unbanned_ips_list = [line.split()[-1] for line in lines if 'Unban' in line]
        return unbanned_ips_list

    def __delete_ip(self, ip: str):
        lines = self.__get_ips_log()
        with open(self.ips_file_path, "w") as f:
            for line in lines:
                if line.strip("\n") != ip:
                    f.write(line + '\n')

    def __add_ip(self, ip: str):
        with open(self.ips_file_path, 'a') as f:
            f.write(ip + '\n')


parser = F2BParser(f2b_logfile_path='fail2ban.log', ips_file_path='tmp.txt')
parser.test()
