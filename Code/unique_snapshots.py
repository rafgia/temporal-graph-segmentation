from load import load_graph
import matplotlib.pyplot as plt

def compression_on_snapshots(new_temporal_dict):
    compressed_temporal_dict = {}
    for i in range(len(new_temporal_dict)):
        if len(compressed_temporal_dict)<1:
            compressed_temporal_dict[i] = new_temporal_dict[i]
            continue
        if sorted(new_temporal_dict[i]) != sorted(new_temporal_dict[i-1]):
            compressed_temporal_dict[i] = new_temporal_dict[i]
    compressed_value =  (len(compressed_temporal_dict))/(len(new_temporal_dict))
    return compressed_temporal_dict, compressed_value

def compression_neighborhoods_per_node(temporal_dict):
    node_neighborhood_freq = {}
    for snapshot, edges in temporal_dict.items():
        for edge in edges:
            for node in edge:
                node_neighborhood = set()
                for other_edge in edges:
                    if other_edge != edge:
                        for other_node in other_edge:
                            if other_node != node:
                                node_neighborhood.add(other_node)
                node_neighborhood = frozenset(node_neighborhood)
                if node in node_neighborhood_freq:
                    if node_neighborhood in node_neighborhood_freq[node]:
                        node_neighborhood_freq[node][node_neighborhood] += 1
                    else:
                        node_neighborhood_freq[node][node_neighborhood] = 1
                else:
                    node_neighborhood_freq[node] = {node_neighborhood: 1}
    node_compression = {}
    for node, neighborhoods in node_neighborhood_freq.items():
        count = 0
        for neighborhood, freq in neighborhoods.items():
            count += freq 
        node_compression[node] = count/len(temporal_dict)
    return node_compression

def plot_histogram(data_dict):
    keys = list(data_dict.keys())
    values = list(data_dict.values())

    plt.bar(keys, values)
    plt.xlabel('Node')
    plt.ylabel('Compression_ratio')
    plt.title('Compression per nodes')
    plt.show()

# Function to convert dictionary to CSV
def dict_to_csv(data, filename):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Node 1', 'Node 2', 'Time'])
        for time, edges in data.items():
            for edge in edges:
                csvwriter.writerow([edge[0], edge[1], time])


nodes,node2id,timestamps,timestamp2id,edges,edge2id,timestamp2edges,snapshots,temporal_dict, new_temporal_dict = load_graph("graph_path.txt/csv", True,',')
#compressed_temporal_dict, compressed_value = compression_on_snapshots(new_temporal_dict)
#node_compression = compression_on_nodes(new_temporal_dict)
#print ("Compression ratio: ",compressed_value)
#histogram_nodes_occurrence(node_compression)

#count = 0
#for key, value in node_compression.items():
#    if value > 1:
#        count += 1
#print ("Number of nodes: ", len(nodes), "Number of repeated nodes: ", count)
#print (node_compression)
#dict_to_csv(new_temporal_dict,'workplace_reduced.csv')
data = compression_neighborhoods_per_node(new_temporal_dict)
plot_histogram(data)