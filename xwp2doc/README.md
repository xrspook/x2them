# xwp2doc使用说明

## 1 前言

xwp2doc是一个基于python3的转换脚本，用于转换WordPress导出的XML文件为静态网站。静态网站的风格基于GitBook 3.2.3（借用了GitBook的js和css），需要变换风格的请自行脑补。



之所以要写这个脚本，是因为我从前BSP上的老数据太多，那些BSP都挂了（BlogBus还记得？点点网还记得？），最多的那个上面有9000多篇，里面还有3000多个标签，天文数字一样的数据让静态网站转换工具瘫痪，阵亡的包括GitBook（慢得要死，无药可救的节奏），MkDocs（小试可以，数量一多就完了，中文搜索怪怪的），Hugo（速度飞快，但只有少数非常简洁的模板能成功建站）。只好自己动手。



xwp2doc转换9000多篇文章只需不到30秒，生成的文件不超过50MB（但这也看每篇文章的长度到底是多少）。随便找个地方一放爽歪歪，VS Code搭配Live Server插件，单机也能重温得很开心。



> 成功转换案例：<http://yday.xlanda.net/xdoc/adelrio/>。9498篇日志，3280个标签，6个分类，原始XML文件21.9MB，转换后静态网站48.7MB（7z压缩后3.8MB），转换时间小于30秒（与计算机性能有关，我用的是Win7，CPU i5六系，内存8GB）。



## 2 功能及缺陷

注意：本方法适合转换老blog，如果还要写作，还要增加数据、继续与读者交流，请选择其它静态网站转换方案，比如Hugo，Hexo， Jekyll等。



1. 本方法可快速转换WordPress导出的XML文件为GitBook风格的静态网站。（适配WordPress 5.4.2）。
2. XML导出文件里的正文内容原样输出，不支持多媒体转换搬家，因此对纯文字的blog非常有用，对多媒体很多的blog效果可能非常差，试想多媒体失效后……
3. 支持自定义首页（markdown格式编写）。无自定义首页时默认输出原blog的基础数据，包括：标题、描述、原网址。
4. 静态网站的左边目录默认输出WordPress的分类，全部标签的索引放在一个页面里。如果blog里的文章很多，标签很多，请自行想象恐怖程度（举个例子：3000多个标签，7.5万个标题索引放在一个html里，文件大小为7.7MB，打开会非常慢，但能开。应该极少人有这么多文章和这么多标签吧？）。
5. 不支持站内搜索。曾尝试用lunr.js做全站搜索，但blog的内容太多，根本是个无底洞，所以直接放弃。为了弥补不能搜索，所以配齐了分类及标签的文章索引。GitBook和MkDocs都基于lunr.js做全文搜索，大概因为这样，它们根本转换不出我的“大数据”。
6. 自带404页面，能不能实现跟服务器设置有关。若托管在GitHub Pages，据说放在项目的根目录才有效？放在项目的某个文件夹里是没用的，亲测。
7. 不支持代码高亮。估计是我写的代码注释太奇怪，所以无论是highlight.js还是prism.js渲染后都是错乱的，高亮错乱不如不高亮。



## 3 使用方法

1. 安装python3，并配置好环境（请自行脑补）。

2. xwp2doc需要额外安装两个模块：jinja2（模板套用），markdown（md文件转换）。

	```
	pip install jinja2
	```

	```
	pip install markdown
	```

3. 下载xwp2doc文件夹，把WordPress导出的XML文件（如：wordpress.xml）放到文件夹内。

4. 若要自定义首页，请执行本步骤，否则请直接跳过。修改xwp2doc文件夹内“diy_index_sample.md”文件名为“diy_index.md”，编辑markdown文件，设计你的首页。

5. 在xwp2doc文件夹目录运行。若日志很多，请耐心等待。

   ```
   xwp2doc.py wordpress.xml
   ```

6. 若转换成功，xwp2doc文件夹里会生成wordpress_doc文件夹，这就是静态网站了！想放哪里就放哪里！

7. 若转换失败，脚本会提示错误原因，请自行查找wordpress.xml卡壳的地方，非常有可能是导出的文件里有些奇怪的字符，删掉就好，然后重新执行步骤5。



## 4 尾声

这个脚本的出现纯粹因为我念旧，想把过去的好东西重新放出来，脚本写得不对的，欢迎大家批评指正。