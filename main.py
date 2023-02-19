from datetime import datetime
from decimal import *

coupons = [(0, 0.9),  # -10% 1
           (-1.5, 1),  # -1.5€ 2
           (0, 1.09),  # +9% 3
           (0, 0.95),  # -5% 4
           (-6, 1),  # -6€ 5
           (7, 1),  # +7€ 6
           (0, 0.85),  # -15% 7
           (-8, 1),  # -8€ 8
           (12, 1),  # +12€ 9
           (0, 0.94),  # -6% 10
           (-9.8, 1),  # -9.80€ 11
           (-2, 1)  # -2€ 12
           ]

best_price = 999
best_order = []


def compute_value(order: list):
    def apply(pos, value):
        if pos == 0:  # if not a coupon but separator, do nothing
            return value

        # retrieve value from coupon list
        add_value = coupons[pos-1][0]
        multiply_value = coupons[pos-1][1]

        if (pos == 5 and value < 49) or (pos == 8 and value < 149):
            return value

        return (value + add_value) * multiply_value

    article1 = 180
    article2 = 79
    article3 = 29

    first_split = order.index(0)
    second_split = order.index(0, first_split+1)

    for operation in order[:first_split]:
        article1 = apply(operation, article1)

    for operation in order[first_split:second_split]:
        article2 = apply(operation, article2)

    for operation in order[second_split:]:
        article3 = apply(operation, article3)

    return (
        # first_split, second_split,
        article1 + article2 + article3)


def test_compute():
    order1 = [9, 6, 3, 7, 1, 10, 8, 4, 11, 12, 5, 2, 0, 0]
    order2 = [9, 6, 3, 7, 1, 10, 8, 0, 4, 11, 12, 5, 2, 0]
    order3 = [9, 6, 3, 7, 1, 10, 8, 0, 4, 11, 12, 0, 5, 2]
    order4 = [0, 0, 9, 6, 3, 7, 1, 10, 8, 4, 11, 12, 5, 2]
    assert compute_value(order1) == (121.28098194999995 + 79 + 29)
    # assert compute_value(order2) == (7, 13)
    # assert compute_value(order3) == (7, 11)
    # assert compute_value(order4) == (0, 1)


test_compute()


def position(order, coupon_value):
    global best_price, best_order
    if coupon_value == 4:
        print(datetime.now().timestamp())
    if coupon_value == 13:
        price = compute_value(order)
        if price < best_price:
            best_price = price
            best_order = order
            print(best_price, best_order)
        return
    for coupon_position in range(14):
        if order[coupon_position] != 0:
            continue
        order[coupon_position] = coupon_value
        position(order, coupon_value+1)
        order[coupon_position] = 0


order = [0 for i in range(14)]


position(order, 1)

print(best_price, best_order)
