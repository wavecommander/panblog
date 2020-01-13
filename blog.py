from pathlib import Path
import os
import shutil

# SITE
md_dir = './md/'
out_dir = './site/'
res_out_dir = out_dir + 'res/'

# RES
res_dir = './res/'
pandoc_head = 'pandoc -s -t html5 -o '
css_filename = 'github.css'
css_file = res_dir + css_filename
css_out_file = res_out_dir + css_filename
head_file = res_dir + 'head.html'
head_md_file = res_dir + 'head.md'
comments_html = res_dir + 'foot.html'

# BASE
pandoc_base = 'pandoc -s -t html5 -c %s -H %s -o ' % (css_file, head_file)
base_md_dir = md_dir + 'base/'
base_homepage_file = md_dir + 'base_index.md'
homepage_file = base_md_dir + 'index.md'
home_msg_begin = 'My latest blog post is: '

# BLOG INDEX
blog_index_file = md_dir + 'blog_index.md'
blog_index_start = '% Blog Index'

# POSTS
pandoc_post = 'pandoc -s -t html5 -c %s -H %s -A %s -o ' % (css_file, head_file, comments_html)
post_md_dir = md_dir + 'posts/'

def clean_build():
    quick_build()
    build_blog_index()

def quick_build():
    delete_out_dir()
    build_res()
    build_base()
    build_posts()

def delete_out_dir():
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

def build_res():
    build_head()
    copy_css()

def build_head():
    comd = '%s %s %s' % (pandoc_head, head_file, head_md_file)
    print('Building Header ...')
    os.system(comd)

def copy_css():
    Path(res_out_dir).mkdir(parents=True, exist_ok=True)
    print('Copying CSS ...')
    shutil.copyfile(src=res_dir + css_filename, dst=css_out_file)

def build_base():
    if len(post_list) > 0:
        append_message_to_home()

    print('Building Base Files ...')
    base_files = os.listdir(base_md_dir)
    for base_file in base_files:
        comd = '%s %s %s' % (pandoc_base, out_dir +
                             base_file[:-2] + 'html', base_md_dir + base_file)
        os.system(comd)

def append_message_to_home():
    print('Appending Home Page Message ...')
    post = post_list[0]

    with open(base_homepage_file, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('#####', home_msg_begin +
                                ('[%s](%s)' % (post[1], post[0])))

    with open(homepage_file, 'w+') as file:
        file.write(filedata)
def build_blog_index():
    with open(blog_index_file, 'w+') as blog_index:
        blog_index.write(blog_index_start + '\n\n')
        posts = os.listdir(post_md_dir)
        for post in posts:
            with open(post_md_dir + post, 'r') as post_file:
                title = post_file.readline()[2:-1]
                date = post_file.readline()[:-1]
                blog_index.write('* [%s](%s) - %s \n' % (title, post[:-2] + 'html', date))
    comd = '%s %s %s' % (pandoc_base, out_dir + 'blog_index.html', blog_index_file)
    os.system(comd)

def build_posts():
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    posts = os.listdir(post_md_dir)
    for post in posts:
        comd = '%s %s %s' % (pandoc_post, out_dir + post[:-2] + 'html', post_md_dir + post)
        os.system(comd)

if __name__ == '__main__':
    clean_build()
