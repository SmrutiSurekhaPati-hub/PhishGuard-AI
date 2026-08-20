import joblib
import re

# ============================================================
# PhishGuard AI - Multilingual Message Analyzer
# ============================================================

MODEL_PATH = "models/phishing_model.joblib"

# Load the trained machine-learning model
model = joblib.load(MODEL_PATH)


# ============================================================
# Multilingual phishing keywords
# ============================================================

PHISHING_KEYWORDS = {

    # -------------------------
    # English
    # -------------------------
    "english": [
        "urgent",
        "verify",
        "verification",
        "verify your account",
        "account suspended",
        "account blocked",
        "account locked",
        "click here",
        "click the link",
        "login",
        "password",
        "otp",
        "one time password",
        "bank account",
        "credit card",
        "debit card",
        "confirm your identity",
        "security alert",
        "winner",
        "won a prize",
        "claim now",
        "limited time",
        "act now",
        "update your account",
        "confirm your account",
        "reset your password",
        "payment failed",
        "payment pending",
        "refund",
        "free reward",
        "suspended",
        "immediately"
    ],

    # -------------------------
    # Hindi
    # -------------------------
    "hindi": [
        "तुरंत",
        "सत्यापित",
        "सत्यापन",
        "खाता",
        "खाता बंद",
        "खाता निलंबित",
        "खाता लॉक",
        "क्लिक करें",
        "लिंक पर क्लिक",
        "पासवर्ड",
        "ओटीपी",
        "बैंक खाता",
        "बैंक",
        "पहचान सत्यापित",
        "जानकारी अपडेट",
        "इनाम",
        "पुरस्कार",
        "जीत गए",
        "अभी दावा करें",
        "तुरंत कार्रवाई",
        "भुगतान विफल",
        "भुगतान लंबित",
        "पैसे",
        "वापसी",
        "सुरक्षा चेतावनी",
        "खाता सत्यापित"
    ],

    # -------------------------
    # Odia
    # -------------------------
    "odia": [
        "ତୁରନ୍ତ",
        "ଯାଞ୍ଚ",
        "ସତ୍ୟାପନ",
        "ଖାତା",
        "ଖାତା ବନ୍ଦ",
        "ଖାତା ଲକ୍",
        "ଖାତା ନିଲମ୍ବିତ",
        "ଲିଙ୍କରେ କ୍ଲିକ୍",
        "କ୍ଲିକ୍ କରନ୍ତୁ",
        "ପାସୱାର୍ଡ",
        "ଓଟିପି",
        "ବ୍ୟାଙ୍କ",
        "ବ୍ୟାଙ୍କ ଖାତା",
        "ପରିଚୟ ଯାଞ୍ଚ",
        "ସୂଚନା ଅପଡେଟ",
        "ପୁରସ୍କାର",
        "ଇନାମ",
        "ଜିତିଛନ୍ତି",
        "ଦାବି କରନ୍ତୁ",
        "ଭୁଗତାନ ବିଫଳ",
        "ଭୁଗତାନ ବାକି",
        "ସୁରକ୍ଷା ସତର୍କତା",
        "ଖାତା ଯାଞ୍ଚ"
    ]
}


# ============================================================
# Detect language/script
# ============================================================

def detect_language(message):
    """
    Detect the likely language/script of the message.
    This is a lightweight script-based detector.
    """

    # Odia Unicode range
    odia_characters = re.findall(r"[\u0B00-\u0B7F]", message)

    # Devanagari Unicode range used by Hindi
    hindi_characters = re.findall(r"[\u0900-\u097F]", message)

    if len(odia_characters) >= 2:
        return "odia"

    if len(hindi_characters) >= 2:
        return "hindi"

    return "english"


# ============================================================
# Multilingual phishing keyword analysis
# ============================================================

def multilingual_phishing_score(message):
    """
    Calculate a lightweight phishing risk score based on
    multilingual security keywords.

    Returns:
        score: 0-100
        matched_keywords: list
    """

    text = message.lower()

    matched_keywords = []

    # Search all supported languages
    for language, keywords in PHISHING_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                if keyword not in matched_keywords:
                    matched_keywords.append(keyword)

    # Calculate score
    number_of_matches = len(matched_keywords)

    if number_of_matches == 0:
        score = 0

    elif number_of_matches == 1:
        score = 25

    elif number_of_matches == 2:
        score = 45

    elif number_of_matches == 3:
        score = 65

    elif number_of_matches == 4:
        score = 80

    else:
        score = 90

    # URLs inside messages increase suspicion
    if re.search(r"https?://|www\.", text):

        score = min(100, score + 15)

    # Email-style urgency
    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "तुरंत",
        "ଏବେ",
        "ତୁରନ୍ତ"
    ]

    for word in urgency_words:

        if word.lower() in text:

            score = min(100, score + 10)
            break

    return score, matched_keywords


# ============================================================
# Main analyzer
# ============================================================

def analyze_message(message):
    """
    Analyze a message using:

    1. Existing trained ML model
    2. Multilingual phishing keyword analysis
    3. URL/urgency indicators

    Returns:
        prediction: 'phishing' or 'legitimate'
        confidence: percentage
    """

    message = str(message).strip()

    if not message:
        return "legitimate", 0.0

    # --------------------------------------------------------
    # Existing ML model prediction
    # --------------------------------------------------------

    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]

    class_names = model.classes_

    probability_map = dict(zip(class_names, probabilities))

    model_confidence = probability_map[prediction] * 100


    # --------------------------------------------------------
    # Multilingual analysis
    # --------------------------------------------------------

    language = detect_language(message)

    multilingual_score, matched_keywords = multilingual_phishing_score(
        message
    )


    # --------------------------------------------------------
    # Convert model result into phishing probability
    # --------------------------------------------------------

    phishing_probability = 0.0

    if "phishing" in probability_map:

        phishing_probability = probability_map["phishing"] * 100

    elif "spam" in probability_map:

        phishing_probability = probability_map["spam"] * 100

    else:

        # If the model uses another positive class name,
        # fall back to its prediction.
        if str(prediction).lower() == "phishing":
            phishing_probability = model_confidence
        else:
            phishing_probability = 100 - model_confidence


    # --------------------------------------------------------
    # Combine ML + multilingual analysis
    # --------------------------------------------------------

    # The trained ML model remains the primary signal.
    # Multilingual analysis acts as an additional security layer.

    combined_phishing_probability = (
        (phishing_probability * 0.60)
        + (multilingual_score * 0.40)
    )


    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------

    if combined_phishing_probability >= 50:

        final_prediction = "phishing"

        final_confidence = combined_phishing_probability

    else:

        final_prediction = "legitimate"

        final_confidence = 100 - combined_phishing_probability


    # --------------------------------------------------------
    # Confidence cleanup
    # --------------------------------------------------------

    final_confidence = max(50.0, min(99.0, final_confidence))


    return final_prediction, final_confidence


# ============================================================
# Standalone testing
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PHISHGUARD AI - MULTILINGUAL MESSAGE ANALYZER")
    print("=" * 60)

    message = input("\nEnter a message to analyze: ")

    prediction, confidence = analyze_message(message)

    language = detect_language(message)

    risk_score, matched_keywords = multilingual_phishing_score(message)

    print("\nLanguage:", language)

    print("\nResult:")

    if prediction == "phishing":
        print("🚨 Potential Phishing Detected")
    else:
        print("✅ Likely Legitimate")

    print(f"Confidence: {confidence:.2f}%")

    print(f"Multilingual Risk Score: {risk_score}/100")

    if matched_keywords:

        print("\nDetected suspicious keywords:")

        for keyword in matched_keywords:
            print("-", keyword)

    print("\n" + "=" * 60)