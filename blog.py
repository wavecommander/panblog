import os
import shutil
import calendar
import datetime
from pathlib import Path

abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
global_post_list_list = []

# PANDOC DEFAULT FILES
default = "--defaults ./defaults/"
default_base = default + "base.yaml"
default_content = default + "content.yaml"
default_post = default + "post.yaml"

# SITE
md_dir = "./md/"
out_dir = "./site/"
tmp_dir = "./tmp/"
stateful_dirs = [ out_dir, tmp_dir ]

# HEADER AND FOOTER
head_foot_dir = "./head-foot/"
pandoc_head = "pandoc -t html5 -o "

# BASE
pandoc_base = f"pandoc {default_base} {default_content} -o "
base_md_dir = md_dir + "base/"
base_homepage_file = md_dir + "base-index.md"
homepage_file = tmp_dir + "index.md"

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
js_file = "./days-ago.js"
js_out_dir = f"{out_dir}js/"
js_out_file = js_out_dir + js_file[2:]

# POSTS
pandoc_post = f"pandoc {default_base} {default_content} {default_post} -o "
post_md_dir = md_dir + "posts/"


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
    build_base()
    build_dynamic()
    copy_verbatim()




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
            post_dict[key] = sorted(
                post_dict[key], key=lambda x: x["date"], reverse=True
            )

        for key in post_type_order:
            output_str += (
                f"### {post_type_dict[key]['name']} - {post_type_dict[key]['desc']}\n\n"
            )

            for post in post_dict[key]:
                date = f"{str(post['date'].day)} {calendar.month_name[post['date'].month][:3]} {str(post['date'].year)}"
                output_str += f"{date} - [{post['title']}]({post['path']}) \n\n"
            output_str += "\n"

            post_list_list.append(post_dict[key])

        index.write(output_str)

    cmd = f"{pandoc_base} {out_dir}{index_md_name[:-2]}html {index_md_file}"
    os.system(cmd)

    for i, post_list in enumerate(global_post_list_list):
        find_replace_latest_post_msg(post_list[0], f"#{i}#", post_type_order[i])

    with open(homepage_file, "a+") as file:
        file.write(f'\n\n<script type="text/javascript" src="js/{js_file}"></script>\n')


def find_replace_latest_post_msg(latest_post, to_replace, post_type):
    print(f"Finding+Replacing Latest {post_type} Post Message ...")
    source_file = base_homepage_file
    if os.path.isfile(homepage_file):
        source_file = homepage_file

    with open(source_file, "r") as file:
        filedata = file.read()

    filedata = filedata.replace(
        to_replace,
        f"[{latest_post['title']}]({latest_post['path']}) - {latest_post['date']}",
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


def copy_verbatim():
    print("Copying verbatim dir ...")
    shutil.copytree(src='./verbatim', dst=out_dir, dirs_exist_ok=True)


if __name__ == "__main__":
    clean_build()
