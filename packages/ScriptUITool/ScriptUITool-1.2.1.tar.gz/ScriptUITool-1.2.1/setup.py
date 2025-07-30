from setuptools import setup, find_packages
import os
from ScriptUITool import __version__


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ScriptUITool',
    version=__version__,
    author='孙亮',
    packages=['ScriptUITool'],
    install_requires=[
        'pySide2',
        'NewThread',
        'FileKit',
    ],
    # package_data={'AdminToolsDjango': ['template-1.0/*', 'template-1.0/app_test', 'template-1.0/app_test/migrations',
    #                                    'template-1.0/project_name', 'template-1.0/static']},
    package_data={
        'ScriptUITool': ['ui/StartUI.ui'],
    },
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
)








