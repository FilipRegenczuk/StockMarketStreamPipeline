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
        return self.client.search(
            index=index,
            body={query}
        )
    
    def get_current_value(self, index: str):
        query = """{"sort": [{"Date": {"order": "desc"}}], "size": 1}"""
        curr_value = (
            self.get_documents(index, query)
            .get('hits').get('hits')[0].get('_source').get('Close')
        )
        return curr_value


client = OpenSearchClient('localhost', 9200)
# print(client.info)