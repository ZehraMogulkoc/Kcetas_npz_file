import traci
import sumolib
import csv  # Import the csv module
import xml.etree.ElementTree as ET

sumo_binary = "C:\\Program Files (x86)\\Sumo\\bin\\sumo.exe"
sumo_config = "D:\\ASTGCN-master\\data\\gunes_kcetas\\gunes_kcetas\\gunes_kcetas_morning.sumocfg"
net_file = "D:\\ASTGCN-master\\data\\gunes_kcetas\\gunes_kcetas\\gunes_kcetas.net.xml"

csv_file = "morninggg.csv"  # Specify the CSV file pathh

counted_vehicle_ids = {}

tree = ET.parse(net_file)
root = tree.getroot()

def getAllEdge(net_root):
    edges = {}
    for childElement in net_root:
        if childElement.tag == "edge":
            edge_id = childElement.get("id")
            edges[edge_id] = childElement
    return edges

def count_cars_on_edge(edge_id):
    if edge_id not in counted_vehicle_ids:
        counted_vehicle_ids[edge_id] = set()

    vehicle_count = 0
    for vehicle_id in traci.edge.getLastStepVehicleIDs(edge_id):
        if vehicle_id not in counted_vehicle_ids[edge_id]:
            counted_vehicle_ids[edge_id].add(vehicle_id)
            vehicle_count += 1
    return vehicle_count

def get_edge_ids(net_file):
    net = sumolib.net.readNet(net_file)
    edge_ids = [edge.getID() for edge in net.getEdges()]
    return edge_ids

def get_junction_ids():
    return traci.junction.getIDList()

def main():
    sumo_cmd = [sumo_binary, "-c", sumo_config, "--net-file", net_file]
    traci.start(sumo_cmd)
    edge_ids = get_edge_ids(net_file)
    junction_ids = get_junction_ids()
    interval_duration = 300
    interval_start_time = 0
    edges=getAllEdge(root)
    filtered_junction_ids = [junction_id for junction_id in junction_ids if not (junction_id.startswith("gneJ") or len(junction_id) > 5)]
    # Open the CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the header row
        csv_writer.writerow(["timestep", "location", "flow", "occupy", "speed"])

        try:
            while traci.simulation.getMinExpectedNumber() > 0:
                car_counts = {edge_id: 0 for edge_id in edge_ids}

                current_time = traci.simulation.getTime()
                 # Add this condition to stop at step 3600
                if current_time > 694800:
                    break
                while (current_time - interval_start_time) <= interval_duration:
                    current_time = traci.simulation.getTime()
                    # Calculate car count for all edges within the current interval
                    for edge_id in edge_ids:
                        car_count = count_cars_on_edge(edge_id)
                        car_counts[edge_id] += car_count
                    traci.simulationStep()
                interval_start_time = current_time  # Update the interval start time

                # Write the data to the CSV file
                for junction_id in filtered_junction_ids :
                    sum=0
                    list=[]
                    index = junction_ids.index(junction_id)
                    for edge_id, count in car_counts.items():
                        edge_element = edges[edge_id]
                        to_node = edge_element.get("to") 
                        if to_node == junction_id:
                            sum+=count
                            list.append(edge_id)
                    csv_writer.writerow([int(current_time), junction_ids.index(junction_id), sum, 1, 1])
                    print(f"Time: {int(current_time)}, Index: {index}, Junction ID: {junction_id}, Count: {sum},Edges: {list}")


        except KeyboardInterrupt:
            pass

    traci.close()

if __name__ == "__main__":
    main()


