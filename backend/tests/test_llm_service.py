from backend.services.llm_services import LLMService

service = LLMService()

response = service.generate_response(
    "Explain SOLID principles in 50 words."
)

print(response)