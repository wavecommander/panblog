import os
import shutil
import calendar
import datetime
from pathlib import Path

abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
global_post_list_list = []

# PANDOC DEFAULT FILES
def_base = "--defaults ./base.yaml"
def_content = "--defaults ./content.yaml"
def_post = "--defaults ./post.yaml"

# SITE
md_dir = "./md/"
out_dir = "./site/"
res_out_dir = f"{out_dir}res/"
image_dir = "./images/"
image_out_dir = out_dir + image_dir[2:]
netlify_file = "./netlify.toml"
netlify_out_file = out_dir + netlify_file[2:]

# RES
res_dir = "./res/"
pandoc_head = f"pandoc -t html5 -o "
css_filename = "min.css"
css_file = res_dir + css_filename
css_out_file = res_out_dir + css_filename
head_file = f"{res_dir}head.html"
head_md_file = f"{res_dir}head.md"
comments_html = f"{res_dir}foot.html"

# BASE
pandoc_base = f"pandoc {def_base} {def_content} -o "
base_md_dir = f"{md_dir}base/"
base_homepage_file = f"{md_dir}base-index.md"
homepage_file = f"{base_md_dir}index.md"

# POST INDEX
post_index_md_name = "post-index.md"
post_index_file = f"{md_dir}post-index.md"
post_index_start = "% Post Index"
post_type_order = ["T1", "T2", "RH", "MP", "T3"]
post_type_dict = {
    "T1": {"name": "Tier 1", "desc": "Important"},
    "T2": {"name": "Tier 2", "desc": "Might interest you"},
    "RH": {
        "name": "Rabbit Hole",
        "desc": "Posts that are more "
        + "[a stream of consciousness](https://www.youtube.com/watch?v=GFQbLwaElt4&t=293s)",
    },
    "MP": {"name": "Meta Post", "desc": "Posts about me and this site"},
    "T3": {"name": "Tier 3", "desc": "Why did I spend time writing this?"},
}

# POSTS
pandoc_post = f"pandoc {def_base} {def_content} {def_post} -o "
post_md_dir = f"{md_dir}posts/"


def build_blog_index(
    post_list_list, post_md_dir, index_md_name, index_md_file, index_start
):
    print("Building Post Index ...")
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    post_dict = {key: [] for key in post_type_order}

    output_str = ""

    with open(index_md_file, "w+", encoding="utf8") as index:
        output_str += index_start + "\n\n"
        posts = os.listdir(post_md_dir)

        for post in posts:
            with open(post_md_dir + post, "r", encoding="utf8") as post_file:
                title = post_file.readline()[2:-1]

                date = post_file.readline()[:-1].split()
                date = datetime.date(int(date[2]), abbr_to_num[date[1]], int(date[0]))

                post_type = post_file.readline().split()[0]

                post_dict[post_type].append(
                    {
                        "path": f"{post[:-2]}html",
                        "title": title,
                        "date": date,
                        "type": post_type,
                    }
                )

        for key in post_dict.keys():
            post_dict[key] = sorted(post_dict[key], key=lambda x: x["date"], reverse=True)

        for key in post_type_order:
            output_str += f"### {post_type_dict[key]['name']} - {post_type_dict[key]['desc']}\n\n"

            for post in post_dict[key]:
                date = f"{str(post['date'].day)} {calendar.month_name[post['date'].month][:3]} {str(post['date'].year)}"
                output_str += f"{date} - [{post['title']}]({post['path']}) \n\n"
            output_str += "\n"

            post_list_list.append(post_dict[key])

        index.write(output_str)

    cmd = f"{pandoc_base} {out_dir}{index_md_name[:-2]}html {index_md_file}"
    os.system(cmd)


def find_replace_latest_post_msg(post_list, to_replace, post_type):
    print(f"Finding+Replacing Latest {post_type} Post Message ...")
    source_file = base_homepage_file
    if os.path.isfile(homepage_file):
        source_file = homepage_file

    with open(source_file, "r") as file:
        filedata = file.read()

    days_ago = (datetime.date.today() - post_list[0]['date']).days
    days_str = ''

    if days_ago == 0:
        days_str = "today"
    elif days_ago == 1:
        days_str = "yesterday"
    else:
        days_str = f"{days_ago} days ago"

    filedata = filedata.replace(
        to_replace,
        f"[{post_list[0]['title']}]({post_list[0]['path']}) - {days_str}",
    )

    with open(homepage_file, "w+") as file:
        file.write(filedata)


def delete_out_dir():
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)


def delete_temps():
    if os.path.exists(homepage_file):
        os.remove(homepage_file)
    if os.path.exists(post_index_file):
        os.remove(post_index_file)


def build_head():
    print("Building Header ...")
    cmd = f"{pandoc_head} {head_file} {head_md_file}"
    os.system(cmd)


def copy_css():
    print("Copying CSS ...")
    Path(res_out_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=res_dir + css_filename, dst=css_out_file)


def build_base():
    print("Building Base Files ...")
    base_files = os.listdir(base_md_dir)
    for base_file in base_files:
        cmd = f"{pandoc_base} {out_dir + base_file[:-2]}html {base_md_dir + base_file}"
        os.system(cmd)


def build_posts(posts_md_dir):
    print("Building Posts ...")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    posts = os.listdir(posts_md_dir)
    for post in posts:
        cmd = f"{pandoc_post} {out_dir + post[:-2]}html {posts_md_dir + post}"
        os.system(cmd)


def copy_images():
    print("Copying Images ...")
    Path(image_out_dir).mkdir(parents=True, exist_ok=True)
    images = os.listdir(image_dir)
    for image in images:
        shutil.copyfile(src=image_dir + image, dst=image_out_dir + image)


def copy_netlify():
    print("Copying Netlify TOML ...")
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src=netlify_file, dst=netlify_out_file)


def clean_build():
    print("Clean Building ...")
    delete_out_dir()
    delete_temps()
    build_head()
    copy_css()
    build_posts(post_md_dir)
    build_blog_index(
        global_post_list_list,
        post_md_dir,
        post_index_md_name,
        post_index_file,
        post_index_start,
    )

    for i, post_list in enumerate(global_post_list_list):
        find_replace_latest_post_msg(post_list, f"#{i}#", post_type_order[i])

    build_base()
    copy_images()
    copy_netlify()


if __name__ == "__main__":
    clean_build()
