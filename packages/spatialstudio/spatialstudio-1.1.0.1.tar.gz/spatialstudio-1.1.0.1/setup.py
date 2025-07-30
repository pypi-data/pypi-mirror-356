from setuptools import setup
from setuptools.dist import Distribution

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True  # force wheel to be platform-specific

setup(distclass=BinaryDistribution)