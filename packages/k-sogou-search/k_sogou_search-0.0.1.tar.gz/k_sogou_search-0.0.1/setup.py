import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="k-sogou-search",
    version="0.0.1",
    author="li-xiu-qi",
    author_email="lixiuqixiaoke@qq.com",
    description="A simple unofficial API to get search results from Sogou.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/li-xiu-qi/sogou_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
)
