from prime_sdk.get_order import GetOrderResponse
from prime_sdk.model import Order


def test_get_order_response_parsing():
    mock_json = {
        "order": {
            "id": "order-123",
            "user_id": "user-abc",
            "portfolio_id": "portfolio-xyz",
            "product_id": "BTC-USD",
            "side": "BUY",
            "client_order_id": "client-order-1",
            "type": "LIMIT",
            "base_quantity": "1.0",
            "quote_value": "60000.00",
            "limit_price": "60000.00",
            "start_time": "2024-01-01T00:00:00Z",
            "expiry_time": "2024-01-01T01:00:00Z",
            "status": "FILLED",
            "time_in_force": "GTC",
            "created_at": "2024-01-01T00:00:00Z",
            "filled_quantity": "1.0",
            "filled_value": "60000.00",
            "average_filled_price": "60000.00",
            "commission": "0.00",
            "exchange_fee": "0.00",
            "historical_pov": "100",
            "stop_price": "0.00",
            "net_average_filled_price": "60000.00",
            "user_context": "some-context",
            "client_product_id": "BTC-USD"
        }
    }

    response = GetOrderResponse(response=mock_json)

    assert isinstance(response.response, dict)
    assert "order" in response.response
    assert isinstance(response.order, Order)

    assert response.order.id == "order-123"
    assert response.order.side == "BUY"
    assert response.order.status == "FILLED"
    assert response.order.product_id == "BTC-USD"
