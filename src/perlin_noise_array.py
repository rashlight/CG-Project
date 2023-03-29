import numpy as np
from PIL import Image
from noise import pnoise2

def gen(width, height, tall, chunks):
    print("Gen noise...")

    # Define and Perlin noise parameters
    width *= chunks
    height *= chunks
    scale = 10.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = np.random.randint(0, 31415)

    # Generate Perlin noise
    perlin_noise = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            perlin_noise[y][x] = pnoise2(x/scale, y/scale, octaves=octaves, persistence=persistence,
                                         lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)

    # Normalize the noise to a 0-16 range
    perlin_noise = (perlin_noise - perlin_noise.min()) * tall / \
        (perlin_noise.max() - perlin_noise.min())
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
    grayscale_array = np.array(grayscale_array)

    final_array = []
    for index, value in np.ndenumerate(grayscale_array):
        x, y = index  # row - col
        value = grayscale_array[x, y]
        value_list = []
        for i in range(value + 1):
            value_list.append([x, y, i])
        final_array.append(value_list)

    # Splits the madness into chunks part
    really_final_array = []
    num_sublists = chunks
    chunk_size = len(final_array) // num_sublists 
    for i in range(0, len(final_array), chunk_size):
        really_final_array.append(final_array[i:i+chunk_size])

    # Turn 4-dimen madness into 2
    actual_final_array = []
    for chunk in really_final_array:
        container = []
        for col in chunk:
            for block in col:
                container.append(block)
        actual_final_array.append(container)

    # Normalize the madness
    for chunk in actual_final_array:
        samplex, sampley, samplez = chunk[0]
        for block in chunk:
            block[0] -= samplex
            block[1] -= sampley

    print("noise done.")

    return actual_final_array
