from importlib.metadata import version, PackageNotFoundError
import typer
from typing_extensions import Annotated
from typing import List
import git
from rich.console import Console


PACKAGE_NAME = "gracegit"
VERSION = version(PACKAGE_NAME)

app = typer.Typer(
        no_args_is_help=True,
        help="Grace's Great Git Abstraction"
        )


console = Console()
try:
    repo = git.Repo('.', search_parent_directories=True)
except:
    pass


@app.command("version", short_help="Show the version. Aliases: v")
@app.command("v", short_help="alias for `version`", hidden=True)
def app_version():
    try:
        typer.echo(f"{PACKAGE_NAME} version: {VERSION}")
    except PackageNotFoundError:
        typer.echo("Package not installed, version unknown.")
    raise typer.Exit()


def rs(branch_name) -> str: return f"{branch_name}:{branch_name}"

@app.command("add-commit-push", short_help="Equivalant of running add, commit, and push with normal Git. Aliases: acp")
@app.command("acp", short_help="alias for `add-commit-push`", hidden=True)
def add_commit_push(commit_message: List[str]):
    repo.git.add(all=True)
    console.print("Added Files")
    msg = ' '.join(commit_message)
    repo.index.commit(msg)
    console.print(f"Created commit {msg}")
    branch_name = repo.active_branch.name

    try:
        with console.status("Pushing to Remote"):

            origin = repo.remote(name='origin')
            info_list = origin.push(refspec=rs(branch_name), set_upstream=True)
        console.print(f"Pushed to remote: {origin.url}")
    except:
        # TODO: handle this?????
        console.print("No remote named origin found or failed to push")
        console.print("Please try with the normal git command")
        typer.Exit(code=10)


@app.command("change-branch", short_help="Change into a branch or create a new one if one did not exist before. Aliases: cb, checkout")
@app.command("cb", short_help="alias of `change-branch`", hidden=True)
@app.command("checkout", short_help="alias of `change-branch`", hidden=True)
def change_branch(branch_name: Annotated[str, typer.Argument()] = ""):
    origin = repo.remote(name='origin')
    if branch_name == "":
        default_branch = origin.refs[repo.remote().repo.git.symbolic_ref('refs/remotes/origin/HEAD').split('/')[-1]]
        branch_name = default_branch.name

    branch = None
    remote_branch_name = f"origin/{branch_name}"
    if branch_name in repo.branches:
        branch = repo.branches[branch_name]
    elif remote_branch_name in repo.remote().refs:
        branch = repo.remote().refs[remote_branch_name]

    if branch == None:
        branch = repo.create_head(branch_name)
        branch.checkout()
        console.print(f"Created and checked out new branch {branch_name}")
    else:
        branch.checkout()
        console.print(f"Checked out {branch_name}")
        try:
            with console.status("Pulling Remote"):
                origin.pull(refspec=branch_name.split("/")[~0])
            console.print("Pulled")
        except:
            console.print("Unable to pull remote")

@app.command("clone", hidden=True)
def clone():
    console.print("Uninplimented")
    typer.Exit(5)

@app.command("new-repo", hidden=True)
def new_repo():
    console.print("Uninplimented")
    typer.Exit(5)

@app.command("init-submodules", hidden=True)
def init_submodules():
    console.print("Uninplimented")
    typer.Exit(5)

@app.command("remove-submodule", hidden=True)
def remove_submodule():
    console.print("Uninplimented")
    typer.Exit(5)

@app.command("add-submodule", hidden=True)
def add_submodule():
    console.print("Uninplimented")
    typer.Exit(5)






if __name__ == "__main__":
    app()
