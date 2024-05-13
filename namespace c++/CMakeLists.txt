cmake_minimum_required(VERSION 3.29)
project(namespace_c++)

set(CMAKE_CXX_STANDARD 17)

# Discord RPC
include_directories(discord-rpc/include)
link_directories(discord-rpc/lib)

# cpprestsdk
set(cpprestsdk_DIR "C:/Users/SystemX/vcpkg/packages/cpprestsdk_x64-windows/share/cpprestsdk")
set(cpprestsdk_INCLUDE_DIR "C:/Users/SystemX/vcpkg/packages/cpprestsdk_x64-windows/include")
include_directories(${cpprestsdk_INCLUDE_DIR})
set(ZLIB_ROOT "C:/Users/SystemX/vcpkg/packages/zlib_x64-windows")
set(unofficial-brotli_DIR "C:/Users/SystemX/vcpkg/packages/brotli_x64-windows/share/unofficial-brotli")

find_package(cpprestsdk REQUIRED)
find_package(ZLIB REQUIRED)
find_package(unofficial-brotli REQUIRED)

# Boost
set(BOOST_ROOT "C:/Users/SystemX/vcpkg/installed/x64-windows")
set(Boost_INCLUDE_DIR "${BOOST_ROOT}/include")
set(Boost_LIBRARY_DIR "${BOOST_ROOT}/lib")
set(BOOST_INCLUDEDIR "${Boost_INCLUDE_DIR}")
set(BOOST_LIBRARYDIR "${Boost_LIBRARY_DIR}")
find_package(Boost 1.71.0 COMPONENTS system date_time regex thread REQUIRED)
include_directories(${Boost_INCLUDE_DIR})

# Discord RPC library
set(DISCORD_RPC_LIB "C:/Users/SystemX/discord-rpc/lib/discord-rpc.lib") # Измените на полный путь, если необходимо

add_executable(namespace_c++ main.cpp)

target_link_libraries(namespace_c++ PRIVATE ${cpprestsdk_DIR})
target_link_libraries(namespace_c++ PRIVATE ${cpprestsdk_INCLUDE_DIR})
target_link_libraries(namespace_c++ PRIVATE ${DISCORD_RPC_LIB})
target_link_libraries(namespace_c++ PRIVATE ZLIB::ZLIB)
target_link_libraries(namespace_c++ PRIVATE ${unofficial-brotli_DIR})
target_link_libraries(namespace_c++ PRIVATE Boost::system Boost::date_time Boost::regex Boost::thread)
