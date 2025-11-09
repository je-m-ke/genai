import streamlit as st #type: ignore

# Title
st.title("🧮 Simple Math Calculator")

# Description
st.write("Perform addition, subtraction, multiplication, or division between two numbers.")

# --- Input section ---
col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("Enter first number", value=0.0, step=1.0)
with col2:
    num2 = st.number_input("Enter second number", value=0.0, step=1.0)

# --- Operator selection ---
operation = st.selectbox(
    "Select operation",
    ("Add", "Subtract", "Multiply", "Divide")
)

# --- Action button ---
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
    elif operation == "Subtract":
        result = num1 - num2
    elif operation == "Multiply":
        result = num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            st.error("Cannot divide by zero!")
            st.stop()
        result = num1 / num2

    # Display result
    st.success(f"Result: {result}")

# Footer
st.caption("Built with Streamlit 🚀")

