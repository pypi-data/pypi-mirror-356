from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="crazyagent",  # 包名
    version="1.0.3",  # 版本号
    description="A minimal, efficient, easy-to-integrate, flexible, and beginner-friendly LLM agent development framework with powerful context management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CrazySand",
    author_email="lyt041006@gmail.com",
    url="https://github.com/Crazysand/crazyagent",
    project_urls={
        "Bug Tracker": "https://github.com/Crazysand/crazyagent/issues",
        "Source Code": "https://github.com/Crazysand/crazyagent",
    },
    install_requires=[
        "colorama>=0.4.6",
        "typeguard>=4.4.4",
        "tabulate>=0.9.0",
        "openai>=1.86.0",
        "requests>=2.32.3",
    ],
    license="MIT",
    packages=find_packages(),  # 使用 find_packages() 自动查找所有子模块
    platforms=["any"],
    python_requires=">=3.10",
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
)