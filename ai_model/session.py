class ChatSession:
    def __init__(self, model):
        self._chat_session = model.start_chat_session()

    def send_prompt(self, elements):
        # Print elements for debugging
        print("Elements sent to prompt:", elements)

        # Rebuild prompt with improved format and double-check clarity
        prompt = (
            "Hi, you are a chemistry assistant bot.\n"
            "Your job is to provide information about a chemical compound given its elements.\n"
            f"The elements provided are: {', '.join(elements)}.\n"
            "Please provide the following details ONLY if a known and valid compound can be formed:\n"
            "{Formula: {'elements': <chemical formula>, name: <name>, uses: <uses>, properties: <properties>}}\n"
            "IMPORTANT: If the elements do not form a valid, recognized chemical compound,"
            " respond with EXACTLY this statement:\n"
            "Status Code: 418. I am not equipped with such information please ask - Mr. Mohit Ryan\n"
            "Do not attempt to guess or provide information for unknown compounds."
        )

        try:
            response = self._chat_session.send_message(prompt)
            print("Response text received:", response.text)  # Print raw response for debugging

            expected_error_message = ("Status Code: 418. I am not equipped with such information please ask -"
                                      " Mr. Mohit Ryan")

            if response.text.strip() == expected_error_message:
                return expected_error_message
            if response.text.strip().startswith("{Formula:"):
                return response.text.strip()

            # If response doesn't fit expected formats, return the error message
            return expected_error_message

        except Exception as e:
            return f"An error occurred: {str(e)}"
