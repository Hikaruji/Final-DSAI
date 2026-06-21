"""Smoke tests for search-intent parsing and recommendation quality."""

from app.main import app, lifespan, recommend
from app.models import RecommendRequest
import asyncio

QUERIES = [
    "Beachs in south Viet Nam",
    "beaches in south Vietnam",
    "beach in southern Vietnam",
    "food in Vietnam",
    "historical places in Vietnam",
]


async def main() -> None:
    async with lifespan(app):
        for query in QUERIES:
            response = recommend(RecommendRequest(query=query, top_k=10))
            print("\n" + "=" * 80)
            print(f"Query: {query}")
            print(f"Selected preferences: {response.selected_preferences}")
            print(f"Inferred preferences: {response.inferred_preferences}")
            for idx, result in enumerate(response.recommendations, start=1):
                place = result.place
                print(
                    f"{idx:02d}. {place.name} — {place.location} "
                    f"| score={result.score} | matched={result.matched_labels}"
                )


if __name__ == "__main__":
    asyncio.run(main())
