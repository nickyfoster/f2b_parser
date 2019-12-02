import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import unittest
import time
import os
from F2BParser.F2BParser import F2BParser
from test.env import F2B_LOGFILE, TMP_F2B_LOGFILE
from utils.utils import get_redis


class TestRedis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.redis_test_db_number = 14
        cls.F2bParser = F2BParser(f2b_logfile_path=TMP_F2B_LOGFILE, db=cls.redis_test_db_number)
        cls.redis = get_redis(db=cls.redis_test_db_number)
        cls.redis.flushall()
        cls.generate_f2b_logfile(cls)

    def test_001_add_banned_ips(self):
        self.F2bParser.main_loop()
        time.sleep(1)
        self.assertEqual(True, self.redis.exists("0.0.0.0"))
        self.assertEqual(True, self.redis.exists("0.0.0.1"))

    def test_002_remove_unbanned_ips(self):
        self.update_f2b_logfile()
        time.sleep(1)
        self.assertEqual(False, self.redis.exists("0.0.0.1"))

    def test_003_clean_up(self):
        self.redis.flushall()
        os.remove(TMP_F2B_LOGFILE)
        self.F2bParser.running = False

    def generate_f2b_logfile(self):
        with open(TMP_F2B_LOGFILE, "w") as tmp_f2b_logfile:
            with open(F2B_LOGFILE, 'r') as f2b_logfile:
                lines = f2b_logfile.read().splitlines()
                for line in lines:
                    tmp_f2b_logfile.write(line + '\n')

    def update_f2b_logfile(self):
        new_banned_ip = "2069-01-01 00:00:05,000 fail2ban.actions        [14888]: NOTICE  [sshd] Unban 0.0.0.1\n"
        with open(TMP_F2B_LOGFILE, 'a+') as f:
            f.write(new_banned_ip)
