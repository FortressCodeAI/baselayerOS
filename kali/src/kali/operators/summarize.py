from kali.runtime.registry import register


@register("summarize_stream")
def summarize_stream(payload):

    return {
        "summary":
            payload["summary"]
    }
