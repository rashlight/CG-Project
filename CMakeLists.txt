project(CGProject)

set(CMAKE_CXX_STANDARD 11)
cmake_minimum_required(VERSION 3.4)

# New and shiny opengl
cmake_policy(SET CMP0072 NEW)

# Import modules
set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/modules/" ${CMAKE_MODULE_PATH})

# Add module path in case this is project root
if(PROJECT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/../../modules/" ${CMAKE_MODULE_PATH})
endif()

# Find components on your system
find_package(GLFW REQUIRED)

find_package(Corrade REQUIRED Main)
find_package(Magnum REQUIRED
    GL
    MeshTools
    Primitives
    Shaders
    Trade
    Sdl2Application)

if(CORRADE_TARGET_APPLE)
    find_package(Magnum REQUIRED CglContext)
elseif(CORRADE_TARGET_UNIX)
    find_package(Magnum REQUIRED GlxContext)
elseif(CORRADE_TARGET_WINDOWS)
    find_package(Magnum REQUIRED WglContext)
else()
    message(FATAL_ERROR "No context handler available on this platform")
endif()

# Pedantic
set_directory_properties(PROPERTIES CORRADE_USE_PEDANTIC_FLAGS ON)

# Source add
aux_source_directory(src/ SRC_LIST)
add_executable(CGProject ${SRC_LIST})

# Magnum Corvus
# Add libraries here
target_link_libraries(CGProject PRIVATE
    GLFW::GLFW
    Corrade::Main
    Magnum::Application
    Magnum::GL
    Magnum::GLContext
    Magnum::Magnum
    Magnum::MeshTools
    Magnum::Primitives
    Magnum::Shaders
    Magnum::Trade)

# Make the executable a default target to build & run in Visual Studio
set_property(DIRECTORY ${PROJECT_SOURCE_DIR} PROPERTY VS_STARTUP_PROJECT CGProject)