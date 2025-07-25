# Text to Graph: Swift Transformation from Unstructured Text to Structured Knowledge Graph
 
0. [A Bit of a Personal Note](#0)
1. [Potentials at a Glance](#1)
2. [Tools and frameworks](#2)  
3. [Quick note on the data used for this demonstration](#3)
4. [Detailed Steps](#4)
   1. [Data Loading](#5)
   2. [Data Splitting](#6) 
   3. [Entity and Relation Definition](#7)
   4. [Prompt Template and NLP Model](#8)
      1. [System Prompt](#9)
      2. [Human Prompt](#10)
   5. [Parsing and Query Generation](#11)
   6. [Building the Knowledge Graph](#12)
5. [Conclusions](#13)
6. [References ](#14)
 
<a name="0"></a>
## A Bit of a Personal Note

I spent 9 years of my life playing professional soccer and had the honor of serving as the main goalkeeper for Iran's Youth National Team during the San Marco tournament in Italy. As a kid, I dreamed of becoming a goalkeeper, and Ahmad Reza Abedzadeh was my idol—I had his posters all over my room. Later, when I joined the youth team at Persepolis, I had an opportunity to practice with him for two years while he was the goalkeeper for the senior team. That experience was surreal and deeply motivating.

Years later, as I began developing this project—which converts unstructured data, like text, into a knowledge graph database—I chose his Wikipedia page as my proof of concept. It felt like coming full circle: using my technical skills to pay tribute to the person who first inspired my journey.

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/1.png)

Fig. 1: Ahmad Reza Abedzadeh

<a name="1"></a>
## Potentials at a Glance
Given the power of large language models (LLMs), the possibilities for building advanced solutions to solve real word probles are virtually limitless. By harnessing the capabilities of NLP and graph databases, we can create sophisticated systems that not only understand and process vast amounts of unstructured text but also reveal intricate relationships and patterns within the data. This project exemplifies how we can leverage these cutting-edge technologies to transform raw/unstructured text data into an interconnected/structured knowledge graph. The potential applications are huge. 

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/1000.png)
Fig. 2: We can build advanced solutions to quickly transform unstructured text into a structured graph 

<a name="2"></a>
## Tools and frameworks
To transform unstructured text into a structured knowledge graph database we can use a combination of advanced tools and libraries including 

- LangChain,
- Llama3,
- Groq, and
- Neo4j 

The project demonstrates the power of NLP models in conjunction with graph databases to transform raw/unstructured text data into an interconnected/structured knowledge graph.

<a name="3"></a>
## Quick note on the data used for this demonstration

As a quick demonstration, I chose data loaded as text from Wikipedia on Iranian legendary goalkeeper Ahmad Reza Abedzadeh. Here is the cleaned text:

      Ahmadreza Abedzadeh (Persian: احمدرضا عابدزاده, born 25 May 1966) is an Iranian former footballer who played as a goalkeeper.
      He played for Esteghlal, Sepahan, Persepolis and the Iranian national team.
      He made 78 appearances for Iran, and played for his country at the 1998 FIFA World Cup.Abedzadeh had an unbeaten record in the Tehran derby with 13 matches, seven wins and six draws.
      While playing for Persepolis, he went 802 consecutive minutes without conceding a goal.Abedzadeh was called up at 18 for the Iran national under-20 football team in 1984.
      After his good shows, he was invited to the senior team in 1987 by then-manager Parviz Dehdari.
      Abedzadeh debuted in the match against Kuwait on 27 February 1987, in which he conceded a goal in a 2–1 victory.
      He started in the 1990 Asian Games, where they won the gold medal after defeating North Korea in the final and Abedzadeh saved two penalties.
      At the tournament, he conceded only two goals scored from penalty kicks.Iran defeated Australia in the FIFA World Cup qualification play-offs to reach 1998 FIFA World Cup, their second participation in the World Cup and first since 1978.
      He missed the first match at the World Cup against Yugoslavia due to injury, then captained Iran at the next two games against United States and Germany.
      Iran finished third in their group and Abedzadeh announced his retirement from international football after the final match.Abedzadeh suffered a stroke in 2001 and that was the point in which he let go of professional football.
      He was released some weeks later, but required several surgeries after, and even to this day, has side effects from his stroke.
      Abedzadeh suffered again on 11 March 2007 when his mother died.He has also been the goalkeeping coach for many clubs after retiring from playing football.
      He coached Saipa in 2001, Esteghlal Ahvaz in 2005, Persepolis from 2008 to 2009, Steel Azin in 2010 and Los Angeles Blues from 2011 to 2012.Dubbed the Eagle of Asia for his ability to protect the net, Abedzadeh's international career stretched for 11 years.
      In 2009, he was named in a poll as Iran's favorite player the net, Abedzadeh's international career stretched for 11 years.
      In 2009, he was named in a poll as Iran's favorite player of last 30 years.
      His goalkeeping legacy in Iran is rivaled only by Nasser Hejazi.Abedzadeh married in 1988 and has one daughter, Negar, and one son, Amir, who is also a goalkeeper and plays for SD Ponferradina and the Iranian national team.
      Abedzadeh also runs a restaurant in Motelghoo, one of the cities of Northern Iran.EsteghlalIranian Football League: 1989–90Asian Club Championship: 1990–91, runner up: 1991PersepolisIranian Football League: 1995–96, 1996–97, 1998–99, 1999–2000Hazfi Cup: 1998–99IranAsian Games Gold Medal: 1990RSSSF archive of Ahmad Reza Abedzadeh's international appearances

In the following, the steps required to transform the text above into the knowledge graph will be detailed. 

<a name="4"></a>
## Detailed Steps

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/3.png)

Fig. 3: Quick overview of the pipeline

<a name="5"></a>
### Data Loading

In order to chat with our data we first need to load data and adjust its format to be able to work with. LangChain provides us with over 80 document loaders, which allows us access data of various formats like PDF, HTML, JSON, Word, PowerPoint, etc. from various resources like
- websites
- databases
- Youtube
- …

For this we can use different document loaders, shown in Fig. 4, to load data as text, video transcript, etc. and convert them to a standard document object which can consist of contents and the associated metadata. 

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/rgg.png)
Fig. 4: LangChain document loaders 

Then we need to split data into individual sentences to facilitate finer extraction of entities and relations.

<a name="6"></a>
### Data Splitting 

The documents could be huge and we need to split them up into smaller chunks. This is very important because when we do retrieval augmentation generation we only need to retrieve the piece of the content that is most relevant: we do not want to select the whole document that we loaded in but rather only a paragraph or a few sentences.

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/doc%20sp.png)
Fig. 5: Document splitting in LangChain 

This document splitting may sound trivial but it has a lot of nuances and details that may have a large effect down the line. The main idea is that we want to retain the meaningful relationship. For example, if we have the following data like

      ...
      on this model. The Toyota Camry has a head-snapping 80 HP and an eight-speed automatic transmission that will
      ...

Chunk 1: on this model. The Toyota Camry has a head-snapping

Chunk 2: 80 HP and an eight-speed automatic transmission that will


If we simply do splitting as above we may end up with part of the sentence in one chunk and the other part of the sentence in the other chunk. Therefore, we will not be able to answer the question like “what are the specifications on the Camry?” because we do not have the right information in either chunk. To solve this issue, we do the split with some chunks and overlaps, shown below:


![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/chunk.png)
Fig. 6: Document splitting into different chunks with specifying the chunk size and overlap helps us retain meaningful relationship

We can specify these details like chunk size, chunk overlap, separator, etc. in the specific text splitter we use, some of them areas follow:

- CharacterTextSplitter
- MarkdownHeaderTextSplitter
- TokenTextSplitter
- SentenceTransformersTokenTextSplitter
- RecursiveCharacterTextSplitter
- Language
- NLTKTextSplitter
- SpacyTextSplitter

<a name="7"></a>
### Entity and Relation Definition

Types of entities and relationships can be defined based on the context of the data. This step is crucial in setting up a clear schema for the knowledge graph. To set up the schema this resource could be useful. For this project I used the following entity types and relations:



      entity_types = ['person','award','team', 'company', 'characteristic']
      relation_types = ['playsFor','hasAward','hasCharacteristic','defeated','isFounderOf', 'member', 'children']

<a name="8"></a>
### Prompt Template and NLP Model

A prompt template is created to direct the NLP model to extract the desired information. The Llama3 model via Groq could be utilized to process the text and generate structured JSON outputs. We need to use two distinct types of prompts: System Prompt and Human Prompt. Each serves a specific purpose in guiding the model to perform the extraction task effectively.

<a name="9"></a>
#### System Prompt
The System Prompt defines the role and expectations for the language model. It sets up the model's task by providing clear instructions on how to identify and format the entities and relationships. It informs the model that it needs to act as an advanced algorithm designed to extract structured information for building a knowledge graph. It also specifies that the model should generate output in a JSON format, for example, with predefined keys: head, head_type, relation, tail, and tail_type. Each key has a specific role in representing the relationships between entities.

The system prompt also details the types of entities and relations that the model should focus on, ensuring that the extracted information aligns with the provided definitions. It also directs the model to extract as many entities and relations as possible, and to generate the output without additional explanations or text. Here is the system prompt I used:


      system_prompt = PromptTemplate(
          template = """
          You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph.
          Your task is to identify the entities and relations requested with the user prompt, from a given text.
          You must generate the output in a JSON containing a list with JSON objects having the following keys: "head", "head_type", "relation", "tail", and "tail_type".
          The "head" key must contain the text of the extracted entity with one of the types from the provided list in the user prompt. 
          The "head_type" key must contain the type of the extracted head entity which must be one of the types from {entity_types}.
          The "relation" key must contain the type of relation between the "head" and the "tail" which must be one of the relations from {relation_types}.
          The "tail" key must represent the text of an extracted entity which is the tail of the relation, and the "tail_type" key must contain the type of the tail entity from {entity_types}. 
          Attempt to extract as many entities and relations as you can. 
          IMPORTANT NOTES:
          - Don't add any explanation and text. 
          """,
          input_variables=["entity_types","relation_types"],
      )

<a name="10"></a>
#### Human Prompt

The Human Prompt is used to provide a more user-oriented approach to guide the model. It helps the model understand how to apply the system’s instructions to specific examples and the new text it will process. It offers examples of how text should be processed and what kind of extracted information should look like, serving as a reference for the model. It reiterates the entity and relation types that the model should use, ensuring consistency with the system prompt. It provides a specific text from which the model needs to extract entities and relations, using the format and guidelines set in the system prompt. It includes instructions for formatting the extracted information to ensure the output adheres to the required structure. Here is my human prompt:



      human_prompt = PromptTemplate(
          template = """ Based on the following example, extract entities and relations from the provided text.\n\n
          Use the following entity types, don't use other entity that is not defined below:
          # ENTITY TYPES:
          {entity_types}
          Use the following relation types, don't use other relation that is not defined below:
          # RELATION TYPES:
          {relation_types}
          Below are a number of examples of text and their extracted entities and relationshhips.
          {examples}
          For the following text, generate extract entitites and relations as in the provided example.\n{format_instructions}\nText: {text}""",
          input_variables=["entity_types","relation_types","examples","text"],
          partial_variables={"format_instructions": parser.get_format_instructions()},
      )

To clarify what is expected from the model in terms of output format and content, we need to provide examples. They provide concrete instances of how text should be processed and what kind of entities and relations should be extracted. This ensures that the model understands the task and the specific requirements for formatting the output. Here is the examples I used:

      examples = [
          {
              "text": "Adam is a soccer player for the Liverpool team since 2009, and last year he won the Golden Boot award",
              "head": "Adam",
              "head_type": "person",
              "relation": "playsFor",
              "tail": "Liverpool",
              "tail_type": "team"
          },
          {
              "text": "Adam is a soccer player for the Liverpool team since 2009, and last year he won the Golden Boot award",
              "head": "Adam",
              "head_type": "person",
              "relation": "hasAward",
              "tail": "Golden Boot",
              "tail_type": "award"
          },
          {
              "text": "Liverpool is a soccer team that won the Premier League title in 2020",
              "head": "Premier League title",
              "head_type": "award",
              "relation": "isWonBy",
              "tail": "Liverpool",
              "tail_type": "team"
          },
          {
              "text": "The Golden Boot is awarded to the top scorer of the Premier League",
              "head": "Golden Boot",
              "head_type": "award",
              "relation": "hasCharacteristic",
              "tail": "top scorer of the Premier League",
              "tail_type": "characteristic"
          },
          {
              "text": "Adam Luis was player of UK national team that defeated US team",
              "head": "UK national team",
              "head_type": "team",
              "relation": "defeated",
              "tail": "US team",
              "tail_type": "team"
          },
      ]

The outputs will include identified entities and their respective relationships, as shown below:

      [
          {
              "head": "Ahmadreza Abedzadeh",
              "head_type": "person",
              "relation": "playsFor",
              "tail": "Esteghlal",
              "tail_type": "team"
          },
          {
              "head": "Ahmadreza Abedzadeh",
              "head_type": "person",
              "relation": "hasAward",
              "tail": "Asian Games Gold Medal",
              "tail_type": "award"
          },
          {
              "head": "Ahmadreza Abedzadeh",
              "head_type": "person",
              "relation": "isFounderOf",
              "tail": "restaurant in Motelghoo",
              "tail_type": "company"
          },
          {
              "head": "Ahmadreza Abedzadeh",
              "head_type": "person",
              "relation": "hasCharacteristic",
              "tail": "Eagle of Asia",
              "tail_type": "characteristic"
          },
          {
              "head": "Ahmadreza Abedzadeh",
              "head_type": "person",
              "relation": "children",
              "tail": "Negar",
              "tail_type": "person"
          }
      ]

 

<a name="11"></a>
### Parsing and Query Generation
The structured JSON outputs are parsed to extract unique entities and relationships. Cypher queries ,shown below, are created to merge these entities and establish their relationships in the Neo4j database.



      MERGE (iranian_national_team:team {id: "Iranian national team"})
      MERGE (iranian_football_league:award {id: "Iranian Football League"})
      MERGE (negar:person {id: "Negar"})
      MERGE (amir:person {id: "Amir"})
      MERGE (restaurant_in_motelghoo:company {id: "restaurant in Motelghoo"})
      MERGE (sepahan:team {id: "Sepahan"})
      MERGE (ahmadreza_abedzadeh:person {id: "Ahmadreza Abedzadeh"})
      MERGE (eagle_of_asia:characteristic {id: "Eagle of Asia"})
      MERGE (persepolis:team {id: "Persepolis"})
      MERGE (esteghlal:team {id: "Esteghlal"})
      MERGE (sd_ponferradina:team {id: "SD Ponferradina"})
      MERGE (hazfi_cup:award {id: "Hazfi Cup"})
      MERGE (asian_games_gold_medal:award {id: "Asian Games Gold Medal"})
      MERGE (ahmadreza_abedzadeh)-[:playsFor]->(esteghlal)
      MERGE (ahmadreza_abedzadeh)-[:playsFor]->(sepahan)
      MERGE (ahmadreza_abedzadeh)-[:playsFor]->(persepolis)
      MERGE (ahmadreza_abedzadeh)-[:playsFor]->(iranian_national_team)
      MERGE (ahmadreza_abedzadeh)-[:hasAward]->(asian_games_gold_medal)
      MERGE (ahmadreza_abedzadeh)-[:isFounderOf]->(restaurant_in_motelghoo)
      MERGE (ahmadreza_abedzadeh)-[:hasCharacteristic]->(eagle_of_asia)
      MERGE (ahmadreza_abedzadeh)-[:children]->(negar)
      MERGE (ahmadreza_abedzadeh)-[:children]->(amir)
      MERGE (amir)-[:playsFor]->(sd_ponferradina)
      MERGE (amir)-[:playsFor]->(iranian_national_team)
      MERGE (esteghlal)-[:hasAward]->(iranian_football_league)
      MERGE (persepolis)-[:hasAward]->(iranian_football_league)
      MERGE (persepolis)-[:hasAward]->(hazfi_cup)

<a name="12"></a>
### Building the Knowledge Graph

Based on the above Cypher queries, we can build and populate the knowledge graph in Neo4j, shown below:

![](https://github.com/DanialArab/images/blob/main/text%20to%20graph/final.png)
Fig. 7: Final graph obtained from the text


<a name="13"></a>
## Conclusions
Here, I've provided a brief demonstration of how tools such as LangChain, Llama3, Groq, and Neo4j can be leveraged to convert text into graph databases. By efficiently transforming text data into meaningful, interconnected entities and relationships, we open up new huge opportunities. 

<a name="14"></a>
## References 
 
**<a href="https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/">LangChain: Chat with Your Data</a>**


 
