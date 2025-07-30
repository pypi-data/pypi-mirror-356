# Ezpub [cli-environment]

## Tool to help developer to publish package to PyPI

## Installation

```Terminal
pip3 install Ezpub-karjakak
```

>**Ezpub require setuptools as back-end engine and pyproject.toml file (setup.cfg is optional).**

## Usage

**Create token for variable environment and save it for publish with twine [token key-in in tkinter simpledialog for showing in hidden].**

```Terminal
ezpub -t None
```

**Delete saved token.**

```Terminal
ezpub -t d
```

**Create save token.**

```Terminal
# Windows
ezpub -t %VARTOKEN%

# MacOS X
ezpub -t $VARTOKEN
```

**Building the package and create [build, dist, and package.egg-info] for uploading to PyPI.**

```Terminal
# Window
ezpub -b .\package-path\

# MacOS X
ezpub -b ./package_path/
```

**TAKE NOTE:**

* **Ezpub will try to move existing [build, dist, and package.egg-info] to created archive folder and create new one.**
  * **If Exception occured, user need to remove them manually.**

**Pubish to PyPI.**

```Terminal
# For Windows only
ezpub -p .\package-path\dist\*

# For MacOS X
ezpub -p ./package_path/dist/*
```

**TAKE NOTE:**

* **If token is not created yet, ~~it will start process "-t" automatically~~ user will be prompt to create first.**
* **Some firewall not allowed moving files to archive, you may exclude Ezpub from it.**
* **You can move the files manually and using `py -m build`  instead. [Please see the source code for assurance]**
* **MacOS X:**
  * **Extra secure with locking.**
* **Dependency:**
  * **twine**
  * **Clien**
  * **filepmon**
  * **filfla**

## Links

* **<https://packaging.python.org/tutorials/packaging-projects/>**

* **<https://twine.readthedocs.io/en/latest/>**
