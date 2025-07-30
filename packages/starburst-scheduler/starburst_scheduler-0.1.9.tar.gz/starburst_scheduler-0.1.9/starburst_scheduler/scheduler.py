import schedule
import time
import logging
from .connector import StarburstConnector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QueryScheduler:
    def __init__(self, connector):
        self.connector = connector
        self.jobs = []

    def schedule_query(self, query, frequency, time_unit="seconds"):
        def job():
            logging.info(f"Running scheduled query: {query}")
            result = self.connector.execute_query(query)
            if result:
                logging.info(f"Query result: {result}")

        if time_unit == "seconds":
            schedule.every(frequency).seconds.do(job)
        elif time_unit == "minutes":
            schedule.every(frequency).minutes.do(job)
        elif time_unit == "hours":
            schedule.every(frequency).hours.do(job)
        elif time_unit == "days":
            schedule.every(frequency).days.do(job)
        else:
            raise ValueError("Unsupported time unit. Use seconds, minutes, hours, or days.")

        self.jobs.append(job)
        logging.info(f"Scheduled query: {query} every {frequency} {time_unit}")
        return job

    def run(self):
        logging.info("Starting scheduler... Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Scheduler stopped.")