class QueryManager:
    def __init__(self, neo4j_client):
        self.neo4j_client = neo4j_client

    def search_by_category(self, category, top_n=5):
        """
        Busca documentos por categoria.
        """
        with self.neo4j_client.driver.session() as session:
            result = session.run(
                """
                MATCH (d:Document)
                WHERE d.category = $category
                RETURN d.text AS text, d.timestamp AS timestamp
                ORDER BY d.timestamp DESC
                LIMIT $top_n
                """,
                category=category,
                top_n=top_n
            )
            return result.data()

    def search_with_filters(self, query_embedding, category=None, min_score=0.8, top_n=5):
        """
        Busca documentos com filtros adicionais.
        """
        with self.neo4j_client.driver.session() as session:
            query = """
            CALL db.index.vector.queryNodes('document_embedding', $top_n, $embedding)
            YIELD node, score
            WHERE score >= $min_score
            """
            if category:
                query += " AND node.category = $category"
            query += """
            RETURN node.text AS text, score
            ORDER BY score DESC
            """

            result = session.run(
                query,
                embedding=query_embedding,
                category=category,
                min_score=min_score,
                top_n=top_n
            )
            return result.data()
