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

# POSTS
pandoc_post = 'pandoc -s -t html5 -c %s -H %s -A %s -o ' % (css_file, head_file, comments_html)
post_md_dir = md_dir + 'posts/'

def clean_build():
    build_res()
    build_base()
    build_posts()

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
    base_files = os.listdir(base_md_dir)
    print('Building Base Files ...')
    for base_file in base_files:
        comd = '%s %s %s' % (pandoc_base, out_dir + base_file[:-2] + 'html', base_md_dir + base_file)
        os.system(comd)
    #build_blog_index()

def build_posts():
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    posts = os.listdir(post_md_dir)
    for post in posts:
        comd = '%s %s %s' % (pandoc_post, out_dir + post[:-2] + 'html', post_md_dir + post)
        os.system(comd)

clean_build()
