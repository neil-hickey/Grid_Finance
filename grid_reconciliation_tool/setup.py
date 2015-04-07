from setuptools import setup

setup(
      name='Grid Reconiciliation Tool', 
      version='1.0',
      description='Web application for reconciling payments',
      author='Group One Point Eight - Trinity College Dublin',
      url='http://www.tcd.ie/',
      packages=['reconciliation_tool'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['Flask',
                        'pandas',
      ],
     )