from langchain_community.graphs import Neo4jGraph

import re

import re

class CypherWrite:
    def __init__(self, output_cypher_query_file):
        self.path = output_cypher_query_file
        self.written_ids = set()  # Track written entity IDs

    def sanitize_variable_name(self, name):
        name = re.sub(r'\W', '_', name)  # Replace non-word characters with _
        if name and name[0].isdigit():
            name = 'n_' + name  # Prefix if it starts with a digit
        return name.lower()

    def write_merge_statements(self, unique_entities_list, cypher_statements):
        with open(self.path, 'w') as file:
            for label, entity in unique_entities_list:
                sanitized_label = label.strip()
                if sanitized_label.lower() in self.written_ids:
                    continue  # Skip duplicates
                self.written_ids.add(sanitized_label.lower())

                safe_id = self.sanitize_variable_name(sanitized_label)
                merge_statement = f"""MERGE ({safe_id}:{entity} {{id: "{label}"}})\n"""
                file.write(merge_statement)

        with open(self.path, 'a') as file:
            try:
                for statement in cypher_statements:
                    # Sanitize variable names in relationships
                    sanitized_statement = self.sanitize_statement(statement)
                    file.write(sanitized_statement)
                print(f"Cypher statements successfully written to {self.path}")
            except Exception as e:
                print(f"An error occurred while writing to {self.path}: {e}")

    def sanitize_statement(self, statement):
        """
        Sanitize variable names in the MERGE relationship statement.
        """
        def replacer(match):
            var = match.group(1)
            sanitized = self.sanitize_variable_name(var)
            return f'({sanitized}'

        return re.sub(r'\(([\w\d_]+)', replacer, statement)


class KnowledgeGraphBuilder:
    def __init__(self, neo4j_url, neo4j_user, neo4j_password):
      self.neo4j_url = neo4j_url
      self.neo4j_user = neo4j_user
      self.neo4j_password = neo4j_password

    def execute_merge_statements(self, path_to_merge_statements):
        with open(path_to_merge_statements, "r") as file:
            queries = file.read()
            # print (type(queries))
            # queries = queries[:62]
            # print (queries)

        try:
            graph = Neo4jGraph(url = self.neo4j_url, 
                               username = self.neo4j_user, 
                               password = self.neo4j_password)
            graph.query(queries) # This line sends a Cypher query string (in my case, MERGE statements read from a file) to my Neo4j database using the graph object, which is an instance of Neo4jGraph.
            graph.refresh_schema()
            print(graph.schema)
        except Exception as e:
            print(f"Error refreshing schema: {e}")
            print("Ensure Neo4j connection details are correct and Langchain Neo4jGraph is initialized if needed.")


