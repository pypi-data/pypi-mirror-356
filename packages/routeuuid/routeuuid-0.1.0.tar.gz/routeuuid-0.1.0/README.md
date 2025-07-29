> **Select your language:** [English](README.md), [Español](README.es.md)

# RouteUUID

**RouteUUID** is a Flask extension that allows you to differentiate between various UUID versions in your routes.

## Features

- **UUID Version Differentiation**  
  Use specific URL converters to ensure that the UUID in the route matches the expected version.

| UUID Version  | Converter      | Provider      | Observation                          |
|---------------|----------------|---------------|--------------------------------------|
| **UUID**      | `<uuid:...>`   | **werkzeug**  | Native; does not distinguish version |
| **UUID v1**   | `<uuid1:...>`  | **routeuuid** |                                      |
| **UUID v2**   | `<uuid2:...>`  |               | Not Implemented                      |
| **UUID v3**   | `<uuid3:...>`  | **routeuuid** |                                      |
| **UUID v4**   | `<uuid4:...>`  | **routeuuid** |                                      |
| **UUID v5**   | `<uuid5:...>`  | **routeuuid** |                                      |

## Installation

You can install **RouteUUID** via pip:

```bash
pip install routeuuid
```

Below is a simple example of how to use **RouteUUID** in your Flask application:

```python
from uuid import UUID
from flask import Flask
from routeuuid import RouteUUID

app = Flask(__name__)

# Register the custom UUID converters in the Flask app.
RouteUUID(app)

# Or:
#
# route_uuid = RouteUUID()
# ...
# route_uuid.init_app(app)

@app.route("/item/<uuid4:item_id>")
def get_item_v4(item_id: UUID):
    return f"Item ID (UUID v4): {item_id}"

@app.route("/item/<uuid1:item_id")
def get_item_v1(item_id: UUID):
    return f"Item ID (UUID v1): {item_id}"

if __name__ == "__main__":
    app.run(debug=True)
```

In this example, the route `/item/<uuid4:item_id>` will only accept strings that conform to the format of a UUID version 4.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.