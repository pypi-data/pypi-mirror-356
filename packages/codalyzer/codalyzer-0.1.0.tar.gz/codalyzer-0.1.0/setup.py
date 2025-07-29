from setuptools import setup, find_packages

setup(
    name='codalyzer',
    version='0.1.0',
    description='Advanced Python Code Analyzer with Graphs and Real-time Sync',
    author_email='aeden6877@gmail.com',
    author='Adam Alcander et Eden',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'colorama',
        'requests',
        'tqdm',
        'psutil',
        'rich',
        'pygments',
        'tabulate',
        'socketify'
    ],
    entry_points={
        'console_scripts': [
            'codalyzer=codalyzer.core:main'
        ]
    },
    python_requires='>=3.7',
)
