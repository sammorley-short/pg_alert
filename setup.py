from setuptools import setup, find_packages

setup(
    name='pg_alert',
    version='0.0.1',
    # url='https://github.com/mypackage.git',
    author='Sam Morley-Short',
    author_email='sam.morleyshort@gmail.com',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        'selenium>=3.141.0,<4.0.0',
        'python-dateutil>=2.8.1,<3.0.0',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
    ],
)
