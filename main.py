import os
from src.data_extractor import WikipediaDataExtractor
from src.text_processor import TextProcessor
from src.relation_extractor import RelationExtractor
from src.knowledge_graph_builder import CypherWrite, KnowledgeGraphBuilder

import json
# from langchain_community.graphs import Neo4jGraph
from src.text_normalizer import TextNormalizer



if __name__ == "__main__":
    query = "Ahmad Reza Abedzadeh"
    output_text_file = "data/Abedzadeh.txt"
    output_normalized_text_file = "data/Normalized_Abedzadeh.txt"
    output_relations_file = "data/clear_result_Abedzadeh.txt"
    cypher_query_file = "data/cypher_query.txt"
    entity_types = ['person', 'award', 'team', 'company', 'characteristic']
    relation_types = ['playsFor', 'hasAward', 'hasCharacteristic', 'defeated', 'isFounderOf', 'member', 'children']
    examples = [
        {"text": "Adam is a soccer player for the Liverpool team since 2009, and last year he won the Golden Boot award", "head": "Adam", "head_type": "person", "relation": "playsFor", "tail": "Liverpool", "tail_type": "team"},
        {"text": "Adam is a soccer player for the Liverpool team since 2009, and last year he won the Golden Boot award", "head": "Adam", "head_type": "person", "relation": "hasAward", "tail": "Golden Boot", "tail_type": "award"},
        {"text": "Liverpool is a soccer team that won the Premier League title in 2020", "head": "Premier League title", "head_type": "award", "relation": "isWonBy", "tail": "Liverpool", "tail_type": "team"},
        {"text": "The Golden Boot is awarded to the top scorer of the Premier League", "head": "Golden Boot", "head_type": "award", "relation": "hasCharacteristic", "tail": "top scorer of the Premier League", "tail_type": "characteristic"},
        {"text": "Adam Luis was player of UK national team that defeated US team", "head": "UK national team", "head_type": "team", "relation": "defeated", "tail": "US team", "tail_type": "team"},
    ]

    # Data Extraction
    data_extractor = WikipediaDataExtractor()
    raw_text = data_extractor.fetch_and_clean(query)
    # print (raw_text)

    # Text Processing
    text_processor = TextProcessor()
    split_docs = text_processor.split_text(raw_text)
    full_text = text_processor.get_full_text(split_docs)
    formatted_sentences = text_processor.segment_into_sentences(full_text)
    text_processor.save_sentences(formatted_sentences, output_text_file)
    # print (formatted_sentences)
    # Relation Extraction

    text_normalizer = TextNormalizer()
    text_normalizer.load_text(output_text_file)
    entities = text_normalizer.extract_entities()
    text_normalizer.canonicalize_entities(entities)
    normalized_formatted_sentences = text_normalizer.normalize_text()
    text_normalizer.save_normalized_text(output_normalized_text_file, normalized_formatted_sentences)


    relation_extractor = RelationExtractor(entity_types, relation_types, examples)
    all_extracted_relations = []
    with open(output_normalized_text_file, 'r') as f:
        # sentences = f.read().splitlines()
        sentences = f.read().split('. ')

        for sentence in sentences:
            if sentence.strip():
                relations = relation_extractor.extract_relations_from_sentence(sentence, entity_types, relation_types, examples)
                # print (relations)
                all_extracted_relations.extend(relations)
    print (all_extracted_relations)

    with open(output_relations_file, 'w') as f:
        json.dump(all_extracted_relations, f, indent=4)

    unique_entities = set()
    for item in all_extracted_relations:
        if 'tail' in item and 'head' in item:
            unique_entities.add((item['head'], item['head_type']))
            unique_entities.add((item['tail'], item['tail_type']))
        else:
            print("Missing keys, either tail or head, in item:", item)
    
    cypher_statements = set()
    for item in all_extracted_relations:
        head = item['head'].replace(" ","_").replace("-","").replace("'","").lower()
        tail = item['tail'].replace(" ","_").replace("-","").replace("'","").lower()
        cypher = f"""MERGE ({head})-[:{item['relation']}]->({tail})\n"""
        # print (cypher)
        cypher_statements.add(cypher)

    # print(f"cypher_statements: {cypher_statements}")

    unique_entities_list = list(unique_entities)
    # print(f"unique_entities_list: {unique_entities_list}")

    merge_statemetns_writer = CypherWrite(cypher_query_file)
    # merge_statemetns_writer.write_merge_statements (unique_entities_list)
    merge_statemetns_writer.write_merge_statements (unique_entities_list, cypher_statements)

    neo4j_url = os.environ.get("neo4j_url")  
    neo4j_user = os.environ.get("neo4j_user")  
    neo4j_password = os.environ.get("neo4j_password")  

    kg_builder = KnowledgeGraphBuilder(
        neo4j_url=neo4j_url,
        neo4j_user=neo4j_user,
        neo4j_password=neo4j_password)
    kg_builder.execute_merge_statements(path_to_merge_statements=cypher_query_file)