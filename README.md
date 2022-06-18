# 同步文件夹  

## 目录设置 file_list.txt 一个文件夹一行
```
C:\Users\W\Desktop\folder\gitfolder
C:\Users\W\Desktop\folder\gitfolder\folder1
```

## 使用方法
```
cd file_sync
python3 file_sync.py
# win
# 可封装成.bat: pythonw  __YOUR_DIR__\file_sync.py
# 或使用pyinstaller打包为exe再创建快捷方式 pyinstaller -F -w file_sync.py
# linux： 封装为sh等 
```

## 状态判断
查看run.txt(已添加至.gitignore)


## Refer
https://github.com/iWoz/file_sync 特定文件同步