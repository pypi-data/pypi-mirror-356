from setuptools import setup, find_packages

# Read requirements.txt into a list
with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='FPT-Diffusion',
    version='0.1.3',
    author='martinj',
    author_email='martinj1@student.ubc.ca',
    description = "Free Particle Tracking (for) Diffusion. SPT, MPT, image processing, and other tools for research scientists around the world. ",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
)
