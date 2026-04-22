def choose_mode(topic):

    topic = topic.lower()

    # Debate topics
    if (
        "replace" in topic
        or "danger" in topic
        or "vs" in topic
        or "good or bad" in topic
        or "ethical" in topic
    ):
        return "debate"

    # Motivation topics
    elif (
        "motivation" in topic
        or "success" in topic
        or "discipline" in topic
        or "confidence" in topic
    ):
        return "motivational"

    # News topics
    elif (
        "latest" in topic
        or "trend" in topic
        or "news" in topic
        or "2026" in topic
    ):
        return "news"

    # Default
    else:
        return "interview"