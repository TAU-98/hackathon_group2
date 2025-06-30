from setuptools import setup, find_packages

setup(
    name='hackathon-madm-experiment',
    version='0.1',
    description='Python implementation of a multi-attribute decision-making experiment with (mock) eye-tracking.',
    author='Your Name',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'pytest',
        'pygame',
    ],
    include_package_data=True,
    python_requires='>=3.7',
) 