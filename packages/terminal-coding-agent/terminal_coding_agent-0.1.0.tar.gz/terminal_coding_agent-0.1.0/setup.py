from setuptools import setup, find_packages

setup(
    name='terminal-coding-agent',
    version='0.1.0',
    description='Terminal-based AI coding assistant using OpenAI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Keshav Tiwari',
    author_email='keshav.tiwari623@email.com',
    url='https://github.com/KeshavTiwari373/terminal-coding-agent',
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
        'rich',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'code-agent=terminal_coding_agent.agent:agent_chat_loop',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
