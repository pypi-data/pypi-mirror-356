from difflib import get_close_matches
def find_similar(package: str, known_packages: list[str], threshold: float = 0.7) -> list[str]:
    return get_close_matches(package, known_packages, n=3, cutoff=threshold)