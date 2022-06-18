# 同步文件夹  
支持多仓库&多文件夹配置，采用集合类消重+定时器进行降频&集中，定时处理所有待更新的仓库。  
此外，为了保证运行状态，采用file_sync.py本身实时输出刷新时间 + autorun.py进行再次封装外部检测保证长时间稳定性(可选用)

## 目录设置 file_list.txt 一个文件夹一行
```
C:\Users\W\Desktop\folder\gitfolder
C:\Users\W\Desktop\folder\gitfolder\folder1
```

## 使用方法
```
cd file_sync
python3 file_sync.py
# 自动监控运维版-使用autorun.py代替file_sync.py
python3 autorun.py
# win
# 可封装成.bat: pythonw  __YOUR_DIR__\file_sync.py
# 或使用pyinstaller打包为exe再创建快捷方式 pyinstaller -F -w file_sync.py
# linux： 封装为sh等 
```

## 状态判断
运行后会自动在根目录创建run.txt并显示最近阻塞进程刷新时间-5s一刷新(run.txt已添加至.gitignore不会频繁更库, 但建议同步文件夹设置为二级目录，否则run.txt依然会触发事件)

## Refer
https://github.com/iWoz/file_sync 特定文件同步，在此基础上改进 