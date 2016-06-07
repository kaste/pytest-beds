from setuptools import setup

setup(
    name="pytest-beds",
    version='0.3.0',
    description='Fixtures for testing Google Appengine (GAE) apps',
    long_description=open('README.rst').read(),
    license='MIT',
    author='herr kaste',
    author_email='herr.kaste@gmail.com',
    url='https://github.com/kaste/pytest-beds',
    platforms=['linux', 'osx', 'win32'],
    packages=['testbeds'],
    entry_points={'pytest11': ['testbeds = testbeds.plugin'], },
    zip_safe=False,
    install_requires=['pytest>=2.4.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Utilities',
        'Programming Language :: Python',
    ],
)
