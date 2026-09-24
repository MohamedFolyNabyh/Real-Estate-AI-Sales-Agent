# from langchain_core.messages import HumanMessage

# from app.graph import graph


# config = {
#     "configurable": {
#         "thread_id": "customer_2"
#     }
# }


# while True:

#     user_input = input("\nYou: ")

#     if user_input.lower() == "exit":
#         break

#     result = graph.invoke(
#         {
#             "messages": [
#                 HumanMessage(content=user_input)
#             ]
#         },
#         config=config
#     )

#     final_message = result["messages"][-1]

#     print("\nAgent:")
#     print(final_message.content)