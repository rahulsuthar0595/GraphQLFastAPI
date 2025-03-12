import logging
import time

from strawberry.extensions import SchemaExtension

logging.basicConfig(level=logging.INFO)


class ResponseLogExtension(SchemaExtension):
    def on_operation(self):
        start_time = time.time()
        yield
        logging.info(f"GraphQL Operation Time: {time.time() - start_time}")
