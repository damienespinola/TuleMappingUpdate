#
# This program is part of the 2021 Tule Mapping Update Project. It takes a .kml file (only Addresses2.kml right now) of
# address points made using Google Earth Pro and adds address schema structure to the file as well as address attribute
# data for all addresses. Attribute data is based off the placemark's name. This processing is necessary to upload
# address data to Google Maps using Google's Geo Data Upload tool. Documentation on the tool and the needed structure
# can be found here (https://support.google.com/mapcontentpartners/answer/144284?hl=en&ref_topic=22146) and
# here (https://developers.google.com/kml/documentation/extendeddata?csw=1)
#
# Special thanks to everyone at the Tule River Structural Fire Branch, especially Aaron Franco for his blessings,
# Mike Vasquez knocking out the data in two days, and Alexis Lozano and Kidd Valdez for getting me to get
# frappuccinos that one morning.
#
# Author(s): Damien Espinola (damien.espinola@gmail.com)
#
# Date Created: August 24, 2021
# Last Modified: September 19, 2021
#
# TODO:
# Should be able to pick a file other than Addresses2
# Really should come up with a more manageable method of supporting future addresses
#

import xml.etree.ElementTree as ET
import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    NorthRezRegex = re.compile('^n', re.IGNORECASE)
    SouthRezRegex = re.compile('^s', re.IGNORECASE)
    ChimneyRegex = re.compile('^chimney', re.IGNORECASE)
    CowMtRegex = re.compile('^cow', re.IGNORECASE)

    tree = ET.parse('Addresses2.kml')

    root = tree.getroot()

    GMAddressSchema = ET.SubElement(root[0], 'Schema')  # Schema elements are always a child of <Document>
    GMAddressSchema.attrib["name"] = 'ResidentialAddress'
    GMAddressSchema.attrib["id"] = 'ResidentialAddressId'

    GMASnumber = ET.SubElement(GMAddressSchema, 'SimpleField')
    GMASnumber.attrib["type"] = 'string'
    GMASnumber.attrib["name"] = 'ST_NUM'

    GMASname = ET.SubElement(GMAddressSchema, 'SimpleField')
    GMASname.attrib["type"] = 'string'
    GMASname.attrib["name"] = 'ST_NAME'

    GMAScity = ET.SubElement(GMAddressSchema, 'SimpleField')
    GMAScity.attrib["type"] = 'string'
    GMAScity.attrib["name"] = 'CITY'

    GMASstate = ET.SubElement(GMAddressSchema, 'SimpleField')
    GMASstate.attrib["type"] = 'string'
    GMASstate.attrib["name"] = 'STATE'

    GMASzip = ET.SubElement(GMAddressSchema, 'SimpleField')
    GMASzip.attrib["type"] = 'string'
    GMASzip.attrib["name"] = 'ZIP'

    addressName = ""
    addressSplit = []

    # for elem in root:
    #   for subelm in elem:
    #      print(subelm)
    # print(root[0][0])
    # print(root[0][1])
    # print(root[0].find('{http://www.opengis.net/kml/2.2}name'))
    someFolder = root[0].find('{http://www.opengis.net/kml/2.2}Folder')

    # for elem in someFolder:
    #   print(elem)

    # print(someFolder[0].tag)
    # print(someFolder[0].attrib)
    # print(someFolder[0].text)

    placemarks = someFolder.findall('{http://www.opengis.net/kml/2.2}Placemark')

    for address in placemarks:
        # print(address.find('{http://www.opengis.net/kml/2.2}name').text)
        addressName = address.find('{http://www.opengis.net/kml/2.2}name').text
        addressSplit = addressName.split()
        # print(addressSplit[1])
        addressStreetName = ''

        if NorthRezRegex.match(addressSplit[1]):
            addressStreetName = "North Reservation Road"
        elif SouthRezRegex.match(addressSplit[1]):
            addressStreetName = "South Reservation Road"
        elif CowMtRegex.match(addressSplit[1]):
            addressStreetName = "Cow Mountain Road"
        elif ChimneyRegex.match(addressSplit[1]):
            addressStreetName = "Chimney Road"
        else:
            raise ValueError("This address: " + addressName + " matches nothing.")

        addrAttributes = ET.SubElement(address, 'ExtendedData')

        addrSchema = ET.SubElement(addrAttributes, 'SchemaData')
        addrSchema.attrib["schemaUrl"] = '#ResidentialAddressId'

        addrStreetNum = ET.SubElement(addrSchema, 'SimpleData')
        addrStreetNum.attrib["name"] = 'ST_NUM'
        addrStreetNum.text = addressSplit[0]

        addrStreetName = ET.SubElement(addrSchema, 'SimpleData')
        addrStreetName.attrib["name"] = 'ST_NAME'
        addrStreetName.text = addressStreetName

        addrCity = ET.SubElement(addrSchema, 'SimpleData')
        addrCity.attrib["name"] = 'CITY'
        addrCity.text = 'Porterville'

        addrState = ET.SubElement(addrSchema, 'SimpleData')
        addrState.attrib["name"] = 'STATE'
        addrState.text = 'CA'

        addrZip = ET.SubElement(addrSchema, 'SimpleData')
        addrZip.attrib["name"] = 'ZIP'
        addrZip.text = '93257'

    ET.indent(tree, space="\t", level=0)  # without this the added xml elements show up on a single line. Looks ugly
    #print(ET.tostring(root, encoding='utf8').decode('utf8'))
    tree.write('Addresses2wAttributes.kml', encoding="utf-8")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
