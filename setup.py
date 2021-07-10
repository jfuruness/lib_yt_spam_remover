from setuptools import setup, find_packages
import sys

setup(
    name='lib_yt_spam_remover',
    packages=find_packages(),
    version='0.0.1',
    author='Justin Furuness',
    author_email='jfuruness@gmail.com',
    url='https://github.com/jfuruness/lib_yt_spam_remover.git',
    download_url='https://github.com/jfuruness/lib_yt_spam_remover.git',
    keywords=['Furuness', 'Youtube', 'Spam'],
    install_requires=[
        "google-api-python-client"
        ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'],
    entry_points={
        'console_scripts': 'lib_yt_spam_remover = lib_yt_spam_remover.__main__:main'
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
