import numpy as np
import hanlp
from kmeans_pytorch import kmeans
from transformers import AutoTokenizer, AutoModel
import torch
from pathlib import Path

# 检查 GPU 是否可用
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"使用设备: {device}")

# 加载官方中文句子边界检测模型
sent_model = hanlp.load('UD_CTB_EOS_MUL', devices=0 if device == 'cuda' else -1)
model_path = Path(r"C:\Users\Lenovo\Desktop\rj").resolve()
model_id_str = model_path.as_posix()

# 加载 tokenizer 和模型
tokenizer = AutoTokenizer.from_pretrained(model_id_str, local_files_only=True)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32,
    local_files_only=True
).to(device)


def split_into_sentences(text: str):
    return sent_model(text)


def get_embeddings(sentences):
    # 构建 instruct 格式
    instruct = "Given a document, retrieve relevant passages."
    texts = [f"Instruct: {instruct}\nQuery: {s}" for s in sentences]

    with torch.no_grad():
        inputs = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        outputs = model(**inputs)
        # 最后一个 token 的 hidden state 作为 embedding
        embeddings = outputs.last_hidden_state[:, -1, :]

    # 保持在 GPU 上，但转换为 float32 以支持后续计算
    return embeddings.to(torch.float32)

def cluster_sentences(sentences, embeddings, n_clusters=None):
    n = len(sentences)
    n_clusters = n_clusters or min(4, n)          # 2. 簇数 ≤ 句子数
    n_clusters = max(2, n_clusters)

    embeddings = embeddings.to(device)
    cluster_ids, cluster_centers = kmeans(
        X=embeddings,
        num_clusters=n_clusters,
        distance='euclidean',
        device=device,
    )

    # 确保中心点也在 GPU 上
    cluster_centers = cluster_centers.to(device)

    # 找到距离中心最近的句子索引
    closest_indices = []
    for i in range(n_clusters):
        mask = (cluster_ids == i).to(device)
        cluster_emb = embeddings[mask]
        center = cluster_centers[i].unsqueeze(0)

        # 计算距离并找到最近的句子
        dist = torch.cdist(center, cluster_emb).squeeze(0)
        closest_in_cluster = torch.argmin(dist).item()

        # 映射回原始句子索引
        global_idx = torch.where(mask)[0][closest_in_cluster].item()
        closest_indices.append(global_idx)

    closest_indices.sort()

    # 根据中心点分割文本
    segments = []
    start_index = 0

    for idx in closest_indices[1:]:
        segment = " ".join(sentences[start_index:idx])
        segments.append(segment)
        start_index = idx

    # 添加最后一段
    segment = " ".join(sentences[start_index:])
    segments.append(segment)

    return segments

def find_optimal_clusters_pytorch(embeddings: torch.Tensor, max_k=10):
    # 确保所有计算在同一设备上进行
    embeddings = embeddings.to(device)
    inertias = []
    k_range = range(2, min(max_k, embeddings.size(0)) + 1)

    for k in k_range:
        cluster_ids, centers = kmeans(
            X=embeddings,
            num_clusters=k,
            distance='euclidean',
            device=device
        )

        # 确保中心点在正确设备上
        centers = centers.to(device)

        # 计算惯性（所有点到其最近中心的距离平方和）
        dists = torch.cdist(embeddings, centers)
        inertia = dists.min(dim=1).values.pow(2).sum().item()
        inertias.append(inertia)

    # 肘部法则（仅标量数组）
    inertias = np.array(inertias)
    d1 = np.diff(inertias)
    d2 = np.diff(d1)

    return np.argmax(d2) + 2 if len(d2) else 3


def semantic_text_segmentation(text, n_clusters=None, level=2):
    sentences = split_into_sentences(text)
    if len(sentences) <= 1:
        return [text]

    embeddings = get_embeddings(sentences)

    # 第一次粗分
    coarse = cluster_sentences(sentences, embeddings, n_clusters)

    if level >= 2 and len(coarse) > 1:
        fine = []
        for seg in coarse:
            seg_sents = split_into_sentences(seg)
            if len(seg_sents) <= 2:          # 太短的段不再拆
                fine.append(seg)
                continue
            seg_emb = get_embeddings(seg_sents)
            fine.extend(cluster_sentences(seg_sents, seg_emb, n_clusters))
        return fine

    return coarse


def main():
    """一句话模式：输入一行文本，立即分段"""
    print("文本语义聚类分段工具（一行模式）")
    print("请输入要分段的文本（输入'quit'退出）：")

    while True:
        text = input("\n>>> ").strip()
        if text.lower() == "quit":
            break
        if not text:
            print("输入为空，请重新输入。")
            continue

        try:
            segments = semantic_text_segmentation(text)
            print("\n分段结果：")
            print("-" * 50)
            for i, segment in enumerate(segments, 1):
                print(f"段落 {i}: {segment}")
                print("-" * 30)
        except Exception as e:
            print(f"处理过程中出现错误: {e}")


if __name__ == "__main__":
    main()