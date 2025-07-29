# Guide to additional Python dependencies in Functions

Before bundling this template run:

```sh
python run-before-bundle/install_deps_to_lib.py
```

Then bundle as usual.

## How to add custom additional dependencies

Before running the setup script from above, add your dependencies to the `run-before-bundle/requirements.txt` file.

## Improve development experience

To get autocompletion for the extra packages in your editor, you can install the packages to your local Python enviroment:

```sh
pip install -r run-before-bundle/requirements.txt
```

Or add the generated `lib` folder to `python.analysis.extraPaths` if your editor supports that (e.g. VSCode, Cursor do).

## Getting `platform-warning` log

If you get a log indicating platform specific packages installed, make sure that the zip is bundled on a computer with the `x86_64` architecture.

Bundling with this warning on e.g. a macOS machine will cause the Function zip not to work in production.
