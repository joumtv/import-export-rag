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

    if top_score >= 0.60:
        return {
            "level": "HIGH",
            "should_answer": True,
            "score": top_score,
            "message": "Strong relevant evidence was found."
        }

    elif top_score >= 0.40:
        return {
            "level": "MEDIUM",
            "should_answer": True,
            "score": top_score,
            "message": "Some relevant information was found. Human verification is recommended."
        }

    else:
        return {
            "level": "LOW",
            "should_answer": False,
            "score": top_score,
            "message": "The available evidence is not strong enough to answer reliably."
        }