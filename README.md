# Đề tài 3 – Phân loại tin nhắn rác (SMS Spam)

Bài tập lớn học phần **Nhập môn Học máy** (năm học 2026–2027). Phân loại tin nhắn thành `spam`/`ham`
bằng **BoW / TF-IDF** + **Multinomial Naive Bayes**, **K-NN**, **Cây quyết định**.

## Kết quả chính (tập test, lớp spam; n = 1035, 131 spam)

| Mô hình | Precision | Recall | F1 | FP | FN |
|---|---|---|---|---|---|
| Multinomial NB – baseline (raw + BoW, mặc định) | 0.952 | 0.901 | 0.925 | 6 | 13 |
| K-NN – baseline (raw + BoW, k=5, euclidean) | 1.000 | 0.267 | 0.422 | 0 | 96 |
| Decision Tree – baseline | 0.900 | 0.893 | 0.897 | 13 | 14 |
| **Multinomial NB – tinh chỉnh** (BoW, α=0.1) | 0.933 | 0.954 | **0.943** | 9 | 6 |
| K-NN – tinh chỉnh (TF-IDF, cosine, k=11) | 0.967 | 0.908 | 0.937 | 4 | 12 |
| Decision Tree – tinh chỉnh (gini, depth=10) | 0.967 | 0.901 | 0.933 | 4 | 13 |

> **Lưu ý trung thực:** khoảng tin cậy bootstrap của ba mô hình tinh chỉnh chồng lấn và NB baseline đã tương đương
> trên nhiều lần chia dữ liệu, nên không kết luận một mô hình thắng tuyệt đối. Xem báo cáo, Mục 4.6.

## Cấu trúc

```
README.md  requirements.txt  AI_USAGE.md  run_all.sh  app.py
data/            SMSSpamCollection (không commit; xem bên dưới)
src/             data.py, models.py, eda.py, experiments.py, error_analysis.py,
                 make_report_tables.py, report_utils.py, predict.py
notebooks/       spam_classification.ipynb (chạy từng ô: EDA → mô hình → lỗi → dự đoán)
results/         figures/, tables/, logs/   (sinh bởi run_all.sh)
models/          *.joblib (mô hình đã huấn luyện)
report/          report.tex, report.pdf, figures/, tables/
```

## Dữ liệu

SMS Spam Collection v.1 (Almeida & Gómez Hidalgo, 2011), UCI ML Repository, giấy phép CC BY 4.0:
<https://archive.ics.uci.edu/dataset/228/sms+spam+collection>. Giải nén `sms_spam_collection.zip`
và đặt tệp `SMSSpamCollection` vào `data/`. Tệp mã hóa `latin-1`.

## Chạy lại

```bash
pip install -r requirements.txt
./run_all.sh                  # EDA -> thí nghiệm -> phân tích lỗi (~10 phút trên 1 CPU)
cd report && xelatex report.tex && xelatex report.tex
```

`random_state = 42` cho chia dữ liệu (80/20, phân tầng), 5-fold CV và Cây quyết định.
Môi trường đã dùng: Python 3.12.3, scikit-learn 1.8.0, pandas 3.0.2.

## Notebook (Jupyter / Anaconda)

```bash
jupyter notebook notebooks/spam_classification.ipynb
```
Chạy từng ô theo thứ tự. Mặc định dùng kết quả đã lưu; đặt `RUN_FULL = True` (mục 5) để huấn luyện lại (~10 phút).

## Demo

```bash
python src/predict.py "WINNER!! You have won a £1000 prize. Call 09061701461 to claim"
python src/predict.py --model knn --threshold 0.9 "see you at lunch?"
streamlit run app.py
```

## Thiết kế chống data leakage

- Loại 403 tin trùng văn bản **trước** khi chia (không có cặp trùng bị gán nhãn mâu thuẫn).
- Vectorizer/scaler nằm trong `sklearn.Pipeline`, chỉ fit trên train (kể cả trong từng fold CV).
- Siêu tham số và ngưỡng chọn bằng CV/out-of-fold trên train; test chỉ dùng để báo cáo.

## Phân công nhóm

| Thành viên | MSSV | Phần việc |
|---|---|---|
| _(điền)_ | _(điền)_ | _(vd: EDA, tiền xử lý)_ |
| _(điền)_ | _(điền)_ | _(vd: mô hình, thí nghiệm)_ |
| _(điền)_ | _(điền)_ | _(vd: báo cáo, demo)_ |

Khai báo sử dụng AI: xem [`AI_USAGE.md`](AI_USAGE.md).
