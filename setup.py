from setuptools import setup, find_packages

setup(
    name='dqlite',
    version='0.1',
    packages=find_packages(),
    license='MIT',
    description='An example Python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # List your package dependencies here
        # 'numpy>=1.18.1',
    ],
    url='https://github.com/yourusername/my_package',
    author='Maxim',
    author_email='your.email@example.com',
    entry_points={
        'dqlite.database_adapters': [
            'clickhouse = dq.clickhouse:ClickhouseAdapter',
            'sqlite = dq.sqlite:SQLiteAdapter'
        ],
    },
)
