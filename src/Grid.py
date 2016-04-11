from Essential_functions import get_collides_objects

class Grid(object):
	def __init__(self, cell_w, cell_h, board_w, board_h):
		self.cell_w, self.cell_h = cell_w, cell_h
		rows_number = (board_h + cell_h - 1) / cell_h
		collumns_number = (board_w + cell_w - 1) / cell_w
		self.array = [[[] for _ in range(rows_number)] for _ in range(collumns_number)]
	def __get_positons(self, obj):
		left = max(0, obj.x / self.cell_w)
		right = min(len(self.array) - 1, (obj.x + obj.w) / self.cell_w)
		up = max(0, obj.y / self.cell_h)
		down = min(len(self.array[0]) - 1, (obj.y + obj.h) / self.cell_h)
		return (left, right, up, down)
	def add(self, obj):
		"Dodaje obiekt do siatki"
		left, right, up, down = self.__get_positons(obj)
		for row in range(up, down + 1):
			for collumn in range(left, right + 1):
				self.array[collumn][row].append(obj)
	def remove(self, obj):
		"Usuwa obiekt z siatki"
		left, right, up, down = self.__get_positons(obj)
		for row in range(up, down + 1):
			for collumn in range(left, right + 1):
				self.array[collumn][row].remove(obj)
	def check(self, obj):
		"Zwraca liste obiektow bedacych w kolizji z obiektem wejsciowym"
		left, right, up, down = self.__get_positons(obj)
		collides = []
		for row in range(up, down + 1):
			for collumn in range(left, right + 1):
				for elem in get_collides_objects(obj, self.array[collumn][row]):
					if elem not in collides:
						collides.append(elem)
		return collides
