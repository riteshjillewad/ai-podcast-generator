def choose_music(topic):

    topic = topic.lower()

    if "ai" in topic or "technology" in topic or "future" in topic:
        return "assets/music/futuristic.wav"

    elif "motivation" in topic or "success" in topic:
        return "assets/music/upbeat.wav"

    elif "business" in topic or "finance" in topic:
        return "assets/music/corporate.wav"

    elif "story" in topic or "mystery" in topic:
        return "assets/music/cinematic.wav"

    else:
        return "assets/music/standard.wav"