# import sys
# import os
# sys.path.append(os.path.abspath("."))
#
# from kynex import Kynex
# #
# # if __name__ == "__main__":
# #     prompt =""
# #     response = Kynex.get_llm_response(prompt, model_name="gemini-1.5-flash")
# #     print("\n🔹 Response:\n", response)
#
# from kynex import Kynex
#
# if __name__ == "__main__":
#     prompt = """
# You are an AI assistant supporting sprint planning by generating technical software use cases.
#
# Given the role of a Backend Developer, generate exactly **10 well-defined use cases** in the following strict JSON format:
#
# [
#   {
#     "uc_id": 1,
#     "uc_name": "A concise, technically impactful use case title (avoid vague or generic names)",
#     "uc_desc": "A clear, realistic technical or business challenge relevant to the role. Describe the problem being solved, its significance, and its relevance to the domain.",
#     "required_tools": "Python, FastAPI, MySQL, (include any additional essential tools relevant to the role, but ensure the tool stack is consistent across all 10 use cases — do NOT include any BI tools)",
#     "final_delivarables": "Comma-separated list of expected technical outputs such as APIs, models, scripts, configurations, reports, etc."
#   },
#   ...
# ]
#
# Guidelines:
# - Output must be a valid flat JSON array containing exactly 10 use case objects.
# - Do NOT include markdown or code block formatting (no ```json).
# - `uc_name` must be professional, domain-relevant, and specific (e.g., “Automated Loan Approval Engine” instead of “Finance App”).
# - `required_tools` and `final_delivarables` must be plain comma-separated strings — not arrays.
# - Maintain consistent tools (e.g., Python, FastAPI, MySQL) across all entries, unless the role explicitly requires variation.
# - Respond with only the JSON — no explanations, headers, or comments.
# """
#
#     model_name = "gemini-1.5-flash"
#
#     response = Kynex.get_llm_response(prompt, model_name)
#     print("\n🔹 Use Case Output:\n")
#     print(response)


from kynex import Kynex

if __name__ == "__main__":
    # Simulated input from frontend
    request = {
        "prompt": "You are an AI assistant helping define technical software use cases...",
        "model_name": "gemini-1.5-flash",
        "api_key": "AIzaSyDUpvgVl5S686AFUdKgWq3EL5WvJU7yivk"
        # Note: No llm_type sent from frontend
    }

    response = Kynex.get_llm_response(
        prompt=request["prompt"],
        model_name=request["model_name"],
        api_key=request["api_key"],
        #llm_type=request.get("llm_type")  # Can be None — will default to gemini
        llm_type = Kynex.LLM_GEMINI
    )

    print("\n🔹 Response:\n")
    print(response)
