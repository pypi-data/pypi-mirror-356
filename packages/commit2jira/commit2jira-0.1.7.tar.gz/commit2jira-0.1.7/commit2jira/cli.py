import os
import click
from commit2jira.install import install_hooks

@click.group()
def cli():
    """Commit2Jira CLI"""
    pass

@cli.command()
def install():
    """Install Git hook into current repo"""
    repo_path = os.getcwd()
    install_hooks(repo_path)

def main():
    cli()

if __name__ == "__main__":
    main()
