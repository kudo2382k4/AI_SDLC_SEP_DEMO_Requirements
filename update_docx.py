import sys
import docx

doc_path = r"d:\AISDLC\Templates\HSA_Software Requirement Specification_v0.1.docx"
try:
    doc = docx.Document(doc_path)
except Exception as e:
    print(f"Error opening doc: {e}")
    sys.exit(1)

actors_data = [
    ("1", "Student", "Primary End-user. Học viên THPT chuẩn bị cho kỳ thi ĐGNL. Tương tác với hệ thống để đăng ký khóa học, học bài giảng (tài liệu/video), làm bài Mock Exam theo giai đoạn, theo dõi kết quả, và gửi câu hỏi Q&A."),
    ("2", "Lecturer", "Key User. Chuyên gia học thuật ký hợp đồng thời vụ. Upload bài giảng, import câu hỏi vào Ngân hàng đề, theo dõi tiến độ Dashboard lớp học, và trực tiếp phản hồi các câu hỏi Q&A từ Học viên."),
    ("3", "Operations Staff", "System Administrator. Nhân viên nội bộ quản lý trung tâm. Xác nhận thanh toán học phí, cấu hình khóa học, thiết lập giai đoạn học, và phân công Giảng viên phụ trách lớp học."),
    ("4", "Center Director", "Project Sponsor. Quản lý cấp cao. Trích xuất báo cáo doanh thu, phân tích số liệu tuyển sinh, hiệu suất hoàn thành khóa học theo giai đoạn, và đánh giá chỉ số SLA tương tác Q&A."),
    ("5", "Parent", "Indirect User. Tác nhân phụ không đăng nhập hệ thống lõi. Nhận email thông báo và xem link báo cáo (Read-only) về kết quả điểm Mock Exam theo giai đoạn của học viên."),
    ("6", "Cloud Storage & CDN", "External System. Hệ thống lưu trữ tài liệu tĩnh (PDF, Video) và phân phối tĩnh chuyên biệt (Render MathJax) để tối ưu tải."),
    ("7", "Notification Service", "External System. Dịch vụ (API) bên thứ 3 phục vụ công tác gửi email xác nhận và push notifications tự động."),
    ("8", "Adaptive AI Engine", "External Engine. Module AI độc lập phân tích dữ liệu làm bài thi từ hệ thống lõi để đưa ra lộ trình/gợi ý ôn tập cá nhân hóa.")
]

target_table = None
for table in doc.tables:
    if len(table.rows) > 0 and len(table.columns) >= 3:
        header_row = table.rows[0].cells
        if "Actor" in header_row[1].text and "Description" in header_row[2].text:
            target_table = table
            break

if target_table:
    # Keep the header, remove other rows
    while len(target_table.rows) > 1:
        row = target_table.rows[1]
        target_table._element.remove(row._element)
    
    # Add new rows
    for i, data in enumerate(actors_data):
        row_cells = target_table.add_row().cells
        row_cells[0].text = data[0]
        row_cells[1].text = data[1]
        row_cells[2].text = data[2]

    try:
        doc.save(doc_path)
        print("Successfully updated Actors table.")
    except PermissionError:
        print("PERMISSION ERROR: File đang được mở trong MS Word. Vui lòng tắt Word và chạy lại.")
        sys.exit(1)
    except Exception as e:
        print(f"Error saving doc: {e}")
        sys.exit(1)
else:
    print("Could not find appropriate Actors table in document.")
    sys.exit(1)
