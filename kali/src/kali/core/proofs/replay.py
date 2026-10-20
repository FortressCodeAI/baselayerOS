from ..hashing import sha256_obj


def generate_replay_proof(
        original_output,
        replay_output
):

    original_hash = sha256_obj(
        original_output
    )

    replay_hash = sha256_obj(
        replay_output
    )

    return {

        "proof_type":
            "replay_equivalence",

        "equivalent":
            original_hash == replay_hash,

        "original_hash":
            original_hash,

        "replay_hash":
            replay_hash
    }
