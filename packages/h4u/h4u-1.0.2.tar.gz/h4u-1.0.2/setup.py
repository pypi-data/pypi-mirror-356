from setuptools import setup, find_packages

#leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
	long_description =fh.read()

setup(
	name="h4u",
	version="1.0.2",
	packages=find_packages(),
	install_requires=[],
	author="Jhonnas Iriarte",
	description="Una biblioteca ficticia para consultar cursos fitcticios con links a paginas publicas no relacionadas.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://www.proventutprials.org/",
)

