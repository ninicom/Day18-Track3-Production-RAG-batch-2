# Failure Analysis

Dựa trên kết quả từ `ragas_report.json`, dưới đây là phân tích bottom-5 câu hỏi có điểm trung bình (average score) thấp nhất, kèm theo chẩn đoán (diagnosis) và giải pháp đề xuất (suggested_fix).

| Câu hỏi | Metric tệ nhất | Điểm trung bình | Chẩn đoán (Diagnosis) | Giải pháp đề xuất (Suggested Fix) |
|---|---|---|---|---|
| Nhân viên thử việc được nghỉ mấy ngày? | `context_recall` | 0.25 | Missing relevant chunks | Improve chunking or add BM25 |
| Chính sách mật khẩu VPN là gì? | `faithfulness` | 0.35 | LLM hallucinating | Tighten prompt, lower temperature |
| Khi nào phải bàn giao thiết bị IT? | `context_precision` | 0.40 | Too many irrelevant chunks | Add reranking or metadata filter |
| Báo cáo tài chính quý 1 ở đâu? | `answer_relevancy` | 0.45 | Answer doesn't match question | Improve prompt template |
| Công ty hỗ trợ tiền gửi xe không? | `context_recall` | 0.50 | Missing relevant chunks | Improve chunking or add BM25 |

*(Lưu ý: Bảng này là mẫu định dạng. Khi chạy thành công `pipeline.py`, các câu hỏi và điểm số thực tế sẽ được trích xuất từ test set)*
