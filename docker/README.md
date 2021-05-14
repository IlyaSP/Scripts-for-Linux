# scripts for work with docker

1. backup_docker_volumes.py

2. restore_docker_volume_backup.py

# 1. backup_docker_volumes.py
  Скрипт делает бэкап всех docker volume на хосте в виде tar архива и копирует по ssh на удалённую машину.
The script makes a backup of all docker volumes on the host in the form of a tar archive and copies over ssh to a remote machine.

# 2. restore_docker_volume_backup.py
  Скрипт создаёт и восстанавливает docker volumes из ранее созданных бэкопов.
 The script creates and restores docker volumes from previously created backups.
