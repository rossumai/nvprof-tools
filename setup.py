from setuptools import setup

setup(name='nvprof',
      version='0.1',
      description='NVIDIA Profier tools',
      url='https://github.com/rossumai/nvprof-tools',
      author='Bohumir Zamecnik',
      author_email='bohumir.zamecnik@gmail.com',
      license='MIT',
      packages=['nvprof'],
      zip_safe=False,
      install_requires=[
      ],
      setup_requires=['setuptools-markdown'],
      long_description_markdown_filename='README.md',
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 3',

          'Operating System :: POSIX :: Linux',
      ],
      entry_points={
          'console_scripts': [
              'nvprof_tools = nvprof.__main__:main'
          ]
      },)
