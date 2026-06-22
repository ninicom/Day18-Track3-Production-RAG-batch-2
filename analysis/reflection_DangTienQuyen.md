# Báo cáo Phân tích & Suy ngẫm (Reflection) - Production RAG
**Học viên:** Đặng Tiến Quyền
**Mã HV:** 2A202600896

---

## Phần 1: Mapping bài giảng

| Lecture Concept | Module | Hàm cụ thể | Observation |
|----------------|--------|-------------|-------------|
| Semantic chunking | M1 | `chunk_semantic()` | Threshold 0.85 tạo các chunks bảo toàn ý nghĩa câu tốt hơn so với basic chunking, không cắt ngang các đoạn mô tả chi tiết quy định. |
| Hierarchical chunking | M1 | `chunk_hierarchical()` | Tạo ra `parent_size` 2048 và `child_size` 256 giúp tăng độ chính xác tìm kiếm (retrieval qua child chunks) nhưng giữ trọn bối cảnh trả về (thông qua `parent_id`). |
| BM25 + Dense fusion | M2 | `reciprocal_rank_fusion()` | Kết hợp keyword search (hiệu quả với từ vựng tiếng Việt đặc thù qua `underthesea`) và semantic search bằng `bge-m3`. RRF giúp đưa ra các doc relevant nhất lên top 1-2. |
| Cross-encoder reranking | M3 | `CrossEncoderReranker.rerank()` | Rerank với mô hình `bge-reranker-v2-m3` tối ưu đáng kể thứ hạng (top 3) so với dot-product/cosine cơ bản. Latency khoảng 10-30ms cho mỗi doc. |
| RAGAS 4 metrics | M4 | `evaluate_ragas()` | Context precision có phần thấp với naive baseline nhưng cải thiện nhờ Hybrid Search và Rerank. |
| Contextual embeddings | M5 | `contextual_prepend()`, `_enrich_single_call()` | Bổ sung summary, HyQA, và auto-metadata trước khi embedding giúp tránh sai sót và thiếu sót về ngữ cảnh. |

## Phần 2: Khó khăn & giải quyết

- **Khó khăn lớn nhất:**
  1. Tokenizer của BM25 và segmentation tiếng Việt (`underthesea`) chưa khớp nhau ở các từ nối (VD: `nghỉ_phép` thay vì `nghỉ phép`), làm BM25 không truy xuất được kết quả khi tìm chuỗi tách biệt.
  2. Giao tiếp với Qdrant Client gặp lỗi `ConnectionError` khi không có môi trường Docker chạy Qdrant daemon.
- **Cách debug & giải quyết:**
  1. Sử dụng `.replace("_", " ")` sau khi `word_tokenize()` của `underthesea` để bảo đảm chuỗi được BM25 phân rã đúng đắn.
  2. Sử dụng try/except bắt lỗi kết nối và dự phòng bằng `QdrantClient(location=":memory:")` để tiếp tục thực thi khi Docker Desktop chưa sẵn sàng.
- **Thời gian debug:** Khoảng 10-15 phút. Kiến thức cần bổ sung là các tham số cấu hình nâng cao của Qdrant-Client và Rank-BM25 cho ngôn ngữ có dấu.

## Phần 3: Action Plan cho project

### Project: Hệ thống tư vấn nội quy và chính sách nội bộ

### Hiện tại
- RAG pipeline hiện tại: Naive Pipeline (cắt đoạn theo ký tự, tìm kiếm Dense Vector thuần tuý).
- Known issues: Thỉnh thoảng bị hiện tượng hallucination khi truy vấn câu hỏi có từ khóa hẹp nhưng ngữ cảnh trải dài, Context Precision chưa cao dẫn đến context nhồi nhét.

### Plan áp dụng
1. [x] **Chunking strategy:** Hierarchical chunking. Nó cho phép truy vấn nhanh và chính xác vào từ khoá nhưng gửi LLM nguyên một đoạn bối cảnh đầy đủ.
2. [x] **Search:** Hybrid Search (BM25 + BAAI/bge-m3). BM25 là cốt lõi cho các thuật ngữ nhân sự/viết tắt, kết hợp Dense để hiểu ý đồ ngữ nghĩa.
3. [x] **Reranking:** Có sử dụng, model `BAAI/bge-reranker-v2-m3`. Chi phí latency 50-100ms nhưng cải thiện Precision vượt bậc.
4. [x] **Evaluation:** RAGAS (sử dụng 4 metrics cốt lõi: faithfulness, answer relevancy, context precision, context recall).
5. [x] **Enrichment:** Sử dụng Single-call LLM để tạo metadata và summary đồng thời nhằm tối ưu API cost thay vì gọi 4 prompt riêng biệt.

### Timeline
- Tuần 1: Setup Qdrant & Implement Module 1 (Chunking) & 2 (Hybrid).
- Tuần 2: Áp dụng Cross-Encoder Reranking và thiết lập Enriched data pipeline (HyQA + Metadata).
- Tuần 3: Build Test Set (30-50 Q&A) -> Chạy RAGAS, Failure Analysis và tinh chỉnh.
