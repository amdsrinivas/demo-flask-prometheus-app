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

    # allocate large amount of data
    data_vector = [i+1 for i in range(1000 * offset)]
    # run some operation
    result = sum(data_vector)
    # block the thread for 1-5s
    time.sleep(random.randint(1, 5))

    end = time.time()
    return app.make_response({"data_size": sys.getsizeof(data_vector) + sys.getsizeof(result),
                              "cpu_time": end-start})


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
