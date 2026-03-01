from endee import Endee, Precision

client = Endee()

# Create index
client.create_index(
    name="rag_index",
    dimension=384,
    space_type="cosine",
    precision="int8d"
)