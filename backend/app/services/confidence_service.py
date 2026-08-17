def evaluate_confidence(search_results: list):

    if not search_results:
        return {
            "level": "LOW",
            "should_answer": False,
            "score": 0,
            "message": "No relevant information was found."
        }

    # Get the highest similarity score
    top_score = search_results[0]["score"]

    # HIGH confidence
    if top_score >= 0.75:
        return {
            "level": "HIGH",
            "should_answer": True,
            "score": top_score,
            "message": "Strong relevant evidence was found."
        }

    # MEDIUM confidence
    elif top_score >= 0.60:
        return {
            "level": "MEDIUM",
            "should_answer": True,
            "score": top_score,
            "message": "Relevant information was found, but human verification is recommended."
        }

    # LOW confidence
    else:
        return {
            "level": "LOW",
            "should_answer": False,
            "score": top_score,
            "message": "The available evidence is not strong enough to answer reliably."
        }