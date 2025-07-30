from setuptools import setup, find_packages

setup(
    name='machine-learning-toolkit',
    version='0.1.0',
    description='Utility for evaluating ML models with scikit-learn',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=1.0.0',
        'matplotlib>=3.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
