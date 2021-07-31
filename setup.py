import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='djangorm',
    version='0.0.1',
    author='Devendra K Rane',
    author_email='ranedk@gmail.com',
    description='Django model to Gorm struct conversion tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ranedk/djangorm',
    project_urls = {
        "Bug Tracker": "https://github.com/ranedk/djangorm/issues"
    },
    license='MIT',
    packages=['djangorm'],
    install_requires=[],
)
