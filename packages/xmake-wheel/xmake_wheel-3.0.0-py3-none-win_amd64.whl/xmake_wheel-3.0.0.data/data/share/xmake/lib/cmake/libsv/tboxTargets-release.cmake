#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "libsv::tbox" for configuration "Release"
set_property(TARGET libsv::tbox APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(libsv::tbox PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "ASM_NASM;C"
  # IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/tbox.lib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/tbox.lib"
  )

list(APPEND _IMPORT_CHECK_TARGETS libsv::tbox )
list(APPEND _IMPORT_CHECK_FILES_FOR_libsv::tbox "${_IMPORT_PREFIX}/lib/tbox.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
