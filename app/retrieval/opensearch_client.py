from opensearchpy import OpenSearch


def get_opensearch_client() -> OpenSearch:
    return OpenSearch(
        hosts=[
            {
                "host": "localhost",
                "port": 9200,
            }
        ],
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False,
    )