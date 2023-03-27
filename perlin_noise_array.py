import numpy as np
from PIL import Image
from noise import pnoise2

# Define image size and Perlin noise parameters
width = 64
height = 64
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = np.random.randint(0, 100)

# Generate Perlin noise
perlin_noise = np.zeros((height, width))
for y in range(height):
    for x in range(width):
        perlin_noise[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)

# Normalize the noise to a 0-255 range
perlin_noise = (perlin_noise - perlin_noise.min()) * 255 / (perlin_noise.max() - perlin_noise.min())
perlin_noise = perlin_noise.astype(np.uint8)

# Convert the noise to a grayscale image
image = Image.fromarray(perlin_noise, mode='L')


image.save('perlin_noise.png')
width, height = image.size
    
# Initialize the 2D array with zeros
grayscale_array = [[0 for y in range(height)] for x in range(width)]

# Loop through each pixel in the image and get its grayscale value
for x in range(width):
    for y in range(height):
        grayscale_value = image.getpixel((x, y))
        grayscale_array[x][y] = grayscale_value
grayscale_array=np.array(grayscale_array)

final_array = []
for index, value in np.ndenumerate(grayscale_array):
    x, y = index #row - col
    value = grayscale_array[x,y]
    value_list = []
    for i in range(value + 1):
        value_list.append([x,y,i])
    final_array.append(value_list)



