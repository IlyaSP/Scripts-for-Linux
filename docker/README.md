# scripts for work with docker

1. backup_docker_volumes.py

2. restore_docker_volume_backup.py

3. get_list_runing_containers.py

# 1. backup_docker_volumes.py
  Скрипт делает бэкап всех docker volume на хосте в виде tar архива и копирует по ssh на удалённую машину.
Тестировалось на Ubuntu 20.04
  The script makes a backup of all docker volumes on the host in the form of a tar archive and copies over ssh to a remote machine.
Tested on Ubuntu 20.04

# 2. restore_docker_volume_backup.py
  Скрипт создаёт и восстанавливает docker volumes из ранее созданных бэкопов.
Тестировалось на Ubuntu 20.04
  The script creates and restores docker volumes from previously created backups.
Tested on Ubuntu 20.04

# 3. get_list_runing_containers.py
  Скрипт получает список запущенных контейнеров на хосте и сравнивает с эталонным списком контейнеров, если в списке запущенных контенеров не хватает контейнеров, которые указаны в эталонном списке, то скрипт выдаст ошибку.
   The script receives a list of running containers on the host and compares it with the reference list of containers, if the list of running containers does not contain enough containers that are specified in the reference list, then the script will generate an error.
