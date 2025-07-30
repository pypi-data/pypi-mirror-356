from setuptools import setup, find_packages

setup(
    name='dig-flask-serve',
    version='1.1.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dig_flask_serve': ['static/*'],
    },
    install_requires=[
        'flask>=2.0'
    ],
    description='A lightweight and pluggable model serving framework based on Flask.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='zsj',
    author_email='zhaishujie2@buaa.edu.cn',
    url='https://gitee.com/buaa717/dig-flask-serve.git',  # 可选
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
