cmake_minimum_required(VERSION 3.15)
project(acedrg LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release)
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include/kernel
                    ${CMAKE_CURRENT_SOURCE_DIR}/include/math
                    ${CMAKE_CURRENT_SOURCE_DIR}/include/go
                    ${CMAKE_CURRENT_SOURCE_DIR}/include/forcefield)

set(ACEDRG_TABLES_DIR "tables")

set(SRC

    main.cpp
    
    src/kernel/AllSystem.cpp
    src/kernel/angle.cpp
    src/kernel/atom.cpp
    src/kernel/atomAssembly.cpp
    src/kernel/atomsTree.cpp
    src/kernel/bond.cpp
    src/kernel/CCP4AtomType.cpp
    src/kernel/chain.cpp
    src/kernel/checkEnvAndGetMode.cpp
    src/kernel/chemPropSet.cpp
    src/kernel/chiral.cpp
    src/kernel/codBondAndAngleGroups.cpp
    src/kernel/codClassify.cpp
    src/kernel/coordPolyhedra.cpp
    src/kernel/crystInfo.cpp
    src/kernel/DictCifFILE.cpp
    src/kernel/DnaRna.cpp
    src/kernel/ExtraRestrDictFile.cpp
    src/kernel/file.cpp
    src/kernel/getExtraRestrs.cpp
    src/kernel/inputParams.cpp
    src/kernel/libgcrystInfo.cpp
    src/kernel/libglink.cpp
    src/kernel/libgmodel.cpp
    src/kernel/molecule.cpp
    src/kernel/MolGenerator.cpp
    src/kernel/MolSdfFile.cpp
    src/kernel/MonomerLib.cpp
    src/kernel/neighbList.cpp
    src/kernel/PDBFile.cpp
    src/kernel/periodicTable.cpp
    src/kernel/plane.cpp
    src/kernel/residue.cpp
    src/kernel/restraintList.cpp
    src/kernel/ring.cpp
    src/kernel/secondaryStructures.cpp
    src/kernel/SmileTool.cpp
    src/kernel/ssbond.cpp
    src/kernel/torsion.cpp
    src/kernel/TransCoord.cpp
    src/kernel/utility.cpp

    src/go/GlobOpt.cpp
    src/go/LinAlg.cpp

    src/forcefield/getDerivs.cpp
    src/forcefield/getObjValue.cpp
)

if (MSVC)
    set(SRC ${SRC} src/kernel/win32/getopt.c)
endif (MSVC)

add_executable(libmol ${SRC})

if(DEFINED SKBUILD_DATA_DIR)
    set(_acedrg_libexec "${SKBUILD_DATA_DIR}/libexec")
    set(_acedrg_share   "${SKBUILD_DATA_DIR}/share/acedrg")
else()
    set(_acedrg_libexec "libexec")
    set(_acedrg_share   "share/acedrg")
endif()

install(TARGETS libmol RUNTIME DESTINATION "${_acedrg_libexec}")
install(DIRECTORY "${ACEDRG_TABLES_DIR}/" DESTINATION "${_acedrg_share}/tables")
install(DIRECTORY utils DESTINATION "${_acedrg_share}")
