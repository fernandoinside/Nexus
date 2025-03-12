# src\database\neo4j_db.py
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password, database="neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
        self.ensure_vector_index()

    def add_document(self, text, embedding, metadata):
        with self.driver.session(database=self.database) as session:
            session.run(
                """
                CREATE (:Document {
                    text: $text,
                    embedding: $embedding,
                    language: $language,
                    category: $category,
                    timestamp: datetime()
                })
                """,
                text=text,
                embedding=embedding,
                language=metadata.get("language", "unknown"),
                category=metadata.get("category", "general"),
            )

    def query_similarity(self, embedding, top_n=5, min_score=0.8):
        """
        Consulta o banco de dados Neo4j para documentos semelhantes ao embedding fornecido.
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(
                """
                CALL db.index.vector.queryNodes('document_embedding', $top_n, $embedding)
                YIELD node, score
                WHERE score >= $min_score
                RETURN node.text AS text, score
                ORDER BY score DESC
                """,
                embedding=embedding,
                top_n=top_n,
                min_score=min_score
            )
            return result.data()

    def ensure_vector_index(self):
        """
        Verifica se o índice vetorial existe. Caso contrário, cria o índice.
        """
        with self.driver.session(database=self.database) as session:
            result = session.run("SHOW INDEXES")
            existing_indexes = [record["name"] for record in result]

            if "document_embedding" not in existing_indexes:
                session.run(
                    """
                    CREATE VECTOR INDEX document_embedding
                    FOR (n:Document) ON (n.embedding)
                    OPTIONS {
                        indexConfig: {
                            `vector.dimensions`: 384,
                            `vector.similarity_function`: 'cosine'
                        }
                    }
                    """
                )                            