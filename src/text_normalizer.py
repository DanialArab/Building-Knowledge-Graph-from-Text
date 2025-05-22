import os
import re
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage


class TextNormalizer:
    def __init__(self, model_name="llama3-70b-8192", temperature=0.0):
        self.api_key = os.environ.get("groq_api_key")
        if not self.api_key:
            raise ValueError("groq_api_key environment variable not set.")
        
        self.llm = ChatGroq(
            temperature=temperature,
            model_name=model_name,
            api_key=self.api_key
        )
        self.raw_text = ""
        self.canonical_map = {}

    def load_text(self, path_to_file):
        """Loads text from a file."""
        with open(path_to_file, "r", encoding="utf-8") as f:
            self.raw_text = f.read()

    def extract_entities(self):
        """Extracts entity-like phrases using regex."""
        return list(set(re.findall(
            r"\b(?:Iranian|Iran|US|USA|American|U\.S\.)\s+(?:national\s+team|team|squad)\b",
            self.raw_text, re.IGNORECASE
        )))

    def canonicalize_entities(self, entities):
        """Uses the LLM to normalize entity names."""
        prompt = "Normalize the following entity names to canonical forms for a knowledge graph:\n\n"
        for i, entity in enumerate(entities, 1):
            prompt += f"{i}. {entity}\n"
    
        prompt += "\nReturn only the canonicalized list in the same numbered format, like:\n1. <original> → <canonical>\n"

        messages = [
            SystemMessage(content="You are a helpful assistant that canonicalizes entity names for a knowledge graph."),
            HumanMessage(content=prompt)
        ]

        response = self.llm(messages)
        lines = response.content.strip().split("\n")
        # print (f"lines: {lines}")
        canonical_map = {}
        for line in lines:
            match = re.match(r"\d+\.\s*(.*?)\s*->\s*(.*?)$", line)
            if match:
                original, canonical = match.groups()
                # print (original, canonical)
                canonical_clean = canonical.strip().split("→")[-1].strip().rstrip(".")
                canonical_map[original.lower()] = canonical_clean
            else:
                parts = line.split(". ", 1)
                if len(parts) == 2:
                    original = entities[int(parts[0]) - 1]
                    canonical = parts[1].strip()
                    # print ( canonical)
                    canonical_clean = canonical.strip().split("→")[-1].strip().rstrip(".")
                    # print (canonical_clean)
                    canonical_map[original.lower()] = canonical_clean

        self.canonical_map = canonical_map

    def normalize_text(self):
        """Replaces original entities with canonical ones in text."""
        normalized = self.raw_text
        for original, canonical in self.canonical_map.items():
            pattern = re.compile(rf"\b{re.escape(original)}\b", re.IGNORECASE)
            # print (pattern)
            normalized = pattern.sub(canonical, normalized)
        return normalized
    def save_normalized_text(self, output_path, normalized_text):
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(normalized_text)