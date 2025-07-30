import click
import os
import shutil
import stat

def copy_template(src, dst, project_name):
    """Copies the template directory to a new project directory."""
    if os.path.exists(dst):
        if click.confirm(f"Directory '{project_name}' already exists. Overwrite?"):
            shutil.rmtree(dst)
        else:
            click.echo("Aborting.")
            return

    # A list of files/dirs to ignore
    ignore_list = ["__pycache__"]

    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*ignore_list))

    # Rename gitignore.txt back to .gitignore
    gitignore_path = os.path.join(dst, "gitignore.txt")
    if os.path.exists(gitignore_path):
        os.rename(gitignore_path, os.path.join(dst, ".gitignore"))


@click.group()
def cli():
    """A CLI tool to create a new Selenium POM project."""
    pass


@cli.command()
@click.argument("project_name")
def new(project_name):
    """Creates a new Selenium POM project."""
    template_dir = os.path.join(os.path.dirname(__file__), "template")
    project_dir = os.path.join(os.getcwd(), project_name)

    copy_template(template_dir, project_dir, project_name)

    click.echo(f"Successfully created project '{project_name}'")
    click.echo("To get started:")
    click.echo(f"  cd {project_name}")
    click.echo("  pip install -r requirements.txt")
    click.echo("  python main.py")

if __name__ == '__main__':
    cli() 