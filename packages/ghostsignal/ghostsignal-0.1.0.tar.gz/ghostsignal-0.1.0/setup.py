from setuptools import setup, find_packages

setup(
    name='ghostsignal',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'openai',
        'python-dotenv',
        'face_recognition',
        'Pillow',
        'deepface',
        'gTTS',
        'pygame',
        'imageio',
        'rich',
        'googlesearch-python',
        'exifread',
        'pytesseract'
    ],
    entry_points={
        'console_scripts': [
            'ghostsignal=ghostsignal.main:main'
        ]
    },
    author='Cure',
    description='GhostSignal: AI Hacker Assistant for OSINT',
    keywords='osint ai gpt terminal hacker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
