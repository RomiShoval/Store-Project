import yaml
from errors import TooManyMatchesError, ItemAlreadyExistsError, ItemNotExistError
from item import Item
from shopping_cart import ShoppingCart


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """
        Given tne name of the item and the store ,return a sorted list of all the items that match the search term.
        :param item_name: String
        :return: list
        """
        list = []
        cart = self._shopping_cart.items
        tags = self._shopping_cart.tags
        for item in self._items:
            if item_name in item.name and item not in cart:
                list.append(item)
            elif item_name in item.name and len(cart)==1:
                list.append(item)
        newlist = sorted(list, key=lambda x: (-self._shopping_cart.count_tags(x, tags), x.name))
        for y in newlist:
            print(y)
        return newlist

    def search_by_hashtag(self, hashtag: str) -> list:
        """
        Given tne specific hashtag of the item and the store ,return a sorted list of all the items matching the hashtag.
        :param hashtag: String
        :return: list
        """
        list = []
        tags = self._shopping_cart.tags
        cart = self._shopping_cart.items
        for item in self._items:
            if item not in cart:
                for hashtag1 in item.hashtags:
                    if hashtag1 == hashtag:
                        list.append(item)
                        break
        new_list = sorted(list, key=lambda x: (-self._shopping_cart.count_tags(x, tags), x.name))
        for y in new_list:
            print(y)
        return new_list

    def add_item(self, item_name: str):
        """
        Adds an item with the given name to the customer’s shopping cart.
        :param item_name: String
        """
        list = self.search_by_name(item_name)
        if len(list) == 0:
            raise ItemNotExistError
        item = self._getItemByName(item_name)
        if len(list) > 1:
            raise TooManyMatchesError
        if item_name in self._shopping_cart.items:
            raise ItemAlreadyExistsError
        else:
            self._shopping_cart.add_item(item)

    def remove_item(self, item_name: str):
        """
        Removes an item with the given name from the customer’s shopping cart.
        :param item_name: String
        """
        list = self.search_by_name(item_name)
        if len(list) == 0:
            raise ItemNotExistError
        if len(list) > 1:
            raise TooManyMatchesError
        else:
            for item in self._shopping_cart.items:
                if item_name in item.name:
                    self._shopping_cart.remove_item(item.name)

    def checkout(self) -> int:
        """
        Calculate the total price of all the items in the costumer’s shopping cart.
        :return: Integer
        """
        return self._shopping_cart.get_subtotal()

    def _getItemByName(self, item_name):
        """
        given the item name , return the item object.
        :param item_name: String
        :return: Item
        """
        for item in self._items:
            if item_name == item.name:
                return item
