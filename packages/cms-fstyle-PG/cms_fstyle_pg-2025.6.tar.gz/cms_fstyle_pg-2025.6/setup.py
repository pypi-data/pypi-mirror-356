from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="cms_fstyle_PG",
    version="2025.06",
    author="Fabrice Couderc",
    author_email="fabrice.couderc@cea.ch",
    description="Package to get a proper matplolib style and ROOT-type histogram plotting and some stat/fitting methods",
    include_package_data=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.cern.ch/fcouderc/cms_fstyle",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=['pandas', 'matplotlib', 'numpy'],
    extras_require={'fitter': 'scikit-learn'}
)
