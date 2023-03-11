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
post_index_file = tmp_dir + post_index_md_name
post_index_start = "% Post Index"
post_type_order = ["T1", "T2", "SD", "MP", "T3"]
post_type_dict = {
    "T1": {"name": "Tier 1", "desc": "Important"},
    "T2": {"name": "Tier 2", "desc": "Might interest you"},
    "SD": {
        "name": "Something Different",
        "desc": "[Something completely different](https://youtube.com/clip/UgkxsPjk_YNNT-8-RXnFu5vOdOeih8pW5QY_)",
    },
    "MP": {"name": "Meta Post", "desc": "Posts about me and this site"},
    "T3": {"name": "Tier 3", "desc": "Why did I spend time writing this?"},
}

# POSTS
pandoc_post = f"pandoc {default_base} {default_content} {default_post} -o "
posts_md_dir = md_dir + "posts/"

# JS
js_dict = { homepage_file: [ "days-ago.js" ] }

def clean_build():
    print("Clean Building ...")
    mk_clean_dirs(stateful_dirs)
    build_head()
    build_posts()
    build_blog_index(
        global_post_list_list,
        posts_md_dir,
        post_index_md_name,
        post_index_file,
        post_index_start,
    )
    generate_homepage()
    build_base()
    build_dynamic()
    copy_verbatim()


def exec_pandoc(cmd, md_file):
    # append js script tag(s) if page is supposed to have them
    if md_file in js_dict.keys():
        with open(md_file, "a+") as file:
            for js_file in js_dict[md_file]:
                file.write(f'\n\n<script type="text/javascript" src="js/{js_file}"></script>\n')
    os.system(f"{cmd} {md_file}")


def build_blog_index(
    post_list_list, post_md_dir, index_md_name, index_md_file, index_start
):
    print("Building Post Index ...")

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

    exec_pandoc(f"{pandoc_base} {out_dir}{index_md_name[:-2]}html", index_md_file)


def generate_homepage():
    # Homepage is dynamic so it doesn't get built as HTML until build_dynamic()
    print(f"Generating Homepage ...")
    filedata = ''
    with open(base_homepage_file, "r") as file:
        filedata = file.read()
        for i, post_list in enumerate(global_post_list_list):
            print(f"\tFinding+Replacing Latest {post_type_order[i]} Post Message ...")
            filedata = filedata.replace(
                f"#{i}#",
                f"[{post_list[0]['title']}]({post_list[0]['path']}) - {post_list[0]['date']}",
            )

    with open(homepage_file, "w+") as file:
        file.write(filedata)


def mk_clean_dirs(dirs):
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        Path(dir).mkdir(parents=True, exist_ok=False)


def build_head():
    print("Building Header ...")
    exec_pandoc(f"{pandoc_head} {head_foot_dir}head.html", head_foot_dir + "head.md")


def build_md_dir_html(file_type, md_dir, pandoc_default):
    print(f"Building {file_type} ...")
    md_files = os.listdir(md_dir)
    for md_file in md_files:
        exec_pandoc(f"{pandoc_default} {out_dir + md_file[:-2]}html", md_dir + md_file)


def build_base():
    build_md_dir_html("Base Files", base_md_dir, pandoc_base)


def build_dynamic():
    build_md_dir_html("Dynamically Generated Files", tmp_dir, pandoc_base)


def build_posts():
    build_md_dir_html("Posts", posts_md_dir, pandoc_post)


def copy_verbatim():
    print("Copying verbatim dir ...")
    shutil.copytree(src='./verbatim', dst=out_dir, dirs_exist_ok=True)


if __name__ == "__main__":
    clean_build()
