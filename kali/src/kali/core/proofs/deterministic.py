from ..hashing import sha256_obj


def generate_deterministic_proof(
        action_slug,
        payload,
        output,
        code_version,
        rulebook_hash
):

    proof_material = {
        "action_slug":
            action_slug,

        "payload":
            payload,

        "output":
            output,

        "code_version":
            code_version,

        "rulebook_hash":
            rulebook_hash
    }

    execution_hash = sha256_obj(
        proof_material
    )

    return {
        "proof_type":
            "deterministic_execution",

        "execution_hash":
            execution_hash,

        "material":
            proof_material
    }
