from setuptools import setup, find_packages

setup(
    name="anujscan",
    version="1.0.0",
    description="AnujScan - GUI-based Penetration Testing Toolkit",
    author="Anuj Prajapati",
    author_email="anujprajapati2109@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "anujscan": ["assets/*"]
    },
    install_requires=[
        "pillow",
        "requests",
        "whois"
    ],
    entry_points={
        "console_scripts": [
            "anujscan=anujscan.__main__:show_splash"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
