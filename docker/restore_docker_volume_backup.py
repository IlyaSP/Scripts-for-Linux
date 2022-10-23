import os
import re
import sys
import subprocess
import tarfile


def get_list_backup_volume(dir):
    """Получения списка volume из архивных файлов"""
    backup_volume = []
    dict_list_arhive = {}
    # print(os.listdir(dir))
    for i in os.listdir(dir):
        if re.search(r'tar', i) is not None:
            dict_list_arhive[i.split('.')[0]] = i
            backup_volume.append(i.split('.')[0])

    return dict_list_arhive, backup_volume


def get_list_exist_volume():
    exist_volume = []
    stream = os.popen('docker volume ls --format "{{.Name}}"')
    vol = stream.readlines()
    if len(vol) != 0:
        for i in vol:
            exist_volume.append(i.replace('\n','').strip())
    return exist_volume


def check_intersection_volume(list_backup_volume, list_exist_volume):
    if len(set(list_backup_volume).intersection(set(list_exist_volume))) != 0:
        status = 1
    else:
        status = 0
    return status


def create_volume(list_backup_volume):
    for vol in list_backup_volume:
        command = subprocess.run(['docker', 'volume', 'create' , vol], stdout=subprocess.PIPE,  encoding='utf-8')
        if command.returncode != 0:
            print("Error create {0} volume".format(vol))
            sys.exit(command.stderr)
        else:
            continue

def get_list_all_exist_volume():
    stream = os.popen('docker volume ls --format "{{.Name}}: {{.Mountpoint}}"')
    dict_volume_list = {}
    for i in stream.readlines():
        new_element = i.replace('\n', '').split(':')
        dict_volume_list[new_element[0].strip()] = new_element[1].strip()

    return dict_volume_list


def extract_backup_to_vol(list_backup_volume, dict_volume_list, dict_list_arhive, dir):
    for vol in list_backup_volume:
        dir_mount = dict_volume_list.get(vol)
        # print(dir_mount)
        if dir_mount is None:
            sys.exit("No volume")
        else:
            print('Extcract volume {0}'.format(vol))
            tar_file = '{0}/{1}'.format(dir, dict_list_arhive.get(vol))
            with tarfile.open(tar_file, 'r') as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tar, path=dir_mount)


if __name__ == '__main__':

    dict_list_arhive, list_backup_volume = get_list_backup_volume(dir='.')
    print(list_backup_volume)

    list_exist_volume = get_list_exist_volume()
    print(list_exist_volume)

    status = check_intersection_volume(list_backup_volume, list_exist_volume)
    if status != 0:
        sys.exit('there is an intersection of backup and exist volume')
    else:
        create_volume(list_backup_volume)

    dict_volume_list = get_list_all_exist_volume()
    print(dict_volume_list)

    extract_backup_to_vol(list_backup_volume, dict_volume_list, dict_list_arhive, dir='.')
