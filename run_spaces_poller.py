import time
import logging
import argparse
from datetime import datetime
from starlette.testclient import TestClient
from main import app


def poll_spaces(interval_seconds: int = 300):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    client = TestClient(app)
    logging.info("Starting /spaces poller (interval=%s seconds)", interval_seconds)
    try:
        while True:
            start = datetime.utcnow().isoformat()
            try:
                logging.info("Requesting /spaces at %s", start)
                resp = client.get("/spaces")
                logging.info("Response status=%s", resp.status_code)
                logging.info("Response body: %s", resp.text)
            except Exception:
                logging.exception("Error while requesting /spaces")
            time.sleep(interval_seconds)
    except KeyboardInterrupt:
        logging.info("Poller interrupted, exiting")


def main():
    parser = argparse.ArgumentParser(description="Poll /spaces route periodically (in-process)")
    parser.add_argument("--interval", type=int, default=300, help="Interval in seconds between polls (default: 300)")
    args = parser.parse_args()
    poll_spaces(args.interval)


if __name__ == "__main__":
    main()
