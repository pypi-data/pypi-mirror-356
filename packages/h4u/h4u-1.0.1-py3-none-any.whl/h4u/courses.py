class Course:
	def __init__(self, name, duration, link):
		self.name = name
		self.duration = duration
		self.link = link
#	def __str__(self):
#		return f"{self.name} [{self.duration} horas. Link {self.link}]"

	def __repr__(self):
		return f"{self.name} [{self.duration} horas. Link {self.link}]"
		

courses = [
	Course("Introduccion a Linux", 15, "https://www.google.com/"),
	Course("Personalizacion de Linux", 3, "https://www.microsoft.com/"),
	Course("Introduccion al Hacking", 30, "https://www.amazon.com/")
]

for course in courses:
	print(course)

#print(courses[1]) funciona con el __repr__ para listar por posicionamiento en la lista. aun asi, repr actua como un str


def list_courses():
	for course in courses:
		print(course)

def search_course_by_name(name):
	for course in courses:
		if course.name == name:
			return course
	return None
