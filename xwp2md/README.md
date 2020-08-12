# xwp2md使用说明

## 1 这是什么

WordPress to markdown，WordPress XML转普通md文件，自动生成README.md和SUMMARY.md，可直接用于GitBook。

## 2 如何使用

1. 安装python3，并配置好环境（请自行脑补）。

2. xwp2md需要额外安装html2text模块（html转md）。

3. 下载xwp2md.py，把WordPress导出的XML文件（如：wordpress.xml）放在同一文件夹内。

4. 在xwp2md.py所在文件夹运行。若日志很多，请耐心等待。

	```
	xwp2md.py wordpress.xml
	```

5. 若转换成功，xwp2md.py所在文件夹里会生成wordpress_md文件夹，这就是你要的了！

6. 若转换失败，脚本会提示错误原因，请自行查找wordpress.xml卡壳的地方，非常有可能是导出的文件里有些奇怪的字符，删掉就好，然后重新执行步骤4。