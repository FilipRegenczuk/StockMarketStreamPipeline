import numpy as np
import collections
import matplotlib.pyplot as plt
from opensearchpy import OpenSearch
from matplotlib.animation import FuncAnimation

class StockChangeGraph:
    def __init__(self):
        self.os_client = OpenSearchClient(
            host='localhost',
            port=9200
        )
    
    def create_animation_plot(self):
        value = collections.deque(np.zeros(10))
        fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
        ax = plt.subplot(121)
        ax.set_facecolor('#DEDEDE')

        def update_action_value(i):
            # get data
            value.popleft()
            curr_value = self.os_client.get_current_value('stock')
            value.append(curr_value)

            # clear axis
            ax.cla()

            # plot action value
            ax.plot(value)
            ax.scatter(len(value) - 1, value[-1])
            ax.text(len(value) - 1, value[-1] + 2, value[-1])
            # ax.set_ylim

        # animate plot
        ani = FuncAnimation(fig, update_action_value, interval=1000)
        plt.show()

    def run(self):
        self.create_animation_plot()


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
        result = self.client.search(index='stock', body=query)
        curr_value = (
            result
            .get('hits').get('hits')[0].get('_source').get('Close')
        )
        return curr_value


# client = OpenSearchClient('localhost', 9200)
# print(client.info)

graph = StockChangeGraph()
graph.run()