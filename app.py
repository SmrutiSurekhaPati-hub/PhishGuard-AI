import streamlit as st
from predictor import analyze_message
from url_analyzer import analyze_url


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------

st.title("🛡️ PhishGuard AI")
st.subheader("Multilingual AI-Powered Phishing Detection & Awareness")

st.write(
    "Analyze suspicious messages and URLs using machine learning "
    "and explainable security indicators."
)

st.divider()


# -----------------------------
# Message Analysis
# -----------------------------

st.header("📩 Message / Email Analysis")

message = st.text_area(
    "Paste a suspicious message or email here:",
    height=180,
    placeholder="Example: Urgent! Your account will be blocked. Click the link immediately..."
)


if st.button("🔍 Analyze Message", use_container_width=True):

    if not message.strip():

        st.warning("Please enter a message to analyze.")

    else:

        prediction, confidence = analyze_message(message)

        st.subheader("Analysis Result")

        if prediction == "phishing":

            st.error("🚨 Potential Phishing Detected")

        else:

            st.success("✅ Likely Legitimate")

        st.metric(
            "Model Confidence",
            f"{confidence:.2f}%"
        )

        st.info(
            "This result is an AI-based assessment and should be "
            "used as a security warning, not as a guarantee."
        )


st.divider()


# -----------------------------
# URL Analysis
# -----------------------------

st.header("🔗 URL Security Analysis")

url = st.text_input(
    "Enter a URL to analyze:",
    placeholder="https://example.com"
)


if st.button("🛡️ Analyze URL", use_container_width=True):

    if not url.strip():

        st.warning("Please enter a URL.")

    else:

        result = analyze_url(url)

        st.subheader("URL Analysis Result")

        # Threat level
        if result["threat_level"] == "High Risk":

            st.error("🚨 High Risk URL")

        elif result["threat_level"] == "Suspicious":

            st.warning("⚠️ Suspicious URL")

        else:

            st.success("✅ Low Risk URL")

        # Risk score
        st.metric(
            "Risk Score",
            f"{result['score']} / 100"
        )

        # Indicators
        if result["risk_points"]:

            st.subheader("⚠️ Detected Indicators")

            for point in result["risk_points"]:

                st.write("•", point)

        else:

            st.info(
                "No obvious suspicious indicators were detected."
            )


st.divider()


# -----------------------------
# Safety Recommendations
# -----------------------------

st.header("🔐 Safety Recommendations")

recommendations = [
    "Do not click suspicious links.",
    "Never share passwords, OTPs, PINs, or banking details.",
    "Verify the sender through an official communication channel.",
    "Check the website address carefully before entering information.",
    "Be cautious of urgent threats, unexpected rewards, and unusual requests."
]

for recommendation in recommendations:

    st.write("•", recommendation)


# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "PhishGuard AI | Omnikon National Hackathon 2026 | "
    "Prototype for phishing detection and user awareness"
)