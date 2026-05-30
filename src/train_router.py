# TODO: 实现训练脚本
import os
import json
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from src.utils import print_separator


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "data", "router_dataset.json")
MODEL_PATH = os.path.join(BASE_DIR, "models", "router_model.pkl")

def load_router_dataset(dataset_path=DATASET_PATH):
    """
        读取 router_dataset.json。

        返回：
        questions: 问题列表
        labels: 标签列表
     """
    if not os.path.exists(dataset_path):
        print("数据集不存在")
        return [],[]

    with open(dataset_path, "r", encoding="utf-8") as f:
        data= json.load(f)

    questions = []
    labels = []

    for item in data:
        question=item.get("question","").strip()
        label=item.get("label","").strip()

        if question and label:
            questions.append(question)
            labels.append(label)

    return questions, labels

def print_dataset_summary(questions, labels):
    """
       打印数据集统计信息。
    """
    print_separator("Router Dataset 统计")
    print(f"\n样本数量: {len(questions)}")

    label_count={}

    for label in labels:
        label_count[label]=label_count.get(label,0)+1

    print("\n各类别数量")

    for label, count in label_count.items():
        print(f"-{label}: {count}")

def build_router_model():
    """
       创建 TF-IDF + SVM Router 分类模型。
    """
    model=Pipeline([
        ("tfidf",TfidfVectorizer(
            analyzer="char",
            ngram_range=(2,4),
        )),
        ("classifier",LinearSVC())])

    return model

def evaluate_model(questions, labels):
    """
       评估 Router 模型。
    """
    print_separator("评估 Router 模型")

    if len(questions)<8:
        print("\n数据集过小，无法评估")
        return

    x_train, x_test, y_train, y_test = train_test_split(
        questions, labels, test_size=0.2, random_state=42, stratify=labels)

    model=build_router_model()
    model.fit(x_train, y_train)
    predictions=model.predict(x_test)
    accuracy=accuracy_score(y_test, predictions)

    print(f"\n测试机准确率：{accuracy:4f}")
    print("\n分类报告")
    print(classification_report(y_test, predictions))

def train_final_model(questions, labels):
    """
        使用全部数据训练最终模型。
    """
    model=build_router_model()
    model.fit(questions, labels)

    return model

def save_model(model, model_path=MODEL_PATH):
    """
        保存模型到 models/router_model.pkl。
    """

    model_dir=os.path.dirname(model_path)
    if model_dir and not os.path.exists(model_dir):
        os.makedirs(model_dir)

    joblib.dump(model, model_path)
    print(f"\n模型保存成功：{model_path}")

if __name__ == "__main__":
    questions, labels = load_router_dataset()
    if len(questions)==0:
        print("数据集为空")
        exit()
    print_dataset_summary(questions, labels)
    evaluate_model(questions, labels)
    final_model=train_final_model(questions, labels)
    save_model(final_model)

