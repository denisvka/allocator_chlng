import random


class Inventory(object):
    """
    Represents a virtual inventory

    Arguments: None

    Attributes:
    existing_inventory(dict): items in stock
    backordered_inventory(dict): items that have to be back ordered
    """
    def __init__(self):
        self.existing_inventory = {'A': 150, 'B': 150, 'C': 100, 'D': 100,
                                   'E': 200}
        self.backordered_inventory = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}

    @property
    def total(self):
        """
        Return the total amount of all items in stock

        >> classname.total
        700

        """
        return sum(self.existing_inventory.values())

    def inventory_allocator(self, order):
        """
        Allocate inventory between existing inventory and back ordered

        Parameter:
        order(dict): {"Header": 1, "Lines": [{"Product": "B", "Quantity": "1"}, {"Product": "C", "Quantity": "1"}]}

        Return:
        str that represents order id, qty of items in order,
        qty of items in order can be fulfilled,
        qty of items back ordered

        >> classname.inventory_allocator({"Header": 1, "Lines": [{"Product": "B", "Quantity": "1"}, {"Product": "C", "Quantity": "1"}]})
        1: 0,1,1,0,0::0,1,1,0,0::0,0,0,0,0

        """
        # preparing the list for filling up with items from order
        order_input = ['0'] * len(self.existing_inventory)
        fulfilled_order = order_input[:]
        backordered = order_input[:]

        for item in order['Lines']:
            item_index = sorted(self.existing_inventory.keys()).index(item['Product'])
            # filling up the list with item qty from order
            order_input[item_index] = str(item['Quantity'])

            if item['Quantity'] > self.existing_inventory[item['Product']]:
                difference = abs(self.existing_inventory[item['Product']] - item['Quantity'])
                self.existing_inventory[item['Product']] -= item['Quantity'] - difference
                self.backordered_inventory[item['Product']] += difference

                # filling up the list with fulfilled qty of items
                fulfilled_order[item_index] = str(item['Quantity'] - difference)
                # filling up the list with qty of items to be back ordered
                backordered[item_index] = str(difference)
            else:
                self.existing_inventory[item['Product']] -= item['Quantity']
                # filling up the list with fulfilled qty of items
                fulfilled_order[item_index] = str(item['Quantity'])
        return '{}: {}'.format(order['Header'], '::'.join([','.join(lst) for lst in [order_input, fulfilled_order, backordered]]))


class OrderGenerator(object):
    """
    Represents an order generator

    Arguments: None

    Attributes:
    order_id(int): number of an order

    """
    def __init__(self):
        self.order_id = 0

    def generate_order(self):
        """
        Generate an order with random items and random qty of these items ranging
        between 1 and 5 inclusive

        Parameters: None
        Return:
        dict that looks like
        >> classname.generate_order()
        {"Header": 1, "Lines": [{"Product": "B", "Quantity": "1"}, {"Product": "C", "Quantity": "1"}]}

        """
        order = {'Header': self.order_id, 'Lines': []}
        random_items = sorted(random.sample(['A', 'B', 'C', 'D', 'E'],
                                            random.randint(1, 5)))
        for i in range(len(random_items)):
            order['Lines'].append({'Product': random_items[i],
                                   'Quantity': random.randint(1, 5)})
        self.order_id += 1
        return order


def main():
    inventory = Inventory()
    random_order = OrderGenerator()
    orders_summary = []
    while inventory.total > 0:
        orders_summary.append(inventory.inventory_allocator(random_order.generate_order()))

    for summary in orders_summary:
        print(summary)

if __name__ == '__main__':
    main()
