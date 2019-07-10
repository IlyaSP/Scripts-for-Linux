import os
from subprocess import call
import apt
import apt.progress
import time
import re
import shutil
from crontab import CronTab


# ssh_new_port = "2223"

def instal_app(pkg_name):
    """
    Проверяет установлено ли приложения из списка, если приложение не утсатановлено, устанавливает его.
    Checks whether the application is installed from the list, if the application is not installed, installs it.
    """
    print("\033[96m{0}\033[00m".format("=== Install App ==="))
    for i in pkg_name:
        print("{0} will be installed".format(i))

    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    for ii in pkg_name:
        pkg = cache[ii]
        if pkg.is_installed:
            print("\033[92m{0} already installed\033[00m".format(ii))
        else:
            try:
                pkg.mark_install()
            except Exception as e:
                print("\033[91m{0}\033[00m".format(e))

            try:
                cache.commit()
            except Exception as e:
                print("\033[91m{0}\033[00m".format(e))


def delete_app(del_pkg_name):
    """
    Проверяет установлено ли приложения из списка, если приложение утсатановлено, удаляет его.
    Checks whether the application is installed from the list, if the application is installed, delete it.
    """
    print("\033[96m{0}\033[00m".format("=== Delete App ==="))
    for i in del_pkg_name:
        print("{0} will be deleted".format(i))

    cache = apt.cache.Cache()
    cache.update()
    cache.open(None)
    # resolver = apt.cache.ProblemResolver(cache)
    cache.upgrade()

    for ii in del_pkg_name:
        pkg = cache[ii]
        if pkg.is_installed:
            print("\033[92m{0} already installed\033[00m".format(ii))
            try:
                pkg.mark_delete(True, purge=True)
            except Exception as e:
                print("error delete")
                print("\033[91m{0}\033[00m".format(e))

            try:
                cache.commit()
            except Exception as e:
                print("error cahce")
                print("\033[91m{0}\033[00m".format(e))
        else:
            print("\033[92m{0} - not installed\033[00m".format(ii))
            time.sleep(1)


def ssh_key(path_ssh_key):
    """
    Удаляет дефолтные ssh ключи и генерирует новые ключи ssh
    Removes default ssh keys and generates new ssh keys
    """
    print("\033[96m {0}\033[00m".format("\n=== Removes default SSH keys and generates new SSH keys ==="))
    call("update-rc.d -f ssh remove", shell="True")
    time.sleep(1)
    call("update-rc.d -f ssh defaults", shell="True")
    time.sleep(2)
    list_files = os.listdir(path_ssh_key)
    for i in list_files:
        if re.search("ssh_host_", i) is not None:
            os.mkdir(path_ssh_key + "/insecure")    # Create temp dir
            for ii in list_files:
                if re.search("ssh_host_", ii) is not None:
                    shutil.move(path_ssh_key + "/" + ii, path_ssh_key + "/insecure/" + ii)
            call("dpkg-reconfigure openssh-server", shell="True")   # generate new ssh keys
            shutil.rmtree(path_ssh_key + "/insecure/")   # Delete temp dir
            print("\033[92m{0}\033[00m".format("SSH key was add"))
            break
        else:
            print("\033[93m{0}\033[00m".format("Something went wrong"))


def config_ssh(ssh_new_port, path_ssh_config):
    """
    Настройка ssh
    SSH setup
    """
    print("\033[96m {0}\033[00m".format("\n=== Configuration SSH ==="))
    try:
        with open(path_ssh_config, "r+") as f:
            a = f.readlines()
            i = 0
            # new_port = "2223"
            list_new_param = [
                "Port {0}".format(ssh_new_port),
                "PermitRootLogin no",
                "ClientAliveInterval 900",
                "MaxAuthTries 3",
                "MaxSessions 2",
                "TCPKeepAlive no",
                "X11Forwarding no",
                "AllowAgentForwarding no"
            ]  # list of parameters to change
            list_add_param = []
            while i < len(a):
                if re.match("#Port 22", a[i]) is not None:
                    a.insert(i + 1, "Port {0}\n".format(ssh_new_port))  # Assign a new port for connection via SSH
                    i += 1
                    print("\033[92m{0}{1}\033[00m".format("New port for SSH: ", ssh_new_port))
                    list_add_param.append("Port {0}".format(ssh_new_port))

                elif re.match("Port \d+", a[i]) is not None:  # Delete all other port ssh settings
                    a.pop(i)

                elif re.match("#PermitRootLogin", a[i]) is not None:
                    a.insert(i + 1, "PermitRootLogin no\n")  # do not allow to connect via SSH as root
                    i += 1
                    print("\033[92m{0}\033[00m".format("Prohibit login ssh root"))
                    list_add_param.append("PermitRootLogin no")

                elif re.match("PermitRootLogin", a[i]) is not None:  # delete other settings
                    a.pop(i)

                elif re.match("#ClientAliveInterval", a[i]) is not None:
                    a.insert(i + 1, "ClientAliveInterval 900\n")  # Reduce the lifetime of an inactive session
                    i += 1
                    print("\033[92m{0}\033[00m".format("Reduce the lifetime of an inactive session"))
                    list_add_param.append("ClientAliveInterval 900")

                elif re.match("ClientAliveInterval", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                elif re.match("#MaxAuthTries", a[i]) is not None:
                    a.insert(i + 1, "MaxAuthTries 3\n")  # Set max number of authentication attempts
                    i += 1
                    print("\033[92m{0}\033[00m".format("maximum number of authentication attempts 3"))
                    list_add_param.append("MaxAuthTries 3")

                elif re.match("MaxAuthTries", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                elif re.match("#MaxSessions", a[i]) is not None:
                    a.insert(i + 1, "MaxSessions 2\n")  # Set max concurrent sessions
                    i += 1
                    print("\033[92m{0}\033[00m".format("maximum number of simultaneous sessions 2"))
                    list_add_param.append("MaxSessions 2")

                elif re.match("MaxSessions", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                elif re.match("#TCPKeepAlive", a[i]) is not None:
                    a.insert(i + 1, "TCPKeepAlive no\n")  # Отключаем кипэлайв ssh сессий
                    i += 1
                    print("\033[92m{0}\033[00m".format("TCPKeepAlive ssh sessions disabled"))
                    list_add_param.append("TCPKeepAlive no")

                elif re.match("TCPKeepAlive", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                elif re.match("#X11Forwarding", a[i]) is not None:
                    a.insert(i + 1, "X11Forwarding no\n")  # Отключаем возможность открывать X11Forwarding по ssh
                    i += 1
                    print("\033[92m{0}\033[00m".format("X11Forwarding ssh disabled"))
                    list_add_param.append("X11Forwarding no")

                elif re.match("X11Forwarding", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                elif re.match("#AllowAgentForwarding", a[i]) is not None:
                    a.insert(i + 1, "AllowAgentForwarding no\n")  # Отключаем проброс ключей ssh
                    i += 1
                    print("\033[92m{0}\033[00m".format("AllowAgentForwarding ssh disabled"))
                    list_add_param.append("AllowAgentForwarding no")

                elif re.match("AllowAgentForwarding", a[i]) is not None:  # Remove other settings
                    a.pop(i)
                    
                elif re.match("#DebianBanner", a[i]) is not None:
                    a.insert(i + 1, "DebianBanner no\n")  # Disable OS version publishing in ssh
                    i += 1
                    print("\033[92m{0}\033[00m".format("DebianBanner ssh disabled"))
                    list_add_param.append("DebianBanner no")

                elif re.match("DebianBanner", a[i]) is not None:  # Remove other settings
                    a.pop(i)

                i += 1

            remaining_param = list(set(list_new_param) - set(list_add_param))
            if len(remaining_param) > 0:
                for i in remaining_param:
                    a.append("{0}\n".format(i))
                    print("\033[92m'{0}' was added\033[00m".format(i))
            f.seek(0)
            f.writelines(a)
            print("\033[92m{0}\033[00m".format("SSH was configuration"))
    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))


def fail2ban_config(ssh_new_port, path_fail2ban_config):
    """
    Настройка fail2ban
    Fail2ban setup
    """
    print("\033[96m {0}\033[00m".format("\n=== Configuration Fail2ban ==="))
    if os.path.isfile(path_fail2ban_config + "jail.local"):
        try:
            os.remove(path_fail2ban_config + "jail.local")
            print(print("\033[93m{0} \033[00m".format("Old file 'jail.local' has been deleted")))

        except Exception as e:
            print("\033[91m{0}\033[00m".format(e))

    try:
        with open(path_fail2ban_config + "jail.conf", "r") as f:
            a = f.readlines()
            # print(a)
            i = 0
            while i < len(a):
                if re.match(r'\[sshd\]', a[i]) is not None:
                    sshd_start = i + 1
                    # print(sshd_start)
                    for ii in range(i + 1, len(a)):
                        if re.search(r'\[\w+\]', a[ii]) is not None:
                            sshd_end = ii
                            i = len(a)
                            break

                if i >= len(a):
                    # print("END")
                    break
                else:
                    i += 1

            for i in range(sshd_end - 1, sshd_start, -1):
                # print(a[i])
                a.pop(i)
            a.insert(sshd_start, "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n\n\n".format("enabled = true", "filter = sshd",
            "action = iptables[name=SSH, port=" + str(ssh_new_port) + ", protocol=tcp]",
            r"logpath = /var/log/fail2ban_auth.log", "findtime = 600", "maxretry = 3", "bantime = 180"))

        with open(path_fail2ban_config + "jail.local", "w") as F:
            F.writelines(a)

    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))


"""
def config_dns(path_dns):
    '''
    Настройка DNS
    DNS Setup
    '''
    print("\033[96m {}\033[00m".format("\n=== Configuration DNS ==="))
    call("chattr -i /etc/resolv.conf", shell="True")    # Разблокировка файла resolv.conf
    try:
        with open(path_dns, "r+") as f:
            a = f.readlines()
            for i in range(len(a)):
                if a[i].startswith("nameserver"):
                    temp = a[i]
                    a.pop(i)
                    a.insert(i, "#{0}".format(temp))
                    continue
                elif a[i].startswith("search"):
                    temp = a[i]
                    a.pop(i)
                    a.insert(i, "#{0}".format(temp))
            a.append("nameserver 1.1.1.1\n")
            a.append("nameserver 1.0.0.1\n")
            f.seek(0)
            f.writelines(a)
        call("chattr +i /etc/resolv.conf",
             shell="True")  # Блокируем файл, чтобы не сбрасывались настройки после перезагрузки
        print("\033[92m{}\033[00m".format("DNS was configuration"))
    except Exception as e:
        print("\033[91m{}\033[00m".format(e))
"""


def config_terminal(path_bash):
    """
    Настройка  терминала bash
    Bash terminal setup
    """
    print("\033[96m {}\033[00m".format("\n=== Configuration  terminal BASH ==="))
    new = r'\[\e[1;91m\]\u@\[\e[m\]\[\e[1;93m\]\h\[\e[m\] \[\e[1;34m\]\W\[\e[m\] \[\e[0;31m\]\$ \[\e[m\]\[\e[0;92m\]'
    try:
        with open(path_bash, "r+") as f:
            a = f.readlines()
            i = 0
            while i < len(a):
                if re.search(r'color_prompt" = yes ]; then', a[i]) is not None:
                    print("\033[92m{0}\033[00m".format("Change color terminal"))
                    a.insert(i + 1, "    PS1={0}{1}{2}\n".format("'", new, "'"))
                    a.pop(i + 2)
                    i += 1
                elif re.search(r"alias ll='ls -alF'", a[i]) is not None:  # Add alias
                    print("\033[92m{0}\033[00m".format("Add alias ll='ls -alhF"))
                    a.pop(i)
                    a.insert(i, "{0}\n".format(r"alias ll='ls -alhF'"))
                    i += 1
                elif re.search(r"alias l='ls -CF'", a[i]) is not None:  # Add alias
                    print("\033[92m{0}\033[00m".format("Add alias l='ls -lh'"))
                    a.pop(i)
                    a.insert(i, "{0}\n".format(r"alias l='ls -lh'"))
                    i += 1
                else:
                    i += 1

            f.seek(0)
            f.writelines(a)
            print("\033[92m{0}\033[00m".format("Setup is complete, changes will take effect after a reboot or "
                                           "command execution: 'source ~/.bashrc'"))
    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))


def optimize_sys():
    """
    Оптимизация системы. Если есть свободная оперативная память, то использовать её, а не SWAP
    System optimization. If there is free RAM, then use it, not SWAP
    :return:
    """
    path1 = "/etc/sysctl.conf"
    swapp = 0
    try:
        with open(path1, "r+") as f:
            a = f.readlines()
            for i in range(len(a)):
                if a[i].startswith("vm.swappiness=0"):
                    swapp = 1
                    break
                else:
                    continue
            if swapp == 0:
                a.append("vm.swappiness=0\n")    # swap file will be used only after the end of the operational
            f.seek(0)
            f.writelines(a)
    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))


def clear_tmp(time_exec, user, number_day):
    """
    Функция добавления задания в crontab для удаления временных файлов из /tmp
    The function of adding a job in crontab to delete temporary files from / tmp
    time_exec = 50 14 * * *
    minute------|   | |
    hour------------| |
    day of month------|
    month
    day of week
    """
    print("\033[96m {0}\033[00m".format("\n=== Configuration  rules clear files from /tmp ==="))
    try:
        users_cron = CronTab(user)
        job = users_cron.new(command='find /tmp -mtime +{0} -delete'.format(number_day),
                             comment='delete files older than {0} days'.format(number_day))
        job.setall(time_exec)
        users_cron.write()
        print("\033[92m Task in crontab was added. Files older than {0} will be delete\033[00m".format(number_day))
    except Exception as e:
        print("\033[91m{0}\033[00m".format(e))


def ugrade_sys():
    """
    Обновление системы
    Upgrade system
    """
    a = str(input('Upgrade system (Y/N): '))
    if a == "Y":
        cache = apt.Cache()
        cache.update()
        cache.open(None)
        cache.upgrade()
        cache.upgrade(True)
        try:
            cache.commit()
        except Exception as e:
            print("\033[91m{}\033[00m".format(e))
        print("\033[92m{0}\033[00m".format("Setup complete, reboot required"))
    else:
        print("\033[92m{0}\033[00m".format("Setup complete"))


if __name__ == "__main__":
    ssh_new_port = "2223"
    #instal_app(pkg_name=["openssh-server", "net-tools", "remmina", "ubuntu-restricted-extras", "gnome-tweaks", "clamav",
                         #"clamtk", "clamav-unofficial-sigs", "rkhunter", "python3-crontab", "libpam-pwquality"
    # ,"fail2ban"])
    # time.sleep(2)
    #delete_app(del_pkg_name=["pitivi", "empathy", "empathy-common", "vinagre", "rdesktop", "xinetd"])
    #time.sleep(2)
    #ssh_key(path_ssh_key = "/etc/ssh")
    #time.sleep(2)
    #config_ssh(path_ssh_config="/etc/ssh/sshd_config", ssh_new_port)
    config_ssh(ssh_new_port, path_ssh_config="/etc/ssh/sshd_config")
    #time.sleep(2)
    fail2ban_config(ssh_new_port, path_fail2ban_config="/etc/fail2ban/")
    time.sleep(2)
    #config_terminal(path_bash=os.getenv("HOME") + r"/.bashrc")
    #time.sleep(2)
    #optimize_sys()
    #time.sleep(2)
    #clear_tmp(time_exec='50 14 * * *', user='root', number_day='7')
    # time.sleep(2)
    #ugrade_sys()


