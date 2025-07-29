from setuptools import setup, find_packages

setup(
    name='Tkinter-MSSQL',
    version='0.2.3',
    description='Приложение для управления заявками и партнерами на базе Microsoft SQL Server',
    author='John Doe',
    author_email='thenonnss45@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pyodbc',
        'pillow',
    ],
    entry_points={
        'console_scripts': [
            'MSSQL = MSSQL.main:main'
        ]
    },
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
) 