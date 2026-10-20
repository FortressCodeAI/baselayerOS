from kali.symbolic.replay_engine import (
    ReplayEngine
)


def replay_execution(
    execution_id
):

    result = (
        ReplayEngine
        .replay(
            execution_id
        )
    )

    print(result)