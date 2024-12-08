def bge_reranker(source_text:str,target_list:list)->float:
    from FlagEmbedding import FlagReranker
    #score取值：-10-10，添加 normalize=True，使用sigmoid转换到0-1之间。
    model_path='/home/tione/notebook/model/a_rerank_model/bge-reranker-v2-m3'
    reranker = FlagReranker(model_path, use_fp16=True,normalize=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
    
    list_text = text2list(source_text,target_list)
    score = reranker.compute_score(list_text)
    print(score)
    return score
def text2list(source_text:str,target_list:list)->list:
    list_text=[]
    for i in target_list:
        sub_list=[source_text,i]
        list_text.append(sub_list)
    return list_text
def xiaobu_embed(source_text:str,target_list:list)->list:
    from sentence_transformers import SentenceTransformer
    source_text = [source_text]
    model_path='/home/tione/notebook/model/a_embeding_model/xiaobu-embedding-v2'
    model = SentenceTransformer(model_path)
    embeddings_1 = model.encode(source_text, normalize_embeddings=True)
    embeddings_2 = model.encode(target_list, normalize_embeddings=True)
    similarity = embeddings_1 @ embeddings_2.T
    print(similarity[0])
    return similarity[0]
def bge_m3_embed(source_text:str,target_list:list)->list:
    from FlagEmbedding import BGEM3FlagModel
    model_path='/home/tione/notebook/model/a_embeding_model/bge-m3'
    model = BGEM3FlagModel(model_path,use_fp16=True) 
    embeddings_1 = model.encode([source_text])['dense_vecs']
    embeddings_2 = model.encode(target_list)['dense_vecs']
    similarity = embeddings_1 @ embeddings_2.T
    print(similarity[0])
    return similarity[0]
def get_top_text(score_list:list,text_list:list,num:int)->list:
    '''
    相关性由高到低
    '''
    # Create a list of tuples (score, text)
    scored_texts = list(zip(score_list, text_list))
    
    # Sort by score in descending order
    sorted_texts = sorted(scored_texts, key=lambda x: x[0], reverse=True)
    
    # Return top num texts
    return [text for _, text in sorted_texts[:num]]
if __name__=='__main__':
    source_text = '我想买房'
    target_list = ['房价上涨','我想在城市中心购买一套公寓','租房不如购房','准备首付','我超能吃']
    s1=bge_reranker(source_text,target_list)
    s2=xiaobu_embed(source_text,target_list)
    s3=bge_m3_embed(source_text,target_list)
    t1=get_top_text(s1,target_list,2)
    t2=get_top_text(s2,target_list,2)
    t3=get_top_text(s3,target_list,2)
    print(s1,s2,s3)
    print(t1,t2,t3)
