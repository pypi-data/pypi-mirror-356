from setuptools import setup, find_packages

# Optional: read version from VERSION file
with open("VERSION") as f:
    version = f.read().strip()

setup(
    name='QAppuccinoLibrary',  # ✅ Unique name (must NOT conflict with existing PyPI package!)
    version=version,
    description='Reusable Robot Framework keyword library for QAppuccino TestOps',
    author='Eric Zamora',
    author_email='eric.zamora@lpstech.com',
    url='https://github.com/LPS-PH-ODC/QAppuccinoLibrary',
    packages=find_packages(),
    package_data={'qappuccino': ['*.resource']},
    include_package_data=True,
    install_requires=[
        'robotframework',
        'robotframework-seleniumlibrary',
    ],
    classifiers=[
        "Framework :: Robot Framework",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
