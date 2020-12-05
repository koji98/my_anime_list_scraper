import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_anime_list_scraper",
    version="0.0.45",
    author="Chidi Udeze",
    author_email="chidiu98@gmail.com",
    description="A scraper for www.myanimelist.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koji98/my_anime_list_scraper",
    # py_modules=["scraper"],
    packages=setuptools.find_packages(),
    # package_dir={ '':'my_anime_list_scraper'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
