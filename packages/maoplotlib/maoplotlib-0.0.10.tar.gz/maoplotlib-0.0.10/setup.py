from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='maoplotlib',
  version='0.0.10',
  author='maoshka',
  author_email='marsohod_mao@mail.ru',
  description='you go girl',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/maomaoshka/maomao',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='mao exam ',
  project_urls={
    'GitHub': 'https://github.com/maomaoshka/maomao'
  },
  python_requires='>=3.6'
)