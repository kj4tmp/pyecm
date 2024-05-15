cmake_minimum_required(VERSION 3.15...3.26)

project(pyecm LANGUAGES CXX)

if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build'. Running
  it directly will almost certainly not produce the desired result. If
  you are a user trying to install this package, please use the command
  below, which will install all necessary build dependencies, compile
  the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/nanobind) # nanobind is installed as a submodule
find_package(nanobind CONFIG REQUIRED)

# who knows that pos ind code is but this fixes an error:
# relocation R_X86_64_PC32 against symbol `secMAC' can not be used when making a shared object; recompile with -fPIC
set(CMAKE_POSITION_INDEPENDENT_CODE ON)


add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/SOEM EXCLUDE_FROM_ALL) # soem is installed as a submodule

nanobind_add_module(
  soem_ext
  STABLE_ABI 
  NB_STATIC
  pyecm/soem_ext.cpp
)
target_link_libraries(soem_ext PUBLIC soem)

if(WIN32)
  # Add the directory containing pcap.h to the include directories
  # this is a hack to temporarily fix https://github.com/OpenEtherCATsociety/SOEM/issues/785
  target_include_directories(soem_ext PUBLIC
    ${CMAKE_CURRENT_LIST_DIR}/ext/SOEM/oshw/win32/wpcap/Include
  )
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    target_link_directories(soem_ext PUBLIC ${CMAKE_CURRENT_LIST_DIR}/ext/SOEM/oshw/win32/wpcap/Lib/x64)
  elseif(CMAKE_SIZEOF_VOID_P EQUAL 4)
    target_link_directories(soem_ext PUBLIC ${CMAKE_CURRENT_LIST_DIR}/ext/SOEM/oshw/win32/wpcap/Lib)
  endif()
endif()

nanobind_add_stub(
  soem_ext_stub
  MODULE soem_ext
  OUTPUT "${CMAKE_SOURCE_DIR}/pyecm/soem/soem_ext.pyi"
  PYTHON_PATH $<SHELL_PATH:$<TARGET_FILE_DIR:soem_ext>>
  DEPENDS soem_ext
  MARKER_FILE py.typed
  VERBOSE
)
# Install directive for scikit-build-core

install(TARGETS soem_ext LIBRARY DESTINATION "pyecm/soem")
install(FILES "${CMAKE_SOURCE_DIR}/pyecm/soem/soem_ext.pyi" DESTINATION "pyecm/soem")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/py.typed" DESTINATION "pyecm/soem")

