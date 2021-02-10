from setuptools import setup, find_packages


setup(
    name="guided_tours_lib",
    version="0.0.1",
    description="Guided tours shared lib",
    author="Lorcan Leonard",
    author_email="lorcanleonard@gmail.com",
    packages=find_packages(),
    namespace_packages=["guided_tours_lib"],
    zip_safe=False,
)
