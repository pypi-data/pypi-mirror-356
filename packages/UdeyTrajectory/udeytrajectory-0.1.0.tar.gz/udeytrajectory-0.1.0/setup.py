from setuptools import setup, find_packages

setup(
    name='UdeyTrajectory',               # Use a unique name!
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],                   # List dependencies here
    author='Andrew Lin',
    author_email='hungryc9@gmail.com',
    description='This is Humaniize trajectorry calculation module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
