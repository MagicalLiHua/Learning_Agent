# import weaviate
#
# # 使用 with 语句，离开缩进区间后会自动调用 client.close()
# with weaviate.connect_to_local(
#         host="10.160.108.2",
#         port=8080,
#         grpc_port=50051,
# ) as client:
#     print(f"连接状态: {client.is_ready()}")
#
# # 此时连接已安全关闭，不会报 Warning


import weaviate

client = weaviate.connect_to_local(
    host="10.160.108.2",
    port=8080,
    grpc_port=50051,
)

print(client.is_ready())

client.collections.create("Database")

database = client.collections.get("Database")
uuid = database.data.insert(
    properties={
        "segment_id": "1000",
        "document_id": "1",
    },
    # 复制生成1536维向量
    vector=[0.12345] * 1536
)

print(uuid)