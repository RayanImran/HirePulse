import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Correct client initialization, assuming 'PersistentClient' exists
        try:
            self.chroma_client = chromadb.PersistentClient(path='vectorstore')  # Ensure this matches your environment
        except AttributeError as e:
            print(f"ChromaDB client initialization error: {e}")

        # Proper collection creation
        try:
            self.collection = self.chroma_client.get_or_create_collection(name="portfolio")
        except Exception as e:
            print(f"Error creating or accessing collection: {e}")

    def load_portfolio(self):
        try:
            if not self.collection.count():  # Check if the collection is empty before loading data
                for _, row in self.data.iterrows():
                    # Add documents with metadata and UUID
                    self.collection.add(
                        documents=[row["Techstack"]],  # It should be in list format
                        metadatas=[{"links": row["Links"]}],  # Metadatas also expect a list
                        ids=[str(uuid.uuid4())]
                    )
        except Exception as e:
            print(f"Error loading portfolio: {e}")

    def query_links(self, skills):
        try:
            # Query the collection and retrieve metadata
            result = self.collection.query(query_texts=[skills], n_results=2)  # Ensure query_texts is a list
            return result.get('metadatas', [])
        except Exception as e:
            print(f"Error querying links: {e}")
            return []
