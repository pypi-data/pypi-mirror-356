from pystarburst import Session
import trino.auth
import logging
import ssl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StarburstConnector:
    def __init__(self, host, port, user, password, catalog, schema, http_scheme="https", verify_ssl=True):
        self.db_parameters = {
            "host": host,
            "port": port,
            "http_scheme": http_scheme,
            "auth": trino.auth.BasicAuthentication(user, password),
            "catalog": catalog,
            "schema": schema
        }
        if not verify_ssl:
            self.db_parameters["verify"] = False  # Disable SSL verification if needed
        self.session = None

    def connect(self):
        try:
            self.session = Session.builder.configs(self.db_parameters).create()
            logging.info(f"Connected to Starburst cluster: {self.db_parameters['host']}:{self.db_parameters['port']}")
            return True
        except Exception as e:
            logging.error(f"Connection failed: {str(e)}")
            return False

    def execute_query(self, query):
        if not self.session:
            raise ValueError("Not connected to Starburst. Call connect() first.")
        try:
            result = self.session.sql(query).collect()
            logging.info(f"Query executed successfully: {query}")
            return result
        except Exception as e:
            logging.error(f"Query execution failed: {str(e)}")
            return None