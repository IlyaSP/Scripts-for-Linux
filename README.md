# Scripts-for-Linux
# scripts to configure and work with linux

1.config_new_linux.py;

2.fail2ban_change_timer.py;

# 1. config_new_linux.py
  Скрипт предназначен для первичной настройки ОС linux. В него входит установка различных пакетов, удаление
не нужных приложений, настройка SSH, настройка терминала, оптимизация системы, настройка Fail2ban и другое. Перед использованием
требуется установка пакета "python-crontab". Запускаться должен под пользователем root. Тестировался на ОС Ubintu 18.04 и 
OS Parrot 4.19

  The script is intended for initial configuration of the linux OS. This includes installing various packages, removing
unnecessary applications, SSH setup, terminal setup, system optimization, Fail2ban setup and more. Before use
Installing the "python-crontab" package is required. It should run as root. Tested on OS Ubintu 18.04 and
OS Parrot 4.19

# 2. fail2ban_change_timer.py
  Скрипт предназначен для изменений параметров приложения fail2ban. Запускается через crontab.
Тестировался на ОС Ubintu 18.04 и OS Parrot 4.19, версия fail2ban = 0.10.2

  The script is intended for changing the parameters of the fail2ban application. Runs through crontab.
Tested on OS Ubintu 18.04 and OS Parrot 4.19, version fail2ban = 0.10.2
