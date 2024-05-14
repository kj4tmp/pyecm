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


add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/ext/SOEM) # soem is installed as a submodule

# We are now ready to compile the actual extension module
nanobind_add_module(
  # Name of the extension
  soem_ext

  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Build libnanobind statically and merge it into the
  # extension (which itself remains a shared library)
  #
  # If your project builds multiple extensions, you can
  # replace this flag by NB_SHARED to conserve space by
  # reusing a shared libnanobind across libraries
  NB_STATIC

  # Source code goes here
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

set(MY_SOEM_EXT_TARGET_DIR $<TARGET_FILE_DIR:soem_ext>)
cmake_path(NATIVE_PATH MY_SOEM_EXT_TARGET_DIR NATIVE_PYTHON_PATH)
message(STATUS "NATIVE_PYTHON_PATH: ${NATIVE_PYTHON_PATH}")

function (my_nanobind_add_stub name)
  cmake_parse_arguments(PARSE_ARGV 1 ARG "VERBOSE;INCLUDE_PRIVATE;EXCLUDE_DOCSTRINGS;INSTALL_TIME;EXCLUDE_FROM_ALL" "MODULE;OUTPUT;MARKER_FILE;COMPONENT;PATTERN_FILE" "PYTHON_PATH;DEPENDS")

  if (EXISTS ${CMAKE_SOURCE_DIR}/stubgen.py)
    set(NB_STUBGEN "${CMAKE_SOURCE_DIR}/stubgen.py")
  else()
    message(FATAL_ERROR "nanobind_add_stub(): could not locate 'stubgen.py'!")
  endif()

  if (NOT ARG_VERBOSE)
    list(APPEND NB_STUBGEN_ARGS -q)
  else()
    set(NB_STUBGEN_EXTRA USES_TERMINAL)
  endif()

  if (ARG_INCLUDE_PRIVATE)
    list(APPEND NB_STUBGEN_ARGS -P)
  endif()

  if (ARG_EXCLUDE_DOCSTRINGS)
    list(APPEND NB_STUBGEN_ARGS -D)
  endif()

  foreach (TMP IN LISTS ARG_PYTHON_PATH)
    list(APPEND NB_STUBGEN_ARGS -i "${TMP}")
  endforeach()

  if (ARG_PATTERN_FILE)
    list(APPEND NB_STUBGEN_ARGS -p "${ARG_PATTERN_FILE}")
  endif()

  if (ARG_MARKER_FILE)
    list(APPEND NB_STUBGEN_ARGS -M "${ARG_MARKER_FILE}")
    list(APPEND NB_STUBGEN_OUTPUTS "${ARG_MARKER_FILE}")
  endif()

  if (NOT ARG_MODULE)
    message(FATAL_ERROR "nanobind_add_stub(): a 'MODULE' argument must be specified!")
  else()
    list(APPEND NB_STUBGEN_ARGS -m "${ARG_MODULE}")
  endif()

  if (NOT ARG_OUTPUT)
    message(FATAL_ERROR "nanobind_add_stub(): an 'OUTPUT' argument must be specified!")
  else()
    list(APPEND NB_STUBGEN_ARGS -o "${ARG_OUTPUT}")
    list(APPEND NB_STUBGEN_OUTPUTS "${ARG_OUTPUT}")
  endif()

  set(NB_STUBGEN_CMD "${Python_EXECUTABLE}" "${NB_STUBGEN}" ${NB_STUBGEN_ARGS})

  if (NOT ARG_INSTALL_TIME)
    add_custom_command(
      OUTPUT ${NB_STUBGEN_OUTPUTS}
      COMMAND ${NB_STUBGEN_CMD}
      WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
      DEPENDS ${ARG_DEPENDS} "${NB_STUBGEN}" "${ARG_PATTERN_FILE}"
      ${NB_STUBGEN_EXTRA}
    )
    add_custom_target(${name} ALL DEPENDS ${NB_STUBGEN_OUTPUTS})
  else()
    set(NB_STUBGEN_EXTRA "")
    if (ARG_COMPONENT)
      list(APPEND NB_STUBGEN_EXTRA COMPONENT ${ARG_COMPONENT})
    endif()
    if (ARG_EXCLUDE_FROM_ALL)
      list(APPEND NB_STUBGEN_EXTRA EXCLUDE_FROM_ALL)
    endif()
    # \${CMAKE_INSTALL_PREFIX} has same effect as $<INSTALL_PREFIX>
    # This is for compatibility with CMake < 3.27.
    # For more info: https://github.com/wjakob/nanobind/issues/420#issuecomment-1971353531
    install(CODE "set(CMD \"${NB_STUBGEN_CMD}\")\nexecute_process(\n COMMAND \$\{CMD\}\n WORKING_DIRECTORY \"\${CMAKE_INSTALL_PREFIX}\"\n)" ${NB_STUBGEN_EXTRA})
  endif()
endfunction()

my_nanobind_add_stub(
  soem_ext_stub
  MODULE soem_ext
  OUTPUT "${CMAKE_SOURCE_DIR}/pyecm/soem/soem_ext.pyi"
  PYTHON_PATH $<SHELL_PATH:$<TARGET_FILE_DIR:soem_ext>>
  DEPENDS soem_ext
  MARKER_FILE py.typed
  VERBOSE
)
# Install directive for scikit-build-core

# debug stub gen
add_custom_command(TARGET soem_ext_stub
    PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E echo "TARGET_FILE_DIR for soem_ext: $<SHELL_PATH:$<TARGET_FILE_DIR:soem_ext>>"
)

install(TARGETS soem_ext LIBRARY DESTINATION "pyecm/soem")
install(FILES "${CMAKE_SOURCE_DIR}/pyecm/soem/soem_ext.pyi" DESTINATION "pyecm/soem")
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/py.typed" DESTINATION "pyecm/soem")

