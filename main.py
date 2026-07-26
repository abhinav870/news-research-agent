from app.graph.builder import graph
from app.schemas.schemas import NewsRequest

request = NewsRequest(
        topic="Artificial Intelligence",
        duration="latest",
        format="long"
)

initial_state = {"request": request}
result = graph.invoke(initial_state)

print(result["markdown_report"])