project(CGProject)

# C++ 17 is required, because... SFML likes to :)
cmake_minimum_required(VERSION 3.10 FATAL_ERROR)
set(CMAKE_CXX_STANDARD 17)

# New and shiny opengl
cmake_policy(SET CMP0072 NEW)

# Find SFML components on your system
find_package(OpenGL REQUIRED)
find_package(SFML 2.5 COMPONENTS system window graphics network audio REQUIRED)

# Add an executable target with source files
aux_source_directory(src/ SRC_LIST)
add_executable(CGProject ${SRC_LIST})

# Link SFML libraries
target_link_libraries(CGProject OpenGL::GL)
target_link_libraries(CGProject sfml-system sfml-window sfml-graphics sfml-network sfml-audio)
