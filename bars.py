import json, os, math, sys


def load_data(filepath):
	if not os.path.exists(filepath):
		return None
	with open(filepath, 'r', encoding='utf-8') as file_handler:
		return json.load(file_handler)


def get_biggest_bar(data):
	max_bar = max(data, key=lambda x: x['Cells']['SeatsCount'])
	return max_bar


def get_smallest_bar(data):
	min_bar = min(data, key=lambda x: x['Cells']['SeatsCount'])

	return min_bar


def get_closest_bar(data, longitude, latitude):
	y = data[0]['Cells']['geoData']['coordinates'][0]
	x = data[0]['Cells']['geoData']['coordinates'][1]
	min_dist = calc_dist(longitude,latitude,x,y)
	for bar in data:
		curent_bar = bar
		y = curent_bar['Cells']['geoData']['coordinates'][0]
		x = curent_bar['Cells']['geoData']['coordinates'][1]
		dist = calc_dist(longitude, latitude, x, y)
		if dist < min_dist:
			min_dist = dist
			name = curent_bar['Cells']['Name']
	return name

def calc_dist(x1,y1,x2,y2):

	# rad - радиус сферы (Земли)
	rad = 6372795

	# исходное местоположение
	llat1 = x1
	llong1 = y1

	# координаты двух точек (метоположение бара)
	llat2 = x2
	llong2 = y2

	# в радианах
	lat1 = llat1 * math.pi / 180.
	lat2 = llat2 * math.pi / 180.
	long1 = llong1 * math.pi / 180.
	long2 = llong2 * math.pi / 180.

	# косинусы и синусы широт и разницы долгот
	cl1 = math.cos(lat1)
	cl2 = math.cos(lat2)
	sl1 = math.sin(lat1)
	sl2 = math.sin(lat2)
	delta = long2 - long1
	cdelta = math.cos(delta)
	sdelta = math.sin(delta)

	# вычисления длины большого круга
	y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
	x = sl1 * sl2 + cl1 * cl2 * cdelta
	ad = math.atan2(y, x)
	distance = ad * rad
	return distance


if __name__ == '__main__':
	if len(sys.argv) > 1:
		filepath = sys.argv[1]
	else:
		print("Отсутствует путь к файлу. Смотрите инструкцию по запуску программы в README.md")
		exit();
	bars = load_data(filepath)
	if bars is None:
		print("Неверный путь к файлу")
		exit();

	p1 = float(input("Введите первую координату\n"))
	p2 = float(input("Введите вторую координату\n"))
	big_bars = get_biggest_bar(bars)
	format_big_bars = 'Самый большой бар - {0}. Вместимость - {1}'.format(big_bars['Cells']['Name'], big_bars['Cells']['SeatsCount'])
	print(format_big_bars)
	small_bars = get_smallest_bar(bars)
	format_small_bars = 'Самый маленький бар - {0}. Вместимость - {1}'.format(small_bars['Cells']['Name'], small_bars['Cells']['SeatsCount'])
	print(format_small_bars)
	closest_bar = get_closest_bar(bars, p1, p2)
	print("Самый близкий бар - ", closest_bar)
	pass