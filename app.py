import random
import time
import sys

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)


@app.route("/eatMemory/<int:offset>", methods=["GET"])
def eat_memory(offset: int):
    start = time.time()

    # Ensure we don't blow up
    if offset > 10000:
        offset = 10000

    # allocate array to hold large amount of data
    data_vector = []
    # run some operation
    for i in range(1000 * offset):
        op = random.randint(20, 30) * random.randint(20, 30)
        data_vector.append(op)

    end = time.time()
    return app.make_response({"data_size": sys.getsizeof(data_vector),
                              "cpu_time": end - start})


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
