from setuptools import setup, find_packages

setup(
    name="PuQTSqlite",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'PuQTSqlite': ['req/*'],
    },
    install_requires=[
        # Здесь будут зависимости из вашего requirements.txt
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to distribute your PyQt SQLite program files",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/PuQTSqlite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 