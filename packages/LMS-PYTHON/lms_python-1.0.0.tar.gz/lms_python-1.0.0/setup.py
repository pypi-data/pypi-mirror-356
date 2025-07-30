from setuptools import setup, find_packages

setup(
    name='LMS-PYTHON',                    # Paket adı (PyPI’de benzersiz olmalı)
    version='1.0.0',
    author='CSDC-K VV',
    author_email='mark.mark34234@gmail.com',  # Dilersen gerçek e-posta koy
    description='A License Management System package',
    long_description='Python package for License Management System with server and client modules.',
    long_description_content_type='text/plain',
    url='https://github.com/CSDC-K/LMS',  # GitHub veya projenin URL’si
    packages=find_packages(),       # LMS klasörünü otomatik bulur
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
