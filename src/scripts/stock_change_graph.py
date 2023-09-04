import numpy as np
import collections
import matplotlib.pyplot as plt
from opensearchpy import OpenSearch
from matplotlib.animation import FuncAnimation

class StockChangeGraph:
    """
    TODO
    """
    def __init__(self):
        self.os_client = OpenSearchClient(
            host='localhost',
            port=9200
        )
    
    def create_animation_plot(self):
        value = collections.deque(np.zeros(10))
        date = collections.deque(np.zeros(10))
        fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
        ax = plt.subplot(1,1,1)

        def update_action_value(i):
            # get data
            date.popleft()
            value.popleft()
            curr_date, curr_value = self.os_client.get_current_value('stock')
            date.append(curr_date)
            value.append(curr_value)

            # clear axis
            ax.cla()

            # plot action value
            ax.ticklabel_format(useOffset=False, style='plain')
            ax.plot(date, value)
            ax.scatter(date[-1], value[-1])
            ax.text(date[-1], value[-1] + 1, f"{value[-1]:.{2}f}$")
            ax.set_ylim(0, 300)
            ax.set_xlim(curr_date - 10, curr_date)

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
        result = self.client.search(index=index, body=query)
        result_fields = result.get('hits').get('hits')[0].get('_source')
        curr_value = result_fields.get('Close')
        curr_date = result_fields.get('Date')
        return (curr_date, curr_value)


graph = StockChangeGraph('')
graph.run()