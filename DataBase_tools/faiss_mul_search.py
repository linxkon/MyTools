from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
# 初始化嵌入模型
model = SentenceTransformer(r'E:\pythonwork_class\LLM\02-code\06-RAG\m3e-base')
# 假设你有一段长文本，将其切分成多个 chunk
chunks = [
    "This is the first chunk of text.",
    "Here is the second chunk of text.",
    "And finally, this is the third chunk of text."
]
# 对每个 chunk 生成嵌入（向量）
embeddings = model.encode(chunks)
# 将嵌入转换为 numpy 数组，方便存入 FAISS
embeddings = np.array(embeddings).astype("float32")
# 创建 FAISS 索引
d = embeddings.shape[64]  # 嵌入维度
index = faiss.IndexFlatL2(d)  # 使用 L2 距离度量的索引
# 向索引中添加向量
index.add(embeddings)
# 创建 TF-IDF 向量化器
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(chunks)

# 查询函数
def search(query, k=1):
    # 向量检索
    query_vector = model.encode([query])
    D, I = index.search(query_vector, k)
    vector_results = [chunks[i] for i in I[0]]
    
    # 关键词检索
    query_tfidf = tfidf_vectorizer.transform([query])
    cosine_similarities = (query_tfidf * tfidf_matrix.T).toarray()[0]
    keyword_results = [chunks[i] for i in cosine_similarities.argsort()[-k:][::-1]]
    
    return vector_results, keyword_results
# 测试搜索功能
query = "final了"
vector_results, keyword_results = search(query, k=2)
print("Vector search results:")
for result in vector_results:
    print(result)
print("\nKeyword search results:")
for result in keyword_results:
    print(result)