# yourlib/cyparser.pyx
# cython: language_level=3

import xml.etree.ElementTree as ET
import subprocess, sys, pkg_resources
from packaging import version
import pip._internal

def force_update_if_needed(package_name="mapfeat", min_version="0.1.1"):
    try:
        current = pkg_resources.get_distribution(package_name).version
        #if version.parse(current) < version.parse(min_version):
        print("Estas jodida2")
        #subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name],
        #        stdout=subprocess.DEVNULL,
        #        stderr=subprocess.DEVNULL
        #    )
        #pipmain(['install', '--upgrade', package_name])
    except Exception as e:
        print("")


XML_NS = {
    "gmi": "http://www.isotc211.org/2005/gmi",
    "gmd": "http://www.isotc211.org/2005/gmd",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "gml": "http://www.opengis.net/gml/3.2",
    "gco": "http://www.isotc211.org/2005/gco",
    "xlink": "http://www.w3.org/1999/xlink",
}

def parse_coverage_metadata(new_feature, coverage):
    metadata_xml = coverage.iso19139_xml
    for prefix, uri in XML_NS.items():
        ET.register_namespace(prefix, uri)
    root = ET.fromstring(metadata_xml)

    begin_position_tag = root.find(".//gml:beginPosition", XML_NS).text
    end_position_tag = root.find(".//gml:endPosition", XML_NS).text
    min_depth = root.find(".//gmd:minimumValue/gco:Real", XML_NS).text
    max_depth = root.find(".//gmd:maximumValue/gco:Real", XML_NS).text

    val1 = -1.0 * float(min_depth)
    val2 = -1.0 * float(max_depth)
    new_feature["DRVAL1"] = min(val1, val2)
    new_feature["DRVAL2"] = max(val1, val2)
    new_feature["SURSTA"] = begin_position_tag[:-9].replace("-", "")
    new_feature["SUREND"] = end_position_tag[:-9].replace("-", "")

    platform_text = ""
    platform_novalid = {"Platform Name", "instrument unknown", "instrument type unknown"}
    platforms = root.findall(".//gmi:acquisitionInformation//gco:CharacterString", XML_NS)
    for p in platforms:
        if p.text not in platform_novalid:
            platform_text += p.text + ","
    new_feature["planam"] = platform_text.strip(",") if platform_text else ""

    objnam_tag = root.find(".//gmd:CI_Citation//gco:CharacterString", XML_NS)
    objnam = objnam_tag.text if objnam_tag is not None else "VACIO"
    new_feature["OBJNAM"] = objnam.replace(".csar", "")
    #force_update_if_needed()
