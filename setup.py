from setuptools import setup, find_packages

ver = "0.0.1"

setup(
      name = "telepythy",
      version = ver,
      packages = find_packages(),
      author = "Eric Seifert",
      author_email = "seiferteric@gmail.com",
      description = "Remote python function runner",
      keywords = "remote distributed",
      url = "https://github.com/seiferteric/telepythy",
      zip_safe = True,
      install_requires = ['paramiko'],
)
