#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ezc3d" for configuration "Release"
set_property(TARGET ezc3d APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ezc3d PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/ezc3d/libezc3d.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libezc3d.dylib"
  )

list(APPEND _cmake_import_check_targets ezc3d )
list(APPEND _cmake_import_check_files_for_ezc3d "${_IMPORT_PREFIX}/ezc3d/libezc3d.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
