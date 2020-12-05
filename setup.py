import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_anime_list_scraper", # Replace with your own username
    version="0.0.3",
    author="Chidi Udeze",
    author_email="chidiu98@gmail.com",
    description="A scraper for www.myanimelist.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koji98/my_anime_list_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
