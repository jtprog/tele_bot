from apis.bittrex import BittrexClient


class Searcher:

    def __init__(self):
        # Получить список доступных валют
        self.bittrex = BittrexClient()
        self.names = list(self.bittrex.get_all_names())

    def parse_query(self, text: str) -> list:
        """ Понять что именно запросил пользователь
        """
        val = text.upper().strip()
        # TODO: нечёткий поиск
        return [name for name in self.names if val in name]

    def get_prices(self, names: list):
        """ Получить список цен для запрошенных валют
        """
        # Привести имя валюты к паре и обратно
        pairs = [f'USD-{name}' for name in names]
        for (pair, price) in self.bittrex.get_last_prices(pairs=pairs):
            name = pair.split('-')[1]
            yield name, price
