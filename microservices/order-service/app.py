from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

orders_db = {}
order_counter = 1

class Order(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.post("/orders")
def create_order(order: Order):
    global order_counter
    orders_db[order_counter] = {
        "id": order_counter,
        **order.dict(),
        "status": "created"
    }
    order_counter += 1
    return orders_db[order_counter - 1]

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]