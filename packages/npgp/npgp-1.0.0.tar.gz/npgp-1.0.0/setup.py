from setuptools import setup, find_packages

setup(
    name="npgp",
    version="1.0.0",
    description="A CLI to create new Pygame project from a template",
    author="clxakz",
    author_email="zolotarjovdavid15@gmail.com",
    packages=find_packages(),
    package_data={
        "npgp": ["templates/*.py"],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "npgp=npgp.cli:create_project",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
