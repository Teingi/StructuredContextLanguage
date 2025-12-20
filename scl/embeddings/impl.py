## logic it can reuse powermem
import os
from openai import OpenAI

class OpenAIEmbedding:
    def __init__(self):
        self.model = os.getenv("EMBEDDING_MODEL", "BAAI/bge-large-zh-v1.5")
        self.embedding_dims = os.getenv("EMBEDDING_MODEL_DIMS", 1024)

        api_key = os.getenv("EMBEDDING_API_KEY")
        base_url = os.getenv("EMBEDDING_BASE_URL", "https://api.siliconflow.cn/v1")

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text):
        """
        Get the embedding for the given text using OpenAI.

        Args:
            text (str): The text to embed.
        Returns:
            list: The embedding vector.
        """
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(input=[text], model=self.model, dimensions=self.embedding_dims)
            .data[0]
            .embedding
        )

if __name__ == "__main__":
    def main():
        openai_embedding = OpenAIEmbedding()
        print(openai_embedding.embed("Hello, world!"))
    main()