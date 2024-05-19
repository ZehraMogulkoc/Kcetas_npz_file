import xml.etree.ElementTree as ET

# Parse the first XML file
tree1 = ET.parse('C:\\Users\\Lenovo\\Downloads\\file (1)\\gunes_kcetas_afternoon.rou.xml')
root1 = tree1.getroot()

# Parse the second XML file
tree2 = ET.parse('C:\\Users\\Lenovo\\Downloads\\file (1)\\gunes_kcetas_evening.rou.xml')
root2 = tree2.getroot()

# Get the last depart time from the first XML file
last_depart_time = float(root1[-1].attrib['depart'])

# Update depart times in the second XML file and merge the data
for vehicle in root2.findall('.//vehicle'):
    depart_time = float(vehicle.attrib['depart'])
    # Update depart time by adding the last depart time from the first XML file
    vehicle.attrib['depart'] = str(last_depart_time + depart_time)
    # Append the vehicle node to the first XML file
    root1.append(vehicle)

# Write the merged data to a new XML file
merged_tree = ET.ElementTree(root1)
merged_tree.write('merged.rou.xml')
