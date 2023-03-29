import math
import random

import chunk

import block_type
import texture_manager

from perlin_noise_array import gen


class World:
    def __init__(self):
        # create list of block types

        self.texture_manager = texture_manager.Texture_manager(16, 16, 256)
        self.block_types = [None]  # "None" is the block type for air

        self.block_types.append(block_type.Block_type(
            self.texture_manager, "cobblestone", {"all": "cobblestone"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "snow", {"all": "snow"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "grass_block", {"all": "grass"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "dirt", {"all": "dirt"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "stone", {"all": "stone"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "sand", {"all": "sand"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "planks", {"all": "planks"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "red", {"all": "red"}))
        self.block_types.append(block_type.Block_type(
            self.texture_manager, "blue", {"all": "blue"}))

        self.texture_manager.generate_mipmaps()

        # create chunks with very crude terrain generation

        self.chunks = {}

        chunk_count = 9
        voxels = gen(chunk.CHUNK_WIDTH, chunk.CHUNK_LENGTH, chunk.CHUNK_HEIGHT, chunk_count)
        counter = 0

        print("creating world, this may take a while...")
        for x in range(3):
            for z in range(3):
                chunk_position = (x - 4, -1, z - 4)
                current_chunk = chunk.Chunk(self, chunk_position)
                
                for i in range(chunk.CHUNK_WIDTH):
                    for j in range(chunk.CHUNK_HEIGHT):
                        for k in range(chunk.CHUNK_LENGTH):
                            if [i, k, j] in voxels[counter]:
                                if j in range(8, 11): 
                                    current_chunk.blocks[i][j][k] = 2 # snow
                                elif j in range(5, 8): 
                                    current_chunk.blocks[i][j][k] = 6 # sand
                                elif j in range(2, 5): 
                                    current_chunk.blocks[i][j][k] = 3 # grass
                                elif j in range(1, 2): 
                                    current_chunk.blocks[i][j][k] = 4 # dirt
                                else:
                                    current_chunk.blocks[i][j][k] = 5 # sand
                            else:
                                current_chunk.blocks[i][j][k] = 0 # air

                self.chunks[chunk_position] = current_chunk

                # update counter for next part of chunk
                counter += 1

        # update each chunk's mesh
        for chunk_position in self.chunks:
            self.chunks[chunk_position].update_mesh()

        print("rendering...")

    # get the index in the block_types array of the block at a certain position
    def get_block_number(self, position):
        x, y, z = position

        chunk_position = (  # get the chunk in which the the block is's position
            math.floor(x / chunk.CHUNK_WIDTH),
            math.floor(y / chunk.CHUNK_HEIGHT),
            math.floor(z / chunk.CHUNK_LENGTH))

        if not chunk_position in self.chunks:  # return "air" if the chunk doesn't exist
            return 0

        # get the relative position of the block in the chunk

        local_x = int(x % chunk.CHUNK_WIDTH)
        local_y = int(y % chunk.CHUNK_HEIGHT)
        local_z = int(z % chunk.CHUNK_LENGTH)

        # return the block number at the local position in the correct chunk
        return self.chunks[chunk_position].blocks[local_x][local_y][local_z]

    def get_chunk_position(self, position):
        x, y, z = position

        return (
            math.floor(x / chunk.CHUNK_WIDTH),
            math.floor(y / chunk.CHUNK_HEIGHT),
            math.floor(z / chunk.CHUNK_LENGTH))

    def get_local_position(self, position):
        x, y, z = position
        
        return (
            int(x % chunk.CHUNK_WIDTH),
            int(y % chunk.CHUNK_HEIGHT),
            int(z % chunk.CHUNK_LENGTH))

    def get_block_number(self, position):
        x, y, z = position
        chunk_position = self.get_chunk_position(position)

        if not chunk_position in self.chunks:
            return 0
        
        lx, ly, lz = self.get_local_position(position)

        block_number = self.chunks[chunk_position].blocks[lx][ly][lz]
        return block_number

    def set_block(self, position, number):  # set number to 0 (air) to remove block
        x, y, z = position
        chunk_position = self.get_chunk_position(position)

        if not chunk_position in self.chunks:  # if no chunks exist at this position, create a new one
            if number == 0:
                return  # no point in creating a whole new chunk if we're not gonna be adding anything

            self.chunks[chunk_position] = chunk.Chunk(self, chunk_position)

        # no point updating mesh if the block is the same
        if self.get_block_number(position) == number:
            return

        lx, ly, lz = self.get_local_position(position)

        self.chunks[chunk_position].blocks[lx][ly][lz] = number
        self.chunks[chunk_position].modified = True

        self.chunks[chunk_position].update_mesh()

        cx, cy, cz = chunk_position

        def try_update_chunk_at_position(chunk_position, position):
            if chunk_position in self.chunks:
                self.chunks[chunk_position].update_mesh()

        if lx == chunk.CHUNK_WIDTH - 1: 
            try_update_chunk_at_position((cx + 1, cy, cz), (x + 1, y, z))
        if lx == 0: 
            try_update_chunk_at_position((cx - 1, cy, cz), (x - 1, y, z))

        if ly == chunk.CHUNK_HEIGHT - 1: 
            try_update_chunk_at_position((cx, cy + 1, cz), (x, y + 1, z))
        if ly == 0: 
            try_update_chunk_at_position((cx, cy - 1, cz), (x, y - 1, z))

        if lz == chunk.CHUNK_LENGTH - 1: 
            try_update_chunk_at_position((cx, cy, cz + 1), (x, y, z + 1))
        if lz == 0: 
            try_update_chunk_at_position((cx, cy, cz - 1), (x, y, z - 1))

    def draw(self): # draw all the chunks in the world
        for chunk_position in self.chunks:
            self.chunks[chunk_position].draw()