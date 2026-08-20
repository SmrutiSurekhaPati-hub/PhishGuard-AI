from urllib.parse import urlparse


def analyze_url(url):
    """
    Analyze a URL for common suspicious characteristics.
    """

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)

    risk_points = []
    score = 0

    # 1. HTTPS check
    if parsed.scheme != "https":
        risk_points.append("URL does not use HTTPS.")
        score += 15

    # 2. IP address instead of domain name
    hostname = parsed.hostname or ""

    parts = hostname.split(".")

    if hostname.replace(".", "").isdigit():
        risk_points.append("URL uses an IP address instead of a normal domain name.")
        score += 25

    # 3. Suspicious words
    suspicious_words = [
        "login",
        "verify",
        "secure",
        "account",
        "update",
        "confirm",
        "password",
        "bank",
        "reward",
        "claim",
        "free"
    ]

    url_lower = url.lower()

    found_words = [
        word for word in suspicious_words
        if word in url_lower
    ]

    if found_words:
        risk_points.append(
            "Contains potentially suspicious keywords: "
            + ", ".join(found_words)
        )
        score += min(len(found_words) * 5, 25)

    # 4. Excessive subdomains
    if len(parts) > 4:
        risk_points.append("URL contains an unusually large number of subdomains.")
        score += 15

    # 5. Very long URL
    if len(url) > 100:
        risk_points.append("URL is unusually long.")
        score += 10

    # 6. @ symbol
    if "@" in url:
        risk_points.append("URL contains '@', which can be used to disguise the destination.")
        score += 20

    # Limit score
    score = min(score, 100)

    # Threat level
    if score >= 60:
        threat_level = "High Risk"
    elif score >= 30:
        threat_level = "Suspicious"
    else:
        threat_level = "Low Risk"

    return {
        "score": score,
        "threat_level": threat_level,
        "risk_points": risk_points
    }


if __name__ == "__main__":

    print("=" * 50)
    print("PHISHGUARD AI - URL ANALYZER")
    print("=" * 50)

    url = input("\nEnter a URL to analyze: ")

    result = analyze_url(url)

    print("\nThreat Level:", result["threat_level"])
    print("Risk Score:", result["score"], "/ 100")

    if result["risk_points"]:
        print("\nDetected Indicators:")

        for point in result["risk_points"]:
            print("-", point)

    else:
        print("\nNo obvious suspicious indicators detected.")