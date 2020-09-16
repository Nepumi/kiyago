import time
import yaml
import mysql.connector

from core import decor
from dataclasses import dataclass

Test_Queue =[(0,1,6969,"#include<stdio.h>\nint main(){printf(\"Meow\"); return 0;}",'c',0)]

Test_Queue.append((0,1,6970,"#include<stdio.h>\nint main(){int n;scanf(\"%d\",&n);for(int i=0;i<n;i++){for(int j=0;j<n;j++)printf(\"*\");\nprintf(\"\\n\");}}",'c',0))
Test_Queue.append((0,1,6971,"n = int(input())\nprint((\"*\"*n+\"\\n\")*n)",'py',0))


@dataclass
class Payload:
    timestamp: int = 0
    problem_id: int = 0
    user_id: int = 0
    code: str = ""
    lang: str = ""


class Network:

    # Upload result to database
    def send_result(self, result: list):
        sql = "UPDATE submission SET verdict = %s, score = %s, timeuse = %s, state = 1 WHERE submissionId = %s"
        val = (*result, self.submission_id)
        #self.mycursor.execute(sql, val)
        #self.mydb.commit()
        decor.says.network("Result sent.")

    # Upload compile error to database
    def send_error(self, errmsg: str):
        sql = "UPDATE submission SET errmsg = %s, verdict = %s, state = 1 WHERE submissionId = %s"
        val = (errmsg, "Compilation error", self.submission_id)
        #self.mycursor.execute(sql, val)
        #self.mydb.commit()
        decor.says.network("Error message sent.")

    # Check for new submission
    def update(self):
        try:
            pass
        except:
            decor.says.network("Cannot update database.")

    # Fetch new query. Returns None if no query avails.
    def get(self):
        if len(Test_Queue) > 0:
            submission = Test_Queue[0]
            Test_Queue.pop(0)
        else:
            decor.says.network("Cannot fetch query from database.")
            submission = None
        if submission == None:
            return None
        decor.says.network("Payload recieved.")
        self.submission_id = submission[-1]
        return Payload(*submission[:-1])