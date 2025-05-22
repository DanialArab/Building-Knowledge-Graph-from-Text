from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

class TextProcessor:
    def __init__(self, chunk_size=500, chunk_overlap=30):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def split_text(self, text: str):
        return self.text_splitter.create_documents([text])

    def get_full_text(self, split_docs):
        return " ".join(doc.page_content for doc in split_docs)

    def segment_into_sentences(self, full_text: str):
        sentences = re.split(r'(?<=[.!?]) +', full_text)
        return "\n".join(sentences)

    def save_sentences(self, sentences: str, output_path: str):
        with open(output_path, 'w') as f:
            f.write(sentences)