#!/usr/bin/python3

import random
import re
import subprocess


def fail2ban_change_timers(path_fail2ban_config):
    try:
        with open(path_fail2ban_config + "jail.local", "r+") as f:
            a = f.readlines()
            i = 0
            while i < len(a):
                if re.match(r'\[sshd\]', a[i]) is not None:
                    sshd_start = i + 1
                    for ii in range(i + 1, len(a)):
                        if re.search(r'\[\w+\]', a[ii]) is not None:
                            sshd_end = ii
                            i = len(a)
                            break

                if i >= len(a):
                    break
                else:
                    i += 1

            for i in range(sshd_start, sshd_end):
                # a.pop(i)
                if re.match("findtime =", a[i]) is not None:
                    a.pop(i)
                    a.insert(i, "{0}\n".format(r"findtime =" + str(int(random.randrange(300, 1200, 120)))))
                elif re.match("maxretry =", a[i]) is not None:
                    # print(a[i])
                    a.pop(i)
                    a.insert(i, "{0}\n".format(r"maxretry =" + str(int(random.randint(3, 7)))))
                elif re.match("bantime =", a[i]) is not None:
                    # print(a[i])
                    a.pop(i)
                    a.insert(i, "{0}\n".format(r"bantime =" + str(int(random.randrange(600, 18000, 300)))))

            # print (sshd_start)
            f.seek(0)
            f.writelines(a)

    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))

    try:
        subprocess.check_call("service fail2ban restart", shell=True)
        print("The service fail2ban has been restarted")

    except Exception as e:
        print("Error")
        print(e)


if __name__ == "__main__":
    print("Start fail2ban change config")
    path_fail2ban_config = "/etc/fail2ban/"
    fail2ban_change_timers(path_fail2ban_config)

