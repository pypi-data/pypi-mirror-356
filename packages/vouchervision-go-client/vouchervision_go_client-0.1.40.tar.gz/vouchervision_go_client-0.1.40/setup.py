from setuptools import setup, find_packages

'''
python -m build
python -m twine upload dist/* --verbose
'''

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vouchervision-go-client",
    version="0.1.40",  # Incremented version
    author="Will",
    author_email="willwe@umich.edu",
    description="Client for VoucherVisionGO API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gene-Weaver/VoucherVisionGO-client",
    project_urls={
        "Bug Tracker": "https://github.com/Gene-Weaver/VoucherVisionGO/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    py_modules=["client", "list_prompts"],  # Added list_prompts.py
    python_requires=">=3.10",
    install_requires=[
        "requests",
        "termcolor",
        "tabulate",
        "tqdm",
        "pyyaml",  # Added for list_prompts.py
    ],
    extras_require={
        "analytics": ["pandas"],
        "full": ["pandas"],
    },
    entry_points={
        "console_scripts": [
            "vouchervision=client:main",  # Original client entry point
            "vv-prompts=list_prompts:main",  # New entry point for list_prompts
        ],
    },
)