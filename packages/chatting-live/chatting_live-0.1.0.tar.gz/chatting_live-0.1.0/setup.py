from setuptools import setup, find_packages

setup(
    name='chatting-live',
    version='0.1.0',
    author='Omer',
    author_email='worthlifefacts@example.com',
    description='A command-line WebSocket Socket.IO chat client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dreamrenderai/chatting-live',
    packages=find_packages(),
    install_requires=[
        'requests',
        'websocket-client'
    ],
    entry_points={
        'console_scripts': [
            'chatting-live=chatting_live.client:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
