from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

setup(
    name="vitessestack_common",
    version="0.0.6",
    description="Common libraries for Vitessestack APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Santiago Melo Medina",
    author_email="smelomedina05@gmail.com",
    url="https://github.com/VitessestackTech/APICommons",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
