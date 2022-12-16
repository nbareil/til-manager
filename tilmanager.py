#! /usr/bin/env python3

import os
import datetime
import subprocess

import click
import jinja2

from slugify import slugify_url

default_tmpl = """---
categories:
 - til
date: {{ created_at|isoformat }}
title: {{ title }}
description: XXX
---


TIL

"""

DEFAULT_HUGO_DIR = os.path.join(
    os.environ["HOME"], "projects", "justanothergeek.chdir.org"
)
EDITOR = os.environ.get("EDITOR", "nvim")


def isoformat(value):
    return value.isoformat()


@click.group()
@click.option(
    "--dir",
    default=DEFAULT_HUGO_DIR,
    type=click.Path(exists=True, dir_okay=True, writable=True),
)
def cli(dir):
    click.echo(f"Going into {dir}")
    os.chdir(dir)


@click.command()
@click.option("--title", prompt=True)
@click.option("--slug")
def new(title, slug=None):
    # Build valid slug
    if not slug:
        slug = slugify_url(title)
        click.echo(f"slug = {slug}")
        click.confirm("Is it good enough?", abort=True)

    # Fill in template
    created_at = datetime.datetime.now()
    jinja_env = jinja2.Environment()
    jinja_env.filters["isoformat"] = isoformat
    tmpl = jinja_env.from_string(default_tmpl)
    path = os.path.join("content", "post", slug + ".md")
    with open(path, "wt+") as f:
        f.write(tmpl.render(locals()))

    # git dance
    subprocess.run(["git", "add", path])

    # Launch editor
    subprocess.call([EDITOR, path])

    # YOLO or not?
    if click.confirm("Post ready to be published?"):
        subprocess.run(["git", "add", path])
        subprocess.call(["git", "commit", "-m" f"Adding {slug}" ])
        subprocess.call(["git", "push"])

cli.add_command(new)

if __name__ == "__main__":
    cli()
