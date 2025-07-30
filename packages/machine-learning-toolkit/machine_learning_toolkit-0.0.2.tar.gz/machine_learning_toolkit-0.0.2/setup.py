from setuptools import setup

setup(
    name='machine-learning-toolkit',
    version='0.0.2',
    description='Utility for evaluating ML models with scikit-learn',
    author='Your Name',
    author_email='your.email@example.com',
    packages=["machine_learning_toolkit"],
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
