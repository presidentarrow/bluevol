import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bluevol",
    version="0.0.1",
    author="presidentarrow",
    author_email="piyush.galphat@gmail.com",
    description="manage volume of bluetooth headphones",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/presidentarrow/bluevol",
    project_urls={
        "Bug Tracker": "https://github.com/presidentarrow/bluevol/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    package_data={'bluevol': ['/*.glade']},
    entry_points = {
        'console_scripts': ['bluevol=bluevol.index:main'],
    }
)