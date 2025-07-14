
// Select the database to use.
use('my_records');

// Insert a few documents into the sales collection.
db.getCollection('orders').insertMany(
    [
   {
    "order_id": 2,
    "product": "Xbox Series X",
    "c_id": 100401
  },
  {
    "order_id": 3,
    "product": "Nintendo Switch",
    "c_id": 100402
  },
  {
    "order_id": 4,
    "product": "Gaming PC",
    "c_id": 100403
  },
  {
    "order_id": 5,
    "product": "VR Headset",
    "c_id": 100404
  },
  {
    "order_id": 6,
    "product": "Gaming Laptop",
    "c_id": 100405
  }
]

);

// Print a message to the output window.
console.log("Done inserting!!");


