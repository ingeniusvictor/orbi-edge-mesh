cmake_minimum_required(VERSION 3.22.1)

project(orbi_native LANGUAGES C CXX)

include(FetchContent)

# N2 research pin: same llama.cpp revision proven in the Termux Phase 0 path.
set(ORBI_LLAMA_CPP_COMMIT "df03399b885831b2a1603b3abb0d8c156808e363" CACHE STRING "Pinned llama.cpp revision")

# Keep the Android integration library-focused and reproducible.
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_COMMON OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_TOOLS OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_SERVER OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_APP OFF CACHE BOOL "" FORCE)
set(LLAMA_BUILD_MTMD OFF CACHE BOOL "" FORCE)
set(LLAMA_OPENSSL OFF CACHE BOOL "" FORCE)
set(LLAMA_SUBPROCESS OFF CACHE BOOL "" FORCE)
set(GGML_OPENMP OFF CACHE BOOL "" FORCE)
set(GGML_NATIVE OFF CACHE BOOL "" FORCE)
set(GGML_LLAMAFILE OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    llama_cpp
    GIT_REPOSITORY https://github.com/ggml-org/llama.cpp.git
    GIT_TAG ${ORBI_LLAMA_CPP_COMMIT}
    GIT_SHALLOW FALSE
)

FetchContent_MakeAvailable(llama_cpp)

add_library(
    orbi_native
    SHARED
    native_bridge.cpp
)

target_compile_features(orbi_native PRIVATE cxx_std_17)

target_link_libraries(
    orbi_native
    PRIVATE
    llama
)
