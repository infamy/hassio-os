import os
import platform
from doit.tools import Interactive

DOIT_CONFIG = {
    'backend': 'json',
    'dep_file': '.doit.json',
}

def _isdocker():
    return os.path.isfile('/.dockerenv')


def _islinux():
    return platform.system() == 'Linux'


def task_build_ova():
    """Build an HASSOS targetting an OVA file"""
    if _isdocker():
        return {
            'actions': ['make -C /build/buildroot BR2_EXTERNAL=/build/buildroot-external ova_defconfig',
                        'make -C /build/buildroot BR2_EXTERNAL=/build/buildroot-external'],
            'verbosity': 2, 
        } 
    return {'actions':['echo "Must run in docker"'],'verbosity': 2}


def task_docker_rebuild():
    """Rebuild the docker container, maybe needed at times"""
    if _isdocker():
        return {'actions':['echo "In docker container skipping..."'],'verbosity': 2}
    return {
        'actions': ['docker build --no-cache -t hassbuildroot .'],
        'verbosity': 2,
    }


def task_docker_enter():
    """Enter the build docker container"""
    if _isdocker():
        return {'actions':['echo "In docker container skipping..."'],'verbosity': 2}
    if _islinux():
        return {
            'actions': ['modprobe overlayfs',
                        'docker build -t hassbuildroot .', 
                        Interactive('docker run -it --rm --privileged -v "$(pwd):/build" hassbuildroot bash')],
            'verbosity': 2,
        }
    return {
        'actions': ['docker build -t hassbuildroot .', 
                    Interactive('docker run -it --rm --privileged -v "$(pwd):/build" hassbuildroot bash')],
        'verbosity': 2,
    }


def task_build_clean():
    """Do a buildroot clean"""
    if _isdocker():
        return {
            'actions': ['make -C /build/buildroot BR2_EXTERNAL=/build/buildroot-external clean'],
            'verbosity': 2,
        }
    return {'actions':['echo "Must run in docker"'],'verbosity': 2}