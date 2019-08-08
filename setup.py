from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='media_processor',
   version='0.1',
   description='Media processor takes audio, video or images and exports out web ready versions',
   long_description=long_description,
   author='Marek Vymazal',
   packages=['media_processor'],  #same as name
   install_requires=['Pillow', 'fpdf', 'markdown'], #external packages as dependencies
   entry_points={
        'console_scripts': [
                'media_processor = media_processor.__main__:main'
        ]
    },
    #dependency_links = ['git+https://github.com/username/repository.git']
)
