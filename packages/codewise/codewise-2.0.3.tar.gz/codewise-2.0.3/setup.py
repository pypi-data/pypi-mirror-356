from setuptools import setup

try:
    with open('requirements.txt', encoding='utf-8') as f:
        required = f.read().splitlines()
except FileNotFoundError:
    required = []

setup(
    name="codewise",
    version="2.0.3",
    author="BPC",
    description="Ferramenta para análise de código e automação de PRs com CrewAI.",
    long_description=open("README.md", encoding="utf-8").read(),  
    long_description_content_type="text/markdown",  

    package_dir={
        'codewise_lib': 'docs/code_wise/codewise/src/codewise',
        'scripts': 'scripts'
    },
    packages=['codewise_lib', 'scripts'],
    package_data={
        'codewise_lib': ['config/*.yaml'],
    },
    include_package_data=True,
    install_requires=required,
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'codewise-pr=scripts.codewise_review_win:main_pr',
            'codewise-lint=scripts.codewise_review_win:main_lint',
            'codewise-init=scripts.install_hook:main',
            'codewise-help=scripts.help:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators"
    ],
)
