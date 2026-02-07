import streamlit as st
from agents import GeneratorAgent, ReviewerAgent

st.set_page_config(page_title="AI Agent Assessment", layout="centered")

st.title("🤩 AI Agent Assessment")

# User Input

grade = st.number_input("Grade", min_value=1, max_value=12, value=4)
topic = st.text_input("Topic", value="Types of angles")

if st.button("Run Agent Pipeline"):

    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    input_json = {
        "grade": grade,
        "topic": topic
    }

    # Generator

    st.markdown("## 🧠 Generator Output")

    generator_output = generator.generate(input_json)

    st.markdown("### Explanation")
    st.write(generator_output["explanation"])

    if generator_output["mcqs"]:
        st.markdown("### MCQs")
        for i, mcq in enumerate(generator_output["mcqs"], 1):
            st.markdown(f"**Q{i}. {mcq['question']}**")
            for option in mcq["options"]:
                st.write(f"- {option}")
            st.write(f"✅ Correct Answer: **{mcq['answer']}**")
            st.write("")
    else:
        st.write("No questions generated.")

    #  Reviewer

    st.markdown("## 🔎 Reviewer Output")

    reviewer_output = reviewer.review(generator_output, grade)

    if reviewer_output["status"] == "pass":
        st.success("Status: PASS")
    else:
        st.error("Status: FAIL")

    if reviewer_output["feedback"]:
        st.markdown("### Feedback:")
        for item in reviewer_output["feedback"]:
            st.write(f"- {item}")

    # Refinement 
 
    refined_output = None
    final_review = reviewer_output

    if reviewer_output["status"] == "fail":

        st.markdown("## 🔁 Refinement Pass")

        refined_output = generator.generate(
            input_json,
            feedback=reviewer_output["feedback"]
        )

        st.markdown("### Refined Explanation")
        st.write(refined_output["explanation"])

        # Re-review after refinement
        final_review = reviewer.review(refined_output, grade)

        if final_review["status"] == "pass":
            st.success("Final Status After Refinement: PASS")
        else:
            st.error("Final Status After Refinement: FAIL")

   
    # JSON 
    
    st.markdown("---")
    st.markdown("## 📦 Structured JSON Outputs (For Review)")

    st.markdown("### Generator Output (JSON)")
    st.json(generator_output)

    st.markdown("### Reviewer Output (JSON)")
    st.json(reviewer_output)

    if refined_output:
        st.markdown("### Refined Output (JSON)")
        st.json(refined_output)

        st.markdown("### Final Reviewer Output After Refinement (JSON)")
        st.json(final_review)

 
st.markdown("---")
st.markdown(
    "Made with ❤️ by **Arnav** ~ "
)