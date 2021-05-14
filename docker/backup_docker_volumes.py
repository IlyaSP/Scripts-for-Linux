import os
import paramiko
import scp
import tarfile
import glob


def get_list_docker_volume():
   """Получение списка и точек монтирования Volume"""

   stream = os.popen('docker volume ls --format "{{.Name}}: {{.Mountpoint}}"')
   dict_volume_list = {}
   for i in stream.readlines():
      new_element = i.replace('\n','').split(':')
      dict_volume_list[new_element[0].strip()] = new_element[1].strip()

   return (dict_volume_list)


def create_backup_volume(dict_volume_list):
    """Создание архивов volume"""
    for vol, dir in dict_volume_list.items():
      print('Start backup volume {0}'.format(vol))
      tar_name = '{0}.tar'.format(vol)
      with tarfile.open(tar_name, 'x') as tar:    # Архив будет создан, только в случае, если его нет в данной директории
         for i in os.listdir(dir):
            print('Add file/directory "{0}" to archive'.format(i))
            tar.add('{0}/{1}'.format(dir, i), arcname=i)


def copy_backup_to_server(server, port, user, password):
   """Копирование архивов с бэкапом вольюмов на удалённый сервер"""

   ssh = paramiko.SSHClient()
   ssh.load_system_host_keys()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(server, port, user, password)

   # SCPCLient takes a paramiko transport as an argument
   scp_connect = scp.SCPClient(ssh.get_transport())
   files_to_copy = (glob.glob('*.tar'))
   for file in files_to_copy:
      print('Copy "{0}" to {1}'.format(file, server))
      scp_connect.put(file, remote_path='/home/{0}/backup_vol/{1}'.format(user, file))
      #scp_connect.put(file)

   scp_connect.close()
   ssh.close()

if __name__ == '__main__':
   path_temp_folder = '/tmp_folder_docker_volume'
   dict_volume_list = get_list_docker_volume()
   print(dict_volume_list)
   create_backup_volume(dict_volume_list)
   copy_backup_to_server(server="192.168.108.132", port=22, user="bobr", password="12345678")
