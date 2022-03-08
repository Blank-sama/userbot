import os

from ftpretty import ftpretty

from Bonten import config

host = config.get('seedbox', 'host', fallback=None)
username = config.get('seedbox', 'username', fallback=None)
password = config.get('seedbox', 'password', fallback=None)
ftp = ftpretty(host=host, user=username, password=password)


async def tree(path):
    files = []
    ftp.cd(path)
    for x in ftp.list(ftp.pwd(), extra=True):
        if x['directory'] == 'd':
            inner_files = await tree(x['name'])
            files = files + inner_files
            ftp.cd('..')
        elif x['directory'] == '-':
            file_name = f"{ftp.pwd()}/{x['name']}"
            files.append([x['datetime'], x['size'], file_name])

    return files


async def get_ftp_files():
    file_list = await tree('downloads/manual')

    files_grouped_by_date = {}
    for x in file_list:
        date_group = f"{x[0].day}-{x[0].month}-{x[0].year}"

        if date_group not in files_grouped_by_date:
            files_grouped_by_date[date_group] = [x]
        else:
            files_grouped_by_date[date_group].append(x)

    ftp_dir = 'downloads/ftp'

    if not os.path.exists(ftp_dir):
        os.makedirs(ftp_dir)

    for date in files_grouped_by_date:
        files = files_grouped_by_date[date]

        with open(f'{ftp_dir}/{date}.txt', mode='w+') as filed_from_date:
            for file in files:
                full_path = f"ftp://{username}:{password}@{host}{file[2]}"
                filed_from_date.write(full_path + '\n')
