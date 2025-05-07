import streamlit as st
import pandas as pd
import plotly.express as px
from extractor import SkillExtractor
from matcher import ExpertMatcher
import json
# Removed unused import of datetime

# Initialize components
skill_extractor = SkillExtractor()
expert_matcher = ExpertMatcher()

# Set page config
st.set_page_config(
    page_title="IntelliBridge - Human-AI Expert Matching",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 IntelliBridge")
st.markdown("""
Intelligently match human experts with AI agents based on skills, knowledge areas, and complementarity.
""")

# Sidebar for weights
st.sidebar.header("Matching Preferences")
skill_similarity_weight = st.sidebar.slider(
    "Skill Similarity Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.4,
    step=0.1
)

complementarity_weight = st.sidebar.slider(
    "Complementarity Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.4,
    step=0.1
)

domain_alignment_weight = st.sidebar.slider(
    "Domain Alignment Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)

# Ensure weights sum to 1
total_weight = skill_similarity_weight + \
    complementarity_weight + domain_alignment_weight
if total_weight != 1.0:
    st.sidebar.warning("Weights should sum to 1.0. Please adjust the weights.")

# Main content
tab1, tab2, tab3 = st.tabs(
    ["Upload Profiles", "View Matches", "Feedback & Analytics"])

with tab1:
    st.header("Upload Expert Profiles")

    # Add option to load sample data
    if st.button("Load Sample Data"):
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
            st.session_state.human_profiles = sample_data['human_profiles']
            st.session_state.ai_profiles = sample_data['ai_profiles']
            st.success("Sample data loaded successfully!")

    # Human experts upload
    st.subheader("Human Experts")
    human_profiles = []

    num_humans = st.number_input(
        "Number of Human Experts", min_value=1, max_value=10, value=1)

    for i in range(num_humans):
        with st.expander(f"Human Expert {i+1}"):
            name = st.text_input(f"Name {i+1}")
            bio = st.text_area(f"Bio {i+1}")
            skills = st.text_area(f"Skills (comma-separated) {i+1}")

            if name and bio and skills:
                skills_list = [s.strip() for s in skills.split(",")]
                human_profiles.append({
                    "name": name,
                    "bio": bio,
                    "skills": skills_list
                })

    # AI agents upload
    st.subheader("AI Agents")
    ai_profiles = []

    num_ais = st.number_input("Number of AI Agents",
                              min_value=1, max_value=10, value=1)

    for i in range(num_ais):
        with st.expander(f"AI Agent {i+1}"):
            name = st.text_input(f"AI Name {i+1}")
            description = st.text_area(f"Description {i+1}")
            capabilities = st.text_area(
                f"Capabilities (comma-separated) {i+1}")

            if name and description and capabilities:
                capabilities_list = [c.strip()
                                     for c in capabilities.split(",")]
                ai_profiles.append({
                    "name": name,
                    "description": description,
                    "capabilities": capabilities_list
                })

with tab2:
    st.header("Expert Matches")

    if human_profiles and ai_profiles:
        # Calculate matches
        weights = {
            'skill_similarity': skill_similarity_weight,
            'complementarity': complementarity_weight,
            'domain_alignment': domain_alignment_weight
        }

        matches = expert_matcher.match_experts(
            human_profiles, ai_profiles, weights)

        # Convert matches to DataFrame for display
        matches_df = pd.DataFrame(matches)

        # Display matches
        st.dataframe(
            matches_df[['human', 'ai', 'total_score', 'explanation']],
            use_container_width=True
        )

        # Create heatmap of scores
        st.subheader("Match Score Heatmap")

        # Pivot data for heatmap
        heatmap_data = matches_df.pivot(
            index='human',
            columns='ai',
            values='total_score'
        )

        fig = px.imshow(
            heatmap_data,
            labels=dict(x="AI Agent", y="Human Expert", color="Match Score"),
            color_continuous_scale="Viridis",
            aspect="auto"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display detailed match information
        st.subheader("Detailed Match Information")

        for match in matches:
            with st.expander(f"{match['human']} + {match['ai']}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Total Score:** {match['total_score']:.2f}")
                    st.write(
                        f"**Skill Similarity:** {match['skill_similarity']:.2f}")
                    st.write(
                        f"**Complementarity:** {match['complementarity']:.2f}")
                    st.write(
                        f"**Domain Alignment:** {match['domain_alignment']:.2f}")
                    st.write(
                        f"**Feedback Adjustment:** {match['feedback_adjustment']:.2f}")
                    st.write(f"**Explanation:** {match['explanation']}")

                with col2:
                    st.write("**Provide Feedback**")
                    feedback = st.radio(
                        "How was this match?",
                        ["Positive", "Negative", "Neutral"],
                        key=f"feedback_{match['human']}_{match['ai']}"
                    )

                    if feedback != "Neutral":
                        reason = st.text_area(
                            "Reason for feedback (optional)",
                            key=f"reason_{match['human']}_{match['ai']}"
                        )

                        if st.button("Submit Feedback", key=f"submit_{match['human']}_{match['ai']}"):
                            expert_matcher.add_feedback(
                                match['human'],
                                match['ai'],
                                feedback == "Positive",
                                reason
                            )
                            st.success("Feedback submitted successfully!")
    else:
        st.info(
            "Please upload both human and AI profiles in the 'Upload Profiles' tab.")

with tab3:
    st.header("Feedback & Analytics")

    # Load feedback data
    feedback_data = expert_matcher.feedback_data

    # Display feedback statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Feedback",
            len(feedback_data['positive_matches']) +
            len(feedback_data['negative_matches'])
        )

    with col2:
        st.metric(
            "Positive Matches",
            len(feedback_data['positive_matches'])
        )

    with col3:
        st.metric(
            "Negative Matches",
            len(feedback_data['negative_matches'])
        )

    # Display skill weights
    st.subheader("Skill Weights Based on Feedback")

    if feedback_data['skill_weights']:
        skill_weights_df = pd.DataFrame(
            list(feedback_data['skill_weights'].items()),
            columns=['Skill', 'Weight']
        ).sort_values('Weight', ascending=False)

        fig = px.bar(
            skill_weights_df,
            x='Skill',
            y='Weight',
            title='Skill Weights from Feedback'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(
            "No skill weights available yet. Provide feedback on matches to build this data.")

    # Display recent feedback
    st.subheader("Recent Feedback")

    all_feedback = (
        feedback_data['positive_matches'] +
        feedback_data['negative_matches']
    )

    if all_feedback:
        feedback_df = pd.DataFrame(all_feedback)
        feedback_df['timestamp'] = pd.to_datetime(feedback_df['timestamp'])
        feedback_df = feedback_df.sort_values('timestamp', ascending=False)

        for _, row in feedback_df.head(5).iterrows():
            with st.expander(f"{row['human']} + {row['ai']} ({row['timestamp'].strftime('%Y-%m-%d %H:%M')})"):
                st.write(
                    f"**Type:** {'Positive' if row.name < len(feedback_data['positive_matches']) else 'Negative'}")
                if row['reason']:
                    st.write(f"**Reason:** {row['reason']}")
    else:
        st.info(
            "No feedback available yet. Provide feedback on matches to see them here.")
