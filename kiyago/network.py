import time
import yaml
import mysql.connector

from core import decor
from dataclasses import dataclass


@dataclass
class Payload:
    timestamp: int = 0
    problem_id: int = 0
    user_id: int = 0
    code: str = ""


class Network:
    # Setup connection
    def __init__(self):
        # Parse from dbconf.yaml
        with open("./kiyago/dbconf.yaml") as f:
            dbconf = yaml.load(f, Loader=yaml.FullLoader)

        self.mydb = mysql.connector.connect(
            host=dbconf["host"],
            user=dbconf["user"],
            port=dbconf["port"],
            password=dbconf["password"],
            database=dbconf["database"],
        )
        self.mycursor = self.mydb.cursor(buffered=True)

    # Upload result to database
    def send_result(self, result: list):
        sql = "UPDATE submission SET verdict = %s, score = %s, timeuse = %s, state = 1 WHERE submissionId = %s"
        val = (*result, self.submission_id)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        decor.says.network("Result sent.")

    # Upload compile error to database
    def send_error(self, errmsg: str):
        sql = "UPDATE submission SET errmsg = %s, verdict = %s, state = 1 WHERE submissionId = %s"
        val = (errmsg, "Compilation error", self.submission_id)
        self.mycursor.execute(sql, val)
        self.mydb.commit()
        decor.says.network("Error message sent.")

    # Check for new submission
    def update(self):
        try:
            self.mydb.commit()
        except:
            decor.says.network("Cannot update database.")

    # Fetch new query. Returns None if no query avails.
    def get(self):
        try:
            self.mycursor.execute(
                "SELECT time, probId, userId, scode, submissionId FROM submission WHERE state = 0 ORDER BY time"
            )
            submission = self.mycursor.fetchone()
        except:
            decor.says.network("Cannot fetch query from database.")
            submission = None
        if submission == None:
            return None
        decor.says.network("Payload recieved.")
        self.submission_id = submission[4]
        return Payload(*submission[:4])