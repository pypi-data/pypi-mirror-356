from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='colorsearch',
    version='1.0.0',
    description='Search images and videos by dominant color (PyQt6)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zaman Huseyinli',
    author_email='zamanhuseynli23@gmail.com',
    py_modules=['colorsearch'],
    install_requires=[
        'Pillow>=9.0.0',
        'PyQt6>=6.4.0',
    ],
    entry_points={
        'console_scripts': [
            'colorsearch=colorsearch:main',
        ],
    },
    data_files=[
        ('share/applications', ['colorsearch.desktop']),
        ('share/icons/hicolor/64x64/apps', ['colorsearch.svg']),
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: X11 Applications :: Qt',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Graphics',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.8',
)
