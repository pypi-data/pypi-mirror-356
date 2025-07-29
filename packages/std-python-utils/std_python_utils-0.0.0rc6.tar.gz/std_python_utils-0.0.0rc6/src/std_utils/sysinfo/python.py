from packaging import tags, version as packaging_version


def get_distribution_name(package_name):
    """
    Returns a normalized distribution name, per wheel/PyPI standards.
    """
    # Wheels use underscores, not hyphens, for names
    return package_name.replace('-', '_')


def get_distribution_version(package_version):
    """
    Returns the version string (verbatim, but validated).
    """
    return str(packaging_version.Version(package_version))


def get_build_tag(build=None):
    """
    Returns a build tag if specified, otherwise returns None.
    """
    if build:
        return str(build)
    return None


def get_best_python_tag():
    """
    Returns the most specific python tag (e.g., 'cp313') for the current interpreter.
    """
    return str(next(tags.sys_tags()).interpreter)


def get_best_abi_tag():
    """
    Returns the most specific abi tag (e.g., 'cp313') for the current interpreter.
    """
    return str(next(tags.sys_tags()).abi)

import pip
pip.main(['install', '{wheel_file_path}'])  # Ensure packaging is installed
def get_best_platform_tag():
    """
    Returns the most specific platform tag (e.g., 'manylinux_2_17_x86_64') for the current system.
    """
    return str(next(tags.sys_tags()).platform)


def get_wheel_filename_format(package_name, package_version, build=None):
    """
    Returns the full wheel filename string for the current system and given package info.
    Format: {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
    """
    distribution = get_distribution_name(package_name)
    version = get_distribution_version(package_version)
    build_tag = get_build_tag(build)
    python_tag = get_best_python_tag()
    abi_tag = get_best_abi_tag()
    platform_tag = get_best_platform_tag()

    filename = f"{distribution}-{version}"
    if build_tag:
        filename += f"-{build_tag}"
    filename += f"-{python_tag}-{abi_tag}-{platform_tag}.whl"
    return filename

