import bpy

from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
    def close(self):
        # Close the connection
        if self.driver:
            self.driver.close()
    def fetch_nodes(self):
        # Execute a query to fetch 5 nodes
        with self.driver.session() as session:
            result = session.run("MATCH (t:Point) RETURN t")
            return [record["t"] for record in result]

# Connection parameters
uri = "neo4j://localhost:7687"
username = "neo4j"
password = "password"

# Establishing a connection and fetching nodes
connection = Neo4jConnection(uri, username, password)
nodes = connection.fetch_nodes()
for node in nodes:
    print(node)
    x = node.get('x', 0)  # Replace 0 with your preferred default value for x
    y = node.get('y', 0)  # Replace 0 with your preferred default value for y
    z = node.get('z', 0)  # Replace 0 with your preferred default value for z

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,
                                          radius=1,
                                          enter_editmode=False,
                                          align='WORLD',
                                          location=(x, y, z),
                                          scale=(1, 1, 1)
                                          )

# Don't forget to close the connection
connection.close()


### P.S. an example query to create the point
# CREATE (p:Point {name: 'Sample Point', x: 4, y: 2, z: 6}) RETURN p;
