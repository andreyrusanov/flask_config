from distutils.core import setup


setup(
    name='just-another-settings',
    version='0.0.1',
    packages=['just_another_settings'],
    url='https://github.com/andreyrusanov/just-another-settings',
    license='MIT',
    author='Andrey Rusanov',
    author_email='andrey@rusanov.me',
    description='Small lib to manage settings as object for Flask/Bottle/custom apps',
    test_requires=[
        'nose==1.3.7',
        'mock==1.3.0'
    ]
)
