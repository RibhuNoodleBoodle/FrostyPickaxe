# rise360 - ReXGlue Recompiled Project
#
# SDK boilerplate lives in cmake/rexglue.cmake.

cmake_minimum_required(VERSION 3.25)
project(rise360 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(cmake/rexglue.cmake)

# Sources
set(RISE360_SOURCES
    src/main.cpp
)

if(WIN32)
    add_executable(rise360 WIN32 ${RISE360_SOURCES})
else()
    add_executable(rise360 ${RISE360_SOURCES})
endif()

rexglue_setup_target(rise360 GPU_PLUGINS xenos)
