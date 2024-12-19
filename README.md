
mRemoteNG Decrypt Tools.


Project Optimization
Based on the original project, the following optimizations are proposed. Original project address:
https://github.com/gquere/mRemoteNG_password_decrypt


Optimizations:
```
Default output results directly to a TXT file.
Optimize the decrypted result display to clearly indicate the file structure and the folder it belongs to.
If a domain exists, display it in front of the username, e.g., domain\user.
If a port exists, display it after the host, e.g., 127.0.0.1:3389.
Display the protocol type, printed after the port, e.g., 127.0.0.1:3389 (rdp).
Fix some bugs.
```




mRemoteNG 解密工具


基于原项目进行简单优化，原项目地址。
https://github.com/gquere/mRemoteNG_password_decrypt


优化点:
```
默认直接输出结果到txt。
优化-解密结果显示文件结构、在哪个文件夹下面可以清楚区分。
优化-若存在域名则显示在用户名前面。如: domain\user
优化-若存在端口则显示在Host后面。如: 127.0.0.1:3389
优化-显示协议类型，打印在端口后面。如: 127.0.0.1:3389 (rdp)
修复一些BUG
```




Usage
-----
```
usage: mremoteng_decrypt.py [-h] [-p PASSWORD] config_file

Decrypt mRemoteNG configuration files

positional arguments:
  config_file                       mRemoteNG XML configuration file

optional arguments:
  -p PASSWORD, --password PASSWORD  Optional decryption password
```


Example:
```
python3 mremoteng_decrypt.py confCons.xml
```







