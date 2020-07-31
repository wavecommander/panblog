from pathlib import Path
import os
import sys
import shutil
import calendar
import datetime
import fileinput

abbr_to_num = {name: num for num,
               name in enumerate(calendar.month_abbr) if num}
post_list = []

# PANDOC DEFAULT FILES
def_base = '--defaults ./base.yaml'
def_content = '--defaults ./content.yaml'
def_post = '--defaults ./post.yaml'

# SITE
md_dir = './md/'
out_dir = './site/'
res_out_dir = out_dir + 'res/'
image_dir = './images/'
image_out_dir = out_dir + image_dir[2:]
netlify_file = './netlify.toml'
netlify_out_file = out_dir + netlify_file[2:]

# RES
res_dir = './res/'
pandoc_head = 'pandoc %s -o ' % (def_base)
css_filename = 'min.css'
css_file = res_dir + css_filename
css_out_file = res_out_dir + css_filename
head_file = res_dir + 'head.html'
head_md_file = res_dir + 'head.md'
comments_html = res_dir + 'foot.html'

# BASE
pandoc_base = 'pandoc %s %s -o ' % (def_base, def_content)
base_md_dir = md_dir + 'base/'
base_homepage_file = md_dir + 'base_index.md'
homepage_file = base_md_dir + 'index.md'
home_msg_begin = 'My latest blog post is: '

# BLOG INDEX
blog_index_file = md_dir + 'blog_index.md'
blog_index_start = '% Blog Index'

# POSTS
pandoc_post = 'pandoc %s %s %s -o ' % (def_base, def_content, def_post)
post_md_dir = md_dir + 'posts/'


def clean_build():
    delete_out_dir()
    quick_build()
    build_blog_index()
    append_message_to_home()
    copy_images()
    copy_netlify()


def quick_build():
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
    print('Building Header ...')
    comd = '%s %s %s' % (pandoc_head, head_file, head_md_file)
    os.system(comd)


def copy_css():
    print('Copying CSS ...')
    Path(res_out_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=res_dir + css_filename, dst=css_out_file)


def build_base():
    print('Building Base Files ...')
    base_files = os.listdir(base_md_dir)
    for base_file in base_files:
        comd = '%s %s %s' % (pandoc_base, out_dir +
                             base_file[:-2] + 'html', base_md_dir + base_file)
        os.system(comd)


def append_message_to_home():
    print('Appending Homepage Message ...')
    latest_post = post_list[0]
    with open(base_homepage_file, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('#####', home_msg_begin +
                                ('[%s](%s)' % (latest_post[1], latest_post[0])))
    with open(homepage_file, 'w+') as file:
        file.write(filedata)


def build_blog_index():
    global post_list
    print('Building Blog Index ...')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    with open(blog_index_file, 'w+', encoding="utf8") as blog_index:
        blog_index.write(blog_index_start + '\n\n')
        posts = os.listdir(post_md_dir)
        for post in posts:
            with open(post_md_dir + post, 'r', encoding="utf8") as post_file:
                title = post_file.readline()[2:-1]
                date = post_file.readline()[:-1].split()
                date = datetime.date(
                    int(date[2]), abbr_to_num[date[1]], int(date[0]))
                post_list.append((post[:-2] + 'html', title, date))

        post_list = sorted(post_list, key=lambda x: x[2], reverse=True)

        for post in post_list:
            date = post[2]
            date = '%s %s %s' % (
                str(date.day), calendar.month_name[date.month][:3], str(date.year))
            blog_index.write('* %s - [%s](%s) \n' % (date, post[1], post[0]))

    comd = '%s %s %s' % (pandoc_base, out_dir +
                         'blog_index.html', blog_index_file)
    os.system(comd)


def build_posts():
    print('Building Blog Posts ...')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    posts = os.listdir(post_md_dir)
    for post in posts:
        comd = '%s %s %s' % (pandoc_post, out_dir +
                             post[:-2] + 'html', post_md_dir + post)
        os.system(comd)


def copy_images():
    print('Copying Images ...')
    Path(image_out_dir).mkdir(parents=True, exist_ok=True)
    images = os.listdir(image_dir)
    for image in images:
        shutil.copyfile(src=image_dir + image, dst=image_out_dir + image)


def copy_netlify():
    print('Copying Netlify TOML ...')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=netlify_file, dst=netlify_out_file)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('Clean Building ...')
        clean_build()
    else:
        print('Quick Building ...')
        quick_build()
