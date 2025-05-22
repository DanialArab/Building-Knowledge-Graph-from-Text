from langchain_community.document_loaders import WikipediaLoader

class WikipediaDataExtractor:
    def __init__(self):
        pass

    def fetch_and_clean(self, query: str):
        raw_documents = WikipediaLoader(query=query).load()
        if raw_documents:
            filtered_document = raw_documents[0]  
            text = filtered_document.page_content.replace("\n", "").replace("==", "")
            return text
        return ""