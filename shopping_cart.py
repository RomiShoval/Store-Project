from errors import ItemNotExistError, ItemAlreadyExistsError
from item import Item


class ShoppingCart:
    def __init__(self):
        self.items = []
        self.subtotal = 0
        self.tags = []

    def add_item(self, item: Item):
        """
        Adds the given item to the shopping cart.
        :param item:Item
        """
        for c in self.items:
            if c.name == item.name:
                raise ItemAlreadyExistsError
        else:
            self.items.append(item)
            for hashtag in item.hashtags:
                self.tags.append(hashtag)

    def count_tags(self, item: Item, tags: list) -> list:
        """
        Given an item's hashtag list and a list of all the tags in the current shopping cart, counting the appearance of
        the specific hashtag.
        :param item:Item
        :param tags:List
        :return:List
        """
        count = 0
        for hashtag in item.hashtags:
            for tag in tags:
                if hashtag == tag:
                    count += 1
        return count

    def remove_item(self, item_name: str):
        """
        Removes the item with the given name from the shopping cart.
        :param item_name:String
        """
        for item in self.items:
            if item_name in item.name:
                self.items.remove(item)
                return
        else:
            raise ItemNotExistError

    def get_subtotal(self) -> int:
        """
        Calculate the subtotal price of all the items currently in the shopping cart.
        :return: Integer
        """
        for item in self.items:
            self.subtotal += item.price
        return self.subtotal
