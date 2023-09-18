from setuptools import setup, find_packages
from qupyter import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='qupyter',
    version=__version__,
    description='A Python library for quantitative finance.',
    url='https://github.com/qrstai/qupyter',
    author='QRST AI',
    author_email=('qrst.partners@gmail.com',),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'pandas', 'boto3'],
    license='MIT',
    packages=find_packages(),
    python_requires='>=3',
    zip_safe=False,
)

