from setuptools import setup, find_packages

setup(
    name='Starbucks',
    packages=find_packages(),
    version='0.1.0',
    description='Unoffical Starbucks API.',
    long_description=open('README.rst').read(),
    license='BSD License',
    author='Minsoo Park',
    author_email='minsoo1003@gmail.com',
    url='https://github.com/minsoopark/starbucks-py',
    keywords=['Starbucks'],
    install_requires=[
        'click >= 3.3', 'requests >= 2.5.3'
    ],
     entry_points='''
        [console_scripts]
        starbucks-card = starbucks.cli:card_info
    '''
)
