## 用法

下载autofill_release.zip

用于把excel里处理好的数据自动填写到虚拟实验数据表中。

- 先在当前路径下创建xxx.txt，把数据从excel直接粘贴到xxx.txt中，保存

  （请确保粘贴的数据形状和要填的表格一样）

- 再运行autofill.exe，显示“filename?”，输入xxx.txt，回车运行

- 运行后显示“按任意键开始...”，点进实验数据表格的第一格，然后按下键盘任意键就会开始填写

（xxx换成任意名称均可）
（autofill.exe是autofill.py用pyinstaller打包得到的，功能是一样的，如果电脑上有python也可以用python版本）
