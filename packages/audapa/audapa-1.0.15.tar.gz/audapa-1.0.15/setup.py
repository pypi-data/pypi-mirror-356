ver="1.0.15"
README="""To remove configuration files launch the program with one argument.\\
PortAudio can ask for portaudio.h (the file is in portaudio19-dev(ubuntu),portaudio-devel(fedora)).\\
PyAudio and python 3.10 can report playback errors (install from [here](https://github.com/colin-i/pyaudio) and add libportaudio2 package).\\
The audio records are saved where *appdirs.user_data_dir("audapa")* points at (example: ~/.local/share/audapa/1650089398.wav).\\
The points are saved in the *\\_audapacache\\_* folder which is at the file folder or in the home folder if the option is selected. (example: /home/x/audapa/\\_audapacache\\_/example.wav.json or /home/x/\\_audapacache\\_/home/x/audapa/example.wav.json)\\
Knowing where the points are saved, in the root folder at source, write "example.wav" and click the build button from top-right.\\
[Git Page](https://github.com/colin-i/audapa)
"""

#the .pre.py file is making the .py file after using github colin-i test/pyp/pypre
#pip install --user .
#pip uninstall audapa

pkname='audapa'

from setuptools import setup
setup(name=pkname,
	version=ver,
	packages=[pkname],
	#optionals
	#cmdclass={
	#	'build_py': BuildPyCommand
	#},
	#include_package_data=True,
	python_requires='>=3.8',   #for :=
	install_requires=[
		"pycairo>=1.20.0","PyGObject>=3.40",
		#this combination will work from pip, with ubuntu pygobject(python3-gi)+pycairo(python3-cairo) it is also required for python3-gi-cairo there
		#                                                 if these are on the system pip is saying requirements ok but will not work
		#to retest this take PyGObject from https://pypi.org/project/PyGObject/#files , install local, and will work

		"appdirs>=1.4.3",
		"PyAudio>=0.2.11"],
	description='Audio wave file manipulator',
	long_description=README,
	long_description_content_type="text/markdown",
	url='https://github.com/colin-i/audapa',
	author='cb',
	author_email='costin.botescu@gmail.com',
	license='MIT',
	entry_points = {
		'console_scripts': [pkname+'='+pkname+'.main:main']
	}
)

#if there is the problem like in info.md with python10:
# now: rpm modified pyaudio is at releases at my pyaudioo project. deb and appimage are ok
#
# for pypi and source:
#	apt download audapa
#	sudo dpkg --ignore-depends=python3-pyaudio -i audapa.......deb
#but then, to not see broken count now and then, must remove python3-pyaudio at audapa package dependencies from /var/lib/dpkg/status
#A SOLUTION: overwrite ./build/lib.linux-x86_64-3.10/_portaudio.cpython-310-x86_64-linux-gnu.so at python3-pyaudio equivalent

#import subprocess
#import setuptools.command.build_py
#class BuildPyCommand(setuptools.command.build_py.build_py):
#  """Custom build command."""
#  def run(self):
#    subprocess.run(['touch','qwerty.so'])
#    subprocess.run(['mv','qwerty.so','audapa'])
#    #MANIFEST.in include audapa/qwerty.so
#    #and include_package_data=True
#    setuptools.command.build_py.build_py.run(self)
