from pathlib import Path
import os
import sys
import shutil
import calendar
import datetime
import fileinput

abbr_to_num = {name: num for num,
               name in enumerate(calendar.month_abbr) if num}
blog_post_list = []
rabbit_holes_post_list = []

# PANDOC DEFAULT FILES
def_base = '--defaults ./base.yaml'
def_content = '--defaults ./content.yaml'
def_post = '--defaults ./post.yaml'

# SITE
md_dir = './md/'
out_dir = './site/'
res_out_dir = f'{out_dir}res/'
image_dir = './images/'
image_out_dir = out_dir + image_dir[2:]
netlify_file = './netlify.toml'
netlify_out_file = out_dir + netlify_file[2:]

# RES
res_dir = './res/'
pandoc_head = f'pandoc {def_base} -o '
css_filename = 'min.css'
css_file = res_dir + css_filename
css_out_file = res_out_dir + css_filename
head_file = f'{res_dir}head.html'
head_md_file = f'{res_dir}head.md'
comments_html = f'{res_dir}foot.html'

# BASE
pandoc_base = f'pandoc {def_base} {def_content} -o '
base_md_dir = f'{md_dir}base/'
base_homepage_file = f'{md_dir}base-index.md'
homepage_file = f'{base_md_dir}index.md'
blog_msg = 'My latest blog post is: '
rabbit_msg = 'My latest rabbit hole post is: '

# BLOG INDEX
blog_index_md_name = 'blog-index.md'
blog_index_file = f'{md_dir}blog-index.md'
blog_index_start = '% Blog Index\n\nPosts that have a clear narrative/argument'

# RABBIT HOLE INDEX
rabbit_holes_index_md_name = 'rabbit-holes.md'
rabbit_holes_index_file = f'{md_dir}rabbit-holes.md'
rabbit_holes_index_start = '% Rabbit Holes\n\nPosts that are more a stream of consciousness'

# POSTS
pandoc_post = f'pandoc {def_base} {def_content} {def_post} -o '
blog_post_md_dir = f'{md_dir}blog-posts/'
rabbit_holes_md_dir = f'{md_dir}rabbit-holes/'


def clean_build():
    print('Clean Building ...')
    delete_out_dir()
    delete_temps()
    build_head()
    copy_css()
    build_posts(blog_post_md_dir)
    build_posts(rabbit_holes_md_dir)
    build_blog_index(blog_post_list, blog_post_md_dir, blog_index_md_name,
                     blog_index_file, blog_index_start)
    build_blog_index(rabbit_holes_post_list, rabbit_holes_md_dir, rabbit_holes_index_md_name,
                     rabbit_holes_index_file, rabbit_holes_index_start)
    append_message_to_home(blog_post_list, '#BLOG#', blog_msg)
    append_message_to_home(rabbit_holes_post_list, '#RABBIT#', rabbit_msg)
    build_base()
    copy_images()
    copy_netlify()


def delete_out_dir():
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)


def delete_temps():
    if os.path.exists(homepage_file):
        os.remove(homepage_file)
    if os.path.exists(blog_index_file):
        os.remove(blog_index_file)
    if os.path.exists(rabbit_holes_index_file):
        os.remove(rabbit_holes_index_file)


def build_head():
    print('Building Header ...')
    cmd = f'{pandoc_head} {head_file} {head_md_file}'
    os.system(cmd)


def copy_css():
    print('Copying CSS ...')
    Path(res_out_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=res_dir + css_filename, dst=css_out_file)


def build_base():
    print('Building Base Files ...')
    base_files = os.listdir(base_md_dir)
    for base_file in base_files:
        cmd = f'{pandoc_base} {out_dir + base_file[:-2]}html {base_md_dir + base_file}'
        os.system(cmd)


def build_posts(posts_md_dir):
    print('Building Blog Posts ...')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    posts = os.listdir(posts_md_dir)
    for post in posts:
        cmd = f'{pandoc_post} {out_dir + post[:-2]}html {posts_md_dir + post}'
        os.system(cmd)


def build_blog_index(post_list, post_md_dir, index_md_name, index_md_file, index_start):
    print('Building Blog Index ...')
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    with open(index_md_file, 'w+', encoding="utf8") as index:
        index.write(index_start + '\n\n')
        posts = os.listdir(post_md_dir)
        for post in posts:
            with open(post_md_dir + post, 'r', encoding="utf8") as post_file:
                title = post_file.readline()[2:-1]
                date = post_file.readline()[:-1].split()
                date = datetime.date(
                    int(date[2]), abbr_to_num[date[1]], int(date[0]))
                post_list.append((f'{post[:-2]}html', title, date))

        post_list = sorted(post_list, key=lambda x: x[2], reverse=True)

        for post in post_list:
            date = post[2]
            date = f'{str(date.day)} {calendar.month_name[date.month][:3]} {str(date.year)}'
            index.write(f'{date} - [{post[1]}]({post[0]}) \n\n')

    cmd = f'{pandoc_base} {out_dir}{index_md_name[:-2]}html {index_md_file}'
    os.system(cmd)


def append_message_to_home(post_list, to_replace, msg):
    print('Appending Homepage Message ...')
    post_list = sorted(post_list, key=lambda x: x[2], reverse=True)
    latest_post = post_list[0]
    source_file = base_homepage_file
    if os.path.isfile(homepage_file):
        source_file = homepage_file
    with open(source_file, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(to_replace, f'{msg}[{latest_post[1]}]({latest_post[0]})')
    with open(homepage_file, 'w+') as file:
        file.write(filedata)


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
    clean_build()
