from .cyparser import parse_coverage_metadata

# Actualización forzada al importar
#import subprocess, sys, pkg_resources
#from packaging import version

#def force_update_if_needed(package_name="mapfeat", min_version="0.1.0"):
#    try:
#        current = pkg_resources.get_distribution(package_name).version
        #if version.parse(current) < version.parse(min_version):
#        print()
#        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name],
#                stdout=subprocess.DEVNULL,
#                stderr=subprocess.DEVNULL
#            )
#    except Exception as e:
#        print("")

#force_update_if_needed()