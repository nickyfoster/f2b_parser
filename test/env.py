from pathlib import Path

TEST_HOME = Path(__file__).parents[0]
RESOURCES = TEST_HOME / 'resources'
F2B_LOGFILE = RESOURCES / 'test_fail2ban.log'
TMP_F2B_LOGFILE = RESOURCES / 'tmp_fail2ban.log'