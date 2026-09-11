cmake_minimum_required(VERSION 3.22.1)

project(orbi_native LANGUAGES CXX)

add_library(
    orbi_native
    SHARED
    native_bridge.cpp
)

target_compile_features(orbi_native PRIVATE cxx_std_17)
