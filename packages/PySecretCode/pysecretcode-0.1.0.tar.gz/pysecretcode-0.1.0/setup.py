from setuptools import setup, find_packages
setup(
    name='PySecretCode',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[  
        "cryptography",
        "pycryptodome",
        "colorama",
        "rich",
        "pyperclip",
        "pyfiglet",
        "termcolor",
        "pyinstaller",
        "wheel",
        "setuptools",
        "build",
        "pycryptodomex",
        "crcmod",
        "argon2-cffi",
        "mmh3",
        "bcrypt",
],
    entry_points={
        'console_scripts': [
            'pysecretcode = pysecretcode.core:main'
        ]
    },
    author='Eden Simamora',
    description='A Python package for various encryption and hashing algorithms',
    author_email='aeden6877@gmail.com',
    url='https://github.com/yourusername/PySecretCode',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9', 
)