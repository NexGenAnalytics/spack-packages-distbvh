# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Distbvh(CMakePackage):
    """distBVH is a library for asynchronous parallel distributed collision
    detection. It provides data structures and parallel algorithms for use in
    solid mechanics applications that require proximity search."""

    homepage = "https://github.com/sandialabs/distBVH"
    git = "https://github.com/sandialabs/distBVH.git"

    maintainers("nmm0")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("testing", commit="171ccb0e3e7f48ceec98dc3f268f9e8498686e7e")

    # Build variants
    variant("single_precision", default=False, description="Build DistBVH with single precision")
    variant("vtk", default=False, description="Enable VTK support for visualization")
    variant("tracing", default=False, description="Enable detailed performance tracing")
    variant("6dop", default=False, description="Enable 6-DOPs for broadphase")
    variant(
        "lazy_narrowphase",
        default=True,
        description="Use lazy initialization for narrowphase (recommended)",
    )

    # CMake build dependency
    depends_on("cmake@3.15:", type="build")

    # Required dependencies
    depends_on("kokkos@4.4:")
    depends_on("darma-vt+kokkos")
    depends_on("spdlog@1.13:")

    # Optional dependencies
    depends_on("vtk", when="+vtk")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("BVH_ENABLE_TRACING", "tracing"),
            self.define_from_variant("BVH_BROADPHASE_6_DOP", "6dop"),
            self.define_from_variant("BVH_SINGLE_PRECISION", "single_precision"),
            self.define("BVH_DISABLE_TESTS", True),
        ]

        # Handle lazy narrowphase variant (inverted logic)
        if self.spec.satisfies("+lazy_narrowphase"):
            args.append(self.define("BVH_COPY_ALL_NARROWPHASE_PATCHES", False))
        else:
            args.append(self.define("BVH_COPY_ALL_NARROWPHASE_PATCHES", True))

        return args
