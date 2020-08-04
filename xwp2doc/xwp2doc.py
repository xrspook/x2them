import re, sys, time, markdown, os, shutil
from xml.dom import minidom
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict

# 全局函数
filename = ''
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('gitbook_temp.html') # 引入模板

def convert(inputfilename):
    try:
        xmldoc = minidom.parse(inputfilename)
        wp = xmldoc.documentElement
    except Exception as e:
        print ('Fail.')
        print (e)
        print ('Please repair or delete invalid token like "& < >" there.')
        sys.exit(1)
    
    global filename
    global template
    filename = inputfilename.replace('.xml', '')
    
    # 读取XML基础数据
    blog_title = getTagData(wp, 'title')
    blog_desc = getTagData(wp, 'description')
    blog_url = getTagData(wp, 'link')
    posts = wp.getElementsByTagName('item')
    
    # 获取导航及归档数据
    log_list = {}
    log_count = 1
    cat_dict = defaultdict(list)
    all_tag_dict = {}
    single_tag_dict = defaultdict(list)
    for log in posts:
        # 获取标题，网址，发布时间数据
        title = replace_text(getTagData(log, 'title'))
        doc_name = convertDocName(getTagData(log, 'wp:post_date'),title)
        day = convertDay(getTagData(log, 'wp:post_date'))        
        archive_li = '<li>' + day + '<a href="' + doc_name + '">' + title + '</a></li>\n'

        # 获取全部日志页数据
        cat_dict['全部日志'].append(archive_li)        
        log_list[log_count] = doc_name
        log_count += 1

        # 获取归档页（分类、标签）数据
        category = log.getElementsByTagName('category')
        for cat_tag in category:
            if cat_tag.getAttribute('domain') == 'category':
                cat = replace_text(getElementData(cat_tag))
                cat_dict[cat].append(archive_li)
            if cat_tag.getAttribute('domain') == 'post_tag':
                tag = replace_text(getElementData(cat_tag))
                all_tag_dict[tag] = all_tag_dict.get(tag, 0) + 1
                single_tag_dict[tag].append(archive_li)

    all_tags = ''
    all_tag_list = list(zip(all_tag_dict.values(), all_tag_dict.keys()))
    all_tag_list.sort(reverse=True)
    for num, name in all_tag_list:
        all_tags += '<a href = "#' + name + '">' + name + '(' + str(num) + ')</a>' + '  '

    # 生成目录
    summary = '<li><a href="全部标签.html">全部标签</a></li>\n'
    for key in cat_dict:
        summary += '<li><a href="' + key + '.html">' + key + '</a></li>\n'

    # 获取文章页数据
    for log in posts:
        status = getTagData(log, 'wp:status')
        title = replace_text(getTagData(log, 'title'))
        author  = getTagData(log, 'dc:creator')
        date = convertDate(getTagData(log, 'wp:post_date'))
        content = getTagData(log, 'content:encoded').replace('\n\n', '<br/><br/>')
        doc_name = convertDocName(getTagData(log, 'wp:post_date'),title)
        category_list = []
        tag_list = []
        category = log.getElementsByTagName('category')
        for cat_tag in category:
            if cat_tag.getAttribute('domain') == 'category':
                category_list.append(replace_text(getElementData(cat_tag)))
            if cat_tag.getAttribute('domain') == 'post_tag':
                tag_list.append(replace_text(getElementData(cat_tag)))
        category_list_str = ', '.join(category_list)
        tag_list_str = ', '.join(tag_list)
        comment_list  = []
        comment = log.getElementsByTagName('wp:comment')
        comment_id = 1
        for cmt in comment:
            comment_date = getTagData(cmt, 'wp:comment_date')
            comment_author = getTagData(cmt, 'wp:comment_author')
            comment_author_email = getTagData(cmt, 'wp:comment_author_email')
            if comment_author_email:
                comment_author_email += ', '
            comment_author_url = getTagData(cmt, 'wp:comment_author_url')
            if comment_author_url:
                comment_author_url += ', '
            comment_content = getTagData(cmt, 'wp:comment_content')
            comment_list.append('<p>' + str(comment_id) + '. ' + comment_author + ', ' + comment_author_email + 
            comment_author_url + comment_date + '</p><p>' + comment_content + '</p>')
            comment_id += 1
        comment_list_str = ''.join(comment_list)
        
        # 生成导航栏
        index = list(log_list.keys()) [list(log_list.values()).index(doc_name)] # 以键值查询键
        if index - 1 > 0:
            pre = log_list[index - 1]
        else:
            pre = '.'
        if index + 1 < len(log_list):
            nex = log_list[index + 1]
        else:
            nex = '.'
        left = '<a href="' + pre + '" class="navigation navigation-prev "><i class="fa fa-angle-left"></i></a>\n'
        right = '<a href="' + nex +'" class="navigation navigation-next "><i class="fa fa-angle-right"></i></a>'
        navigation = left + right
        
        # 文章页输出
        if status == 'publish':
            doc = ''
            doc += '<h1>' + title + '</h1>'
            doc += '<p>作者: ' + author + '</p>'
            doc += '<p>日期: ' + date + '</p>'
            doc += '<p>分类: ' + category_list_str + '</p>'
            doc += '<p>标签: ' + tag_list_str + '</p><hr>'
            doc += content
            if len(comment_list_str) > 0:
                doc += '<hr>'
                doc += '<h2>从前的评论</h2>\n'
                doc += comment_list_str            
            data = template.render(blog_title = blog_title, page_title = title + ' - ' + blog_title, 
            summary = summary, navigation = navigation, core = doc)
            output(filename, doc_name, data)

    # 主页输出
    if os.path.exists('diy_index.md'): # 根目录有自定义diy_index.md
        f =open('diy_index.md', 'r', encoding='utf-8')
        index_md = f.read()
        f.close()    
        index = markdown.markdown(index_md)
    else: # 套用XML基础数据
        index = '<h1>' + blog_title + '</h1>\n'
        if blog_desc:
            index += '<h4>' + blog_desc + '</h4>\n'
        if blog_url:
            index += '<h4>原址: <a href="'+ blog_url +'">' + blog_url + '</a></h4>\n'
    navigation = '<a href="' + log_list[1] +'" class="navigation navigation-next "><i class="fa fa-angle-right"></i></a>'
    data = template.render(blog_title = blog_title, page_title = blog_title, summary = summary, 
    navigation = navigation, core = index)
    ouput_name = 'index.html'
    output(filename, ouput_name, data)

    # 404页输出
    f =open('404.md', 'r', encoding='utf-8')
    page404_md = f.read()
    f.close()    
    page404 = markdown.markdown(page404_md)
    data = template.render(blog_title = blog_title, page_title = blog_title, summary = summary, 
    navigation = '', core = page404)
    ouput_name = '404.html'
    output(filename, ouput_name, data)

    # 归档标签页输出
    tag_page = '<h1 id="top">全部标签</h1>'
    tag_page += '<h1>共' + str(all_tags.count('(')) + '个</h3>'
    tag_page += '<p>' + all_tags + '</p><hr>'
    for key in single_tag_dict:
        single_tag_str = ''
        single_tag_str += ''.join(single_tag_dict[key])
        tag_page += ''.join('<h3 id="' + key + '">' + key  + ' (' +str(len(single_tag_dict[key])) + ')</h3>\n' + single_tag_str)
    tag_page += '<div class="float-button"><a href="#top">回到顶部</a></div>'
    data = template.render(blog_title = blog_title, page_title = '全部标签 - ' + blog_title, summary = summary, 
    navigation = '', core = tag_page)
    ouput_name = '全部标签.html'
    output(filename, ouput_name, data)

    # 归档分类页输出
    for key in cat_dict:
        cat_list = ''.join(cat_dict[key])
        archive_page(cat_list, key, blog_title, summary)

    # 复制主题文件
    path = os.getcwd() + '\\'
    file_path = path + 'gitbook'
    dir_path = path + filename + '_doc' + '\\' + 'gitbook'
    copy_theme(file_path, dir_path)

def copy_theme(file_path,dir_path): # 复制文件夹
    if not os.path.exists(file_path):
        print("gitbook theme not exist!")
    if os.path.exists(dir_path):
        exit
    else:
        shutil.copytree(file_path, dir_path)

def output(filename, doc_name, data): # 输出
    folder = filename + '_doc'
    path = os.getcwd() + '\\' + folder + '\\'
    if not os.path.exists(path):
        os.mkdir(folder)
    new_file = path + doc_name
    f = open(new_file, 'w', encoding='utf-8')
    f.write(data)
    f.close()

def archive_page(cat, title, blog_title, summary): # 归档分类页输出
    global filename
    global template
    archive_page = '<h1>' + title + '</h1>'
    archive_page += '<h3>共' + str(cat.count('<li>')) + '篇</h3>'
    archive_page += '<p>' + cat + '</p>'
    data = template.render(blog_title = blog_title, page_title = title + ' - ' + blog_title, summary = summary, 
    navigation = '', core = archive_page)
    ouput_name = title + '.html'
    output(filename, ouput_name, data)

def getTagData(log, name): # 获取节点数据
    tagdata_text = ''
    if len(log.getElementsByTagName(name))>0:
        tagdata = log.getElementsByTagName(name)[0]
        tagdata_text = getElementData(tagdata)
    return tagdata_text

def getElementData(element): # 获取节点数据
    data = ''
    for node in element.childNodes:
        if node.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
            data += node.data
    return data

def convertTimeStamp(date): # 转化时间戳
    timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def convertDate(date): # 发布时间格式化
    timeStamp = convertTimeStamp(date)
    date = time.strftime("%Y-%m-%d %H:%M:%S+08:00", time.localtime(timeStamp))
    return date

def convertDay(date): # 发布日期格式化
    timeStamp = convertTimeStamp(date)
    date = time.strftime("%Y-%m-%d ", time.localtime(timeStamp))
    return date

def convertDocName(date, title): # 发布时间转网址
    timeStamp = convertTimeStamp(date)
    doc_name = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(timeStamp)) + '.html'
    return doc_name

def replace_text(data): # 处理特殊字符
    data = data.replace('/', 'or')
    data = data.replace('[', '〔')
    data = data.replace(']', '〕')
    data = data.replace('"', '')
    data = re.sub(r"([:@/\\])", "", data)
    data = re.sub(r"(?:&.*?;)", "", data)
    return data

def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = sys.argv[1:]
    if (len(args) == 1):
        print ('Converting...')
        sys.stdout.flush()
        start = time.time()
        convert(args[0])
        end = time.time()
        print ('Done. Elapse %g seconds.' % (end - start))
if __name__ == "__main__":
    sys.exit(main())
