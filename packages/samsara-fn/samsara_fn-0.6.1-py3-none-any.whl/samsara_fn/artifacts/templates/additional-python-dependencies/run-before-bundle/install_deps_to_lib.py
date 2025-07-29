import shutil
import subprocess
import sys
from pathlib import Path


def install_dependencies_to_path(
    dependency_path: str, requirements_file: str
) -> subprocess.CompletedProcess:
    """
    Install dependencies to the given path with pip using --target flag.
    Remove all files in the given path before installation.
    """
    dep_path = Path(dependency_path)
    if dep_path.exists():
        shutil.rmtree(dep_path)

    return subprocess.run(
        ["pip", "install", "-r", requirements_file, "--target", dependency_path],
        check=True,
    )


def clean_up_depedency_path(dependency_path: str):
    """
    Remove files that are not needed in the dependency directory:
    - binary files
    - dist-info files (leaves METADATA)
    - egg-info files (leaves PKG-INFO)
    """
    dep_path = Path(dependency_path)
    bin_dir = dep_path / "bin"
    if bin_dir.exists():
        shutil.rmtree(bin_dir)

    for dist_info in dep_path.glob("*.dist-info"):
        for file_path in dist_info.iterdir():
            if file_path.name.endswith("WHEEL"):
                platform_tag = get_package_platform_tag(str(file_path))
                if platform_tag != "py3-none-any":
                    package_name = dist_info.name.split("-")[0]
                    print(
                        "\033[31m"
                        f"platform-warning: package '{package_name}' is not platform-agnostic (wheel tag '{platform_tag}'). You can proceed with testing it in the simulator, but for production you need to run the dependency installing script on a machine with x86_64 architecture. See the template README for more details."
                        "\033[0m",
                        file=sys.stderr,
                    )

            if not file_path.name.endswith("METADATA"):
                remove(str(file_path))

    for egg_info in dep_path.glob("*.egg-info"):
        for file_path in egg_info.iterdir():
            if not file_path.name.endswith("PKG-INFO"):
                remove(str(file_path))


def remove(path: str):
    path_obj = Path(path)
    if path_obj.is_file():
        path_obj.unlink()
    else:
        shutil.rmtree(path_obj)


def get_package_platform_tag(wheel_file_path: str):
    wheel_file_lines = []
    with Path(wheel_file_path).open("r") as f:
        wheel_file_lines = f.readlines()

    for line in wheel_file_lines:
        line = line.strip()
        if line.startswith("Tag: "):
            # Extract the part after "Tag: "
            return line[5:]  # len("Tag: ") = 5

    # Return None if no Tag line was found
    return None


if __name__ == "__main__":
    current_dir = Path(__file__).parent.resolve()
    lib_dir = current_dir / ".." / "lib"

    install_dependencies_to_path(
        dependency_path=str(lib_dir),
        requirements_file=str(current_dir / "requirements.txt"),
    )

    clean_up_depedency_path(str(lib_dir))
