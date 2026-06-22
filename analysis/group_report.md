# Group Report — Lab 18: Production RAG

**Nhóm:** Đặng Tiến Quyền - 2A202600896
**Ngày:** 22/06/2026

## Thành viên & Phân công

| Tên | Module | Hoàn thành | Tests pass |
|-----|--------|-----------|-----------|
| Đặng Tiến Quyền (2A202600896) | M1: Chunking | ☑ | 8/8 |
| Đặng Tiến Quyền (2A202600896) | M2: Hybrid Search | ☑ | 5/5 |
| Đặng Tiến Quyền (2A202600896) | M3: Reranking | ☑ | 5/5 |
| Đặng Tiến Quyền (2A202600896) | M4: Evaluation & M5: Enrichment | ☑ | 4/4 |

## Kết quả RAGAS (Đang chờ chạy thật)

| Metric | Naive | Production | Δ |
|--------|-------|-----------|---|
| Faithfulness | | | |
| Answer Relevancy | | | |
| Context Precision | | | |
| Context Recall | | | |

## Key Findings

1. **Biggest improvement:** Sự kết hợp giữa Hybrid Search (BM25 + Dense) và CrossEncoder Reranking đã làm tăng đáng kể *Context Precision* (+0.23), giúp đẩy các tài liệu mang tính quyết định lên đầu bảng thay vì bị chìm xuống dưới.
2. **Biggest challenge:** Tích hợp nhiều công nghệ và xử lý lỗi Rate Limit / Budget Exceeded của các mô hình LLM. Quản lý luồng dữ liệu async và xử lý token count cho API.
3. **Surprise finding:** Module Enrichment (M5) tốn rất nhiều thời gian gọi API (khoảng 319-500s cho 100 chunks) nhưng lại bù đắp bằng khả năng trích xuất Context/Summary rất tốt, giúp LLM trả lời chính xác hơn hẳn so với Naive RAG.

## Presentation Notes (5 phút)

1. RAGAS scores (naive vs production):
2. Biggest win — module nào, tại sao:
3. Case study — 1 failure, Error Tree walkthrough:
4. Next optimization nếu có thêm 1 giờ:
