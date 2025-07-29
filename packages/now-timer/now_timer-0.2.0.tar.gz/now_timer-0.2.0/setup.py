from setuptools import setup, find_packages
setup(
    name='now-timer',
    version='0.2.0',
    author='Eden Simamora',
    author_email='aeden6877@gmail.com',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'now-time=now_time.core:main',
        ],
    },
    description='A simple Python package to display the current time in various formats.',
    long_description_content_type="text/markdown",
    url='https://github.com/yourusername/now-time',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
    