from setuptools import setup

setup(
    name='iota-exrate-manager',
    version='0.1.5',    
    description='A thread safe, stateless python package that manages your receiving dust address',
    url='https://github.com/F-Node-Karlsruhe/iota-exrate-manager',
    author='F-Node-Karlsruhe',
    author_email='contact@f-node.de',
    license='MIT License',
    packages=['iota_exrate_manager'],
    install_requires=[
                    'certifi>=2021.5.30',
                    'charset-normalizer>=2.0.3',
                    'idna>=3.2',
                    'requests>=2.26.0',
                    'urllib3>=1.26.6 ',                 
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Programming Language :: Python :: 3',
    ],
)