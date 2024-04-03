import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

__version__ = "0.0.0"
REPO_NAME = 'Algorithm-Visualizer'
SRC_REPO =  'Algorithm_Visualizer'
AUTHOR_NAME = 'CC-KEH'
AUTHOR_EMAIL = 'cckeh08@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description='Algorithm Visualizer',
    long_description=long_description,
    url=f"https/github.com/{AUTHOR_NAME}/{REPO_NAME}",
    package_dir={"": "Algorithm_Visualizer"},
    packages=setuptools.find_packages(where='Algorithm_Visualizer')
)
