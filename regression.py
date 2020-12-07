import numpy as np
import csv
from matplotlib import pyplot as plt


def calculate_regression(x, y):
	x = np.array(x)
	y = np.array(y)

	x2 = x**2
	y2 = y**2

	xy = x*y

	H = [[len(x), sum(x)],
		 [sum(x), sum(x2)]]

	b2 = 1 / np.linalg.det(H) * (len(x) * sum(xy)-sum(x)*sum(y))
	b1 = sum(y)/len(x)-b2*sum(x)/len(x)

	return lambda x: b2 * x + b1


def plot(x, y, xlabel, ylabel):
	plt.figure()
	plt.title("Regression")
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)


	plt.scatter(x, y, s=1, marker='o', label="data")
	x_ = np.linspace(min(x), max(x), 100)
	y_ = calculate_regression(x, y)(x_)
	plt.plot(x_, y_, color="orange", label="regression line")
	plt.legend()
	plt.show()

if __name__ == "__main__":
	lattitude = []
	day_temp = []
	night_temp = []
	with open("dataset.csv", "r") as fd:
		reader = csv.reader(fd)

		for lat, d_t, n_t in reader:
			lattitude.append(float(lat))
			day_temp.append(float(d_t))
			night_temp.append(float(n_t))


	plot(lattitude, day_temp, "Latitude", "Day Temperature [°C]")
	plot(lattitude, night_temp, "Latitude", "Night Temperature [°C]")





