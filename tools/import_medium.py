#!python

import os.path
from datetime import datetime

import markdownify
import click


def post_headers(name: str, date: str):
    return f"""---
Title: "{name.replace("_", " ").replace("-", " ")}"
Slug: {name}
Date: {date}
Author: Antoine Veuiller
Category: Software Engineering
Tags: TODO
Summary: "TODO"
---
"""


@click.group()
def cli():
    pass


@cli.command()
@click.argument('html_path', type=click.Path(exists=True))
@click.argument('slug', type=str)
def import_medium(html_path: str, slug: str):
    with open(html_path, 'r') as html_file:
        md_content = markdownify.markdownify(html_file.read())

    date = datetime.now().strftime("%Y-%m-%d")
    md_content = f"{post_headers(slug, date)}\n{md_content}"

    post_name = os.path.join("content", "posts", f"{date}_{slug}.md")
    with open(post_name, "w+") as out_f:
        out_f.write(md_content)


if __name__ == '__main__':
    cli()
