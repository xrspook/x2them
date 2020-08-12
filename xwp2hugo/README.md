# xwp2hugo使用说明

## 1 这是什么

WordPress to Hugo，WordPress XML转基于Hugo格式要求的md文件，只生成md文件哦！

## 2 如何使用

1. 安装python3，并配置好环境（请自行脑补）。

2. xwp2hugo需要额外安装html2text模块（html转md）。

3. 下载xwp2hugo.py，把WordPress导出的XML文件（如：wordpress.xml）放在同一文件夹内。

4. 在xwp2hugo.py所在文件夹运行。若日志很多，请耐心等待。

	```
	xwp2hugo.py wordpress.xml
	```

5. 若转换成功，xwp2hugo.py所在文件夹里会生成wordpress_hugo文件夹，这就是你要的了！

6. 若转换失败，脚本会提示错误原因，请自行查找wordpress.xml卡壳的地方，非常有可能是导出的文件里有些奇怪的字符，删掉就好，然后重新执行步骤4。