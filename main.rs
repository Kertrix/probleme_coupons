const COUPONS: [(f64, f64); 12] = [
    (0.0, 0.9),
    (-1.5, 1.0),
    (0.0, 1.09),
    (0.0, 0.95),
    (-6.0, 1.0),
    (7.0, 1.0),
    (0.0, 0.85),
    (-8.0, 1.0),
    (12.0, 1.0),
    (0.0, 0.94),
    (-9.8, 1.0),
    (-2.0, 1.0),
];

static mut BEST_PRICE: f64 = 999.0;
static mut BEST_ORDER: [i32; 14] = [0; 14];

fn compute_value(order: &[i32]) -> f64 {
    fn apply(pos: usize, value: f64) -> f64 {
        if pos == 0 {
            // if not a coupon but separator, do nothing
            return value;
        }

        // retrieve value from coupon list
        let add_value = COUPONS[pos - 1].0;
        let multiply_value = COUPONS[pos - 1].1;

        if (pos == 5 && value < 49.0) || (pos == 8 && value < 149.0) {
            return value;
        }

        (value + add_value) * multiply_value
    }

    let mut article1 = 180.0;
    let mut article2 = 79.0;
    let mut article3 = 29.0;

    let first_split = order.iter().position(|&x| x == 0).unwrap();
    let second_split = order.iter().position(|&x| x == 0).unwrap() + 1;

    for operation in &order[..first_split] {
        article1 = apply(*operation as usize, article1);
    }

    for operation in &order[first_split..second_split] {
        article2 = apply(*operation as usize, article2);
    }

    for operation in &order[second_split..] {
        article3 = apply(*operation as usize, article3);
    }

    article1 + article2 + article3
}

fn position(order: &mut [i32; 14], coupon_value: i32) {
    unsafe {
        if coupon_value == 13 {
            let price = compute_value(order);
            if price < BEST_PRICE {
                BEST_PRICE = price;
                BEST_ORDER = *order;
                println!("{}, {:?}", BEST_PRICE, BEST_ORDER);
            }
            return;
        }
        for coupon_position in 0..14 {
            if order[coupon_position] != 0 {
                continue;
            }
            order[coupon_position] = coupon_value;
            position(order, coupon_value + 1);
            order[coupon_position] = 0;
        }
    }
}

fn main() {
    let mut order = [0; 14];
    position(&mut order, 1);
    unsafe {
        println!("{}, {:?}", BEST_PRICE, BEST_ORDER);
    }
}
