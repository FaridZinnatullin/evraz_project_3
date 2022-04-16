def test__on_get_show_cart(client, checkout_service, cart):
    cart.positions[0].product.sku = 'FOO'
    cart.positions[0].product.price = 1
    cart.positions[0].quantity = 12
    cart.positions[1].product.sku = 'BAR'
    cart.positions[1].product.price = 2
    cart.positions[1].quantity = 22

    checkout_service.get_cart.return_value = cart

    expected = {
        'positions': [
            {
                'product_sku': cart.positions[0].product.sku,
                'product_price': cart.positions[0].product.price,
                'quantity': cart.positions[0].quantity
            },
            {
                'product_sku': cart.positions[1].product.sku,
                'product_price': cart.positions[1].product.price,
                'quantity': cart.positions[1].quantity
            },
        ]
    }

    result = client.simulate_get('/api/checkout/show_cart')

    assert result.status_code == 200
    assert result.json == expected
