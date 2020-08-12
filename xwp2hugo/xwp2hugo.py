import re, sys, time, html2text, os
from xml.dom import minidom

filename = ''
def convert(inputfilename):
    global filename
    try:
        xmldoc = minidom.parse(inputfilename)
        wp = xmldoc.documentElement
    except Exception as e:
        print ('Fail.')
        print (e)
        print ('Please repair or delete invalid token like "& < >" there.')
        sys.exit(1)
        
    posts = wp.getElementsByTagName('item')
    for log in posts:
        status = getTagData(log, 'wp:status')
        title = replace_text(getTagData(log, 'title'))
        author  = getTagData(log, 'dc:creator')
        post_type = getTagData(log, 'wp:post_type')
        date = convertDate(getTagData(log, 'wp:post_date'))
        url = convertUrl(getTagData(log, 'wp:post_date'))
        md_name = convertMdName(getTagData(log, 'wp:post_date'))
        content = getTagData(log, 'content:encoded').replace('\n\n', '<br/><br/>')

        category_list = []
        tag_list = []
        category = log.getElementsByTagName('category')
        for cat_tag in category:
            if cat_tag.getAttribute('domain') == 'category':
                category_list.append('"' + replace_text(getElementData(cat_tag)) + '"')
            if cat_tag.getAttribute('domain') == 'post_tag':
                tag_list.append('"' + replace_text(getElementData(cat_tag)) + '"')
        category_list_str = '[' + ','.join(category_list) + ']'
        tag_list_str = '[' + ','.join(tag_list) + ']'

        comment_list = []
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
    
        h = html2text.HTML2Text()
        h.body_width = 0
        if status == 'publish':
            md = ''
            md += '---\n'
            md += 'title: ' + title + '\n'
            md += 'author: ' + author + '\n'
            md += 'type: ' + post_type + '\n'
            md += 'date: ' + date + '\n'
            md += 'url: ' + url + '\n'
            md += 'categories: ' + category_list_str + '\n'
            md += 'tags: ' + tag_list_str + '\n'
            md += '---\n'
            md += h.handle(content) + '\n'
            if len(comment_list_str) > 0:
                md += '***\n'
                md += '## 从前的评论\n'
                md += h.handle(comment_list_str)
            
            folder = filename + '_hugo'
            path = os.getcwd() + '\\' + folder + '\\'
            if not os.path.exists(path):
                os.mkdir(folder)
            new_file = path + md_name
            f = open(new_file, 'w', encoding='utf-8')
            f.write(md)
            f.close()

def getTagData(log, name): # 获取节点数据，适用于已有格式内容
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
    date = time.strftime("%Y-%m-%dT%H:%M:%S+08:00", time.localtime(timeStamp))
    return date

def convertUrl(date): # 发布时间转网址
    timeStamp = convertTimeStamp(date)
    url = '/post/' + str(timeStamp)
    return url

def convertMdName(date): # 发布时间转网址
    timeStamp = convertTimeStamp(date)
    date = time.strftime("%Y-%m-%d_%H%M%S", time.localtime(timeStamp)) + '.md'
    return date

def replace_text(data):
    data = data.replace('/', 'or')
    data = data.replace('[', '〔')
    data = data.replace(']', '〕')
    data = data.replace('"', '')
    data = re.sub(r"([:@/\\])", "", data)
    data = re.sub(r"(?:&.*?;)", "", data)
    return data

def main(argv=None):
    global filename
    if argv is None:
        argv = sys.argv
    args = sys.argv[1:]
    if (len(args) == 1):
        print ('Converting...'),
        sys.stdout.flush()
        start = time.time()
        filename = args[0].replace('.xml', '')
        convert(args[0])
        end = time.time()
        print ('Done. Elapse %g seconds.' % (end - start))
if __name__ == "__main__":
    sys.exit(main())