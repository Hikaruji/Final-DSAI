#!/usr/bin/env python3
"""Quick smoke test for location-aware recommendation queries."""

from app.data_loader import PLACES
from app.location_resolver import is_location_only_query
from app.ml_intent import infer_preferences
from app.nlp_parser import parse_query, preferences_from_parsed_query
from app.ranking import rank
from app.recommender import PlaceIndex


def run_query(query: str, top_k: int = 5) -> None:
    parsed = parse_query(query)
    location = parsed["location"]
    location_only = is_location_only_query(query, location) if location else False
    parser_preferences = preferences_from_parsed_query(parsed)

    if query and not location_only:
        inferred_preferences, label_probabilities = infer_preferences(query)
    else:
        inferred_preferences, label_probabilities = [], {}

    ml_preferences = [] if parser_preferences else inferred_preferences
    preferences = list(dict.fromkeys(parser_preferences + ml_preferences))

    index = PlaceIndex(PLACES)
    candidates = index.top_k_similar(query, k=len(PLACES) if location else 80)
    results = rank(
        candidates=candidates,
        preferences=preferences,
        query_location=location,
        top_k=top_k,
        has_query=bool(query),
        label_probabilities=label_probabilities if ml_preferences else {},
    )

    print("=" * 80)
    print(f"Query: {query}")
    print(f"Parsed location: {location!r} | location-only: {location_only}")
    print(f"Parser preferences: {parser_preferences} | ML preferences: {inferred_preferences}")
    print("Top recommendations:")
    for i, result in enumerate(results, start=1):
        place = result.place
        print(f"{i}. {place.name} — {place.location} — score={result.score}")


if __name__ == "__main__":
    for sample_query in [
        "Hoi An",
        "places near Hoi An",
        "beach near Hoi An",
        "market Ho Chi Minh city",
        "Sapa",
    ]:
        run_query(sample_query)
