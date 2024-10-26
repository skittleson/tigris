from pybars import Compiler
import os
import shutil
from rich.console import Console
from dotenv import dotenv_values
import datetime

console = Console()
target_dir = "docs"
source_dir = "src"


def get_partials(compiler):
    partial_files = [file for file in os.listdir(os.path.join(source_dir, "partials"))]
    partials = {}
    for partial_file in partial_files:
        with open(
            os.path.join(source_dir, "partials", partial_file), "r", encoding="utf-8"
        ) as file:
            partials[partial_file.replace(".hbs", "")] = compiler.compile(file.read())
    return partials


def static_content_builder():
    compiler = Compiler()
    partials = get_partials(compiler)
    files = [file for file in os.listdir(source_dir) if file.endswith(".hbs")]
    for file in files:
        console.log(f"processing {file}")
        with open(f"{source_dir}/{file}", "r", encoding="utf-8") as source:

            # Arrange the template and values
            template = compiler.compile(source.read())
            context = dotenv_values(".env")
            context["year"] = datetime.datetime.now().year
            result = template(context, partials=partials)
            folder_name = file.replace(".hbs", "")
            target_html_destination = f"{target_dir}/{folder_name}/index.html"

            # home page get a special directory
            if "index.hbs" in file:
                target_html_destination = f"{target_dir}/index.html"
            else:
                os.makedirs(f"{target_dir}/{folder_name}", exist_ok=True)

            # Output response
            with open(target_html_destination, "+x", encoding="utf-8") as html_file:
                html_file.write(result)


def preprocess() -> None:
    """Hot reloadable preprocess clean up event"""

    def delete_all_in_directory(directory_path):
        """Delete all the files/folders in a directory WITHOUT deleting the parent directory"""
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"{directory_path} is not a valid directory")

        # Iterate over all items in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            # Check if it's a file or directory and delete accordingly
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    console.log(f"Clean up {target_dir}")
    delete_all_in_directory(f"{target_dir}/")


def copy_assets():
    console.log("Copy assets and images")
    shutil.copytree(f"{source_dir}/assets", f"{target_dir}/assets")
    shutil.copytree(f"{source_dir}/images", f"{target_dir}/images")
    files = [file for file in os.listdir(source_dir) if not file.endswith(".hbs")]
    for file in files:
        if "." in file:
            shutil.copy(f"{source_dir}/{file}", f"{target_dir}/{file}")
            console.log(f"Copying {file}")


if __name__ == "__main__":
    preprocess()
    static_content_builder()
    copy_assets()
