from setuptools import setup, find_packages

setup(
    name='wolf-cybersecurity-toolkit',
    version='0.1.0',
    author='S. Tamilselvan',
    author_email='tamilselvanresearcher@gmail.com',
    description='A powerful cybersecurity toolkit for Wi-Fi, subdomain, directory attacks, brute-force, CSRF, and more.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Tamilselvan-S-Cyber-Security/Wolf-Cybersecurity-Toolkit.git',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'scapy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
