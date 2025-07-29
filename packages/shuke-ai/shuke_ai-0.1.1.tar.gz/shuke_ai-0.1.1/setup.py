from setuptools import setup, find_packages

setup(
    name="shuke-ai",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "PyQt6==6.6.1",
        "requests==2.31.0",
        "urllib3==2.2.1",
        "python-dotenv>=0.19.0",
        "opencv-python>=4.6.0",
        "pillow>=9.0.0",
        "numpy>=1.21.0"
    ],
    entry_points={
        'console_scripts': [
            'shuke-ai=shuke_ai.main:main',
        ],
    },
    author="Chaiyapeng",
    author_email="your.email@example.com",
    description="舒克AI工具集 - AI工具箱",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shuke-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        'shuke_ai': ['assets/*'],
    },
) 