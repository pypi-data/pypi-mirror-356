from setuptools import setup, find_packages

setup(
    name="gg-research-community-playbook",  # パッケージ名
    version="0.1.1",  # バージョン
    author="Galirage, Inc.",
    author_email="info@galirage.com",
    description="A package for spreadsheet data loader to process with LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/galirage/gg-research-community-playbook",  # GitHubリポジトリなど
    packages=find_packages(exclude=["tests*", "tests"]),
    include_package_data=True,
    install_requires=["matplotlib"],
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
