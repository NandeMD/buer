# buer
A little **b**ack**u**p**er** for my personal projects without extra dependencies. Compresses files to `.lzma` and folders to `.tar.xz.`

## How to Use?
1. Edit config.json
   1. Enter the path of folder to contain your backups \(as a string\): `backup_dest_dir`
   2. Enter all the file/folder paths you want to back up \(as a list of strings\): `files_and_folders`
2. Run the script.
    ```shell
    python3 main.py [interval in seconds]
    ```

### Example:
>#### config.json
>```json
>{
>  "backup_dest_dir": "/home/user/backups",
>  "files_and_folders": [
>    "/home/user/important-folder-1",
>    "/home/user/very-important-file-1",
>    "/home/user/iwannabackup.this"
>  ]
>}
>```

```shell
python3.11 -m venv venv
source venv/bin/activate
python main.py 3600
```