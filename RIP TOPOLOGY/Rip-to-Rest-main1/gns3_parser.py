import json

def parse_gns3_routers(gns3_file_path):
    with open(gns3_file_path, 'r') as f:
        data = json.load(f)

    routers = []
    for node in data.get("topology", {}).get("nodes", []):
        # Adjust these checks based on your file's structure
        if "IOU" in node.get("name", "") or node.get("node_type") == "iou":
            name = node["name"]
            # Try to get telnet info
            host = node.get("console_host", "localhost")
            port = node.get("console")
            routers.append({
                "name": name,
                "host": host,
                "port": port
            })
    return routers

if __name__ == "__main__":
    routers = parse_gns3_routers("RIP TOPOLOGY.json")
    for r in routers:
        print(r)

        