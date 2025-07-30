from setuptools import setup, find_packages

setup(
    name='cleary',
    version='0.1.0',
    description='Ultimate cross-platform console clearer',
    author='TroubleGy',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'cleary=cleary.__main__:main',
            'Cleary=cleary.__main__:main',
            'CLEARY=cleary.__main__:main',
            'cLeary=cleary.__main__:main',
            'clEary=cleary.__main__:main',
            'cleAry=cleary.__main__:main',
            'cleaRy=cleary.__main__:main',
            'clearY=cleary.__main__:main',
            'clr=cleary.__main__:main',
            'Clr=cleary.__main__:main',
            'CLR=cleary.__main__:main',
            'cLR=cleary.__main__:main',
        ],
    },
    python_requires='>=3.6',
) 