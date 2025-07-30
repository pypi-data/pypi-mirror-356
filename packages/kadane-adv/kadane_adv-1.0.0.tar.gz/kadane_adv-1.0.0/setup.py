from setuptools import setup, find_packages

setup(
    name="kadane-adv",
    version="1.0.0",
    description="Advanced Kadane's Algorithm Library with visualization and constraints",
    author="Krunal Wankhade , Parimal Kalpande",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
