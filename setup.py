from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

version = '0.0.3'

setup(
    name='qupyter',
    version=version,
    description='A Python library for quantitative finance.',
    url='https://github.com/qrstai/qupyter',
    author='QRST AI',
    author_email=('qrst.partners@gmail.com',),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'pandas', 'python-dotenv', 'httpx'],
    license='MIT',
    packages=find_packages(include=['qupyter', 'qupyter.*']),
    python_requires='>=3',
    zip_safe=False,
)

