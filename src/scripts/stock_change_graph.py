from opensearchpy import OpenSearch

class StockChangeGraph:
    def __init__(self):
        pass


class OpenSearchClient:
    """
    TODO add docstring
    """
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth = ("admin", "admin"),
            http_compress = True, # enables gzip compression for request bodies
            use_ssl = False,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False
        )
        
    def get_documents(self, index: str, query: str):
        return self.client.seach(
            index=index,
            body={query}
        )

client = OpenSearchClient('localhost', 9200)
# print(client.info)