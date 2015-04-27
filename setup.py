from setuptools import setup, find_packages

setup(
    name='Starbucks',
    packages=find_packages(),
    version='0.5.2',
    description='Unoffical Starbucks API.',
    long_description=open('README.rst').read(),
    license='BSD License',
    author='Minsoo Park',
    author_email='minsoo1003@gmail.com',
    url='https://github.com/minsoopark/starbucks-py',
    keywords=['Starbucks'],
    install_requires=[
        'click >= 3.3', 'requests >= 2.5.3', 'lxml >= 3.0.0'
    ],
     entry_points='''
        [console_scripts]
        starbucks-card = starbucks.cli:card_info
        starbucks-star = starbucks.cli:star_info
    '''
)
