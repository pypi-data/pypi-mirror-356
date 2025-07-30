from setuptools import setup, find_packages

setup(
    name='ghostsignal',
    version='0.1.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'openai',
        'python-dotenv',
        'face_recognition',
        'mediapipe',
        'cvlib',
        'opencv-python',
        'pytesseract',
        'exifread',
        'pygame',
        'imageio',
        'gTTS',
        'Pillow',
        'rich',
        'googlesearch-python'
    ],
    entry_points={
        'console_scripts': [
            'ghostsignal=ghostsignal.main:main'
        ]
    },
    author='Cure',
    description='GhostSignal: AI Hacker Assistant for OSINT',
    keywords='osint ai face-recognition terminal gpt hacker',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
