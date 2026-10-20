import os

import kali.operators.summarize

from kali.symbolic.replay_engine import (
    ReplayEngine
)


def main():

    execution_id = (
        os.environ[
            "KALI_EXECUTION_ID"
        ]
    )

    return ReplayEngine.replay(
        execution_id
    )