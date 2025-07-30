from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='env-factory',
    version='1.1.0',
    description='A flexible Python package for retrieving environment variables from multiple sources including local environment and AWS Secrets Manager',
    long_description=description,
    long_description_content_type="text/markdown",
    author='Deepak M S',
    author_email='deepakcoder80@gmail.com',
    # url='https://github.com/your-username/env-factory',  # Update with your actual GitHub repo
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Security',
    ],
    keywords='environment variables, aws secrets manager, configuration, secrets, env, dotenv',
    python_requires='>=3.8',
    install_requires=[
        'sm-env-read>=1.1.0',
        'python-dotenv'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'mypy>=1.0.0',
        ],
        'dotenv': [
            'python-dotenv>=1.0.0',
        ],
        'sm_env_read':[
            'sm-env-read>=1.1.0',
        ]
    },
    entry_points={
        'console_scripts': [
            # Add console scripts if needed in future
        ],
    },
    # project_urls={
    #     'Bug Reports': 'https://github.com/your-username/env-factory/issues',
    #     'Source': 'https://github.com/your-username/env-factory',
    #     'Documentation': 'https://github.com/your-username/env-factory#readme',
    # },
    license='MIT',
    zip_safe=False,
    include_package_data=True,
)