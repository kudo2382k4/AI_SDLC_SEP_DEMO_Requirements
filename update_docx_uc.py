import sys
import docx

doc_path = r"d:\AISDLC\Templates\HSA_Software Requirement Specification_v0.1.docx"
try:
    doc = docx.Document(doc_path)
except Exception as e:
    print(f"Error opening doc: {e}")
    sys.exit(1)

uc_data = [
    # Student
    ("UC01", "Register Course", "Core Infrastructure", "Student selects a course and submits an enrollment request. Awaits payment approval from Operations."),
    ("UC02", "View Course Material", "Course Content Viewer", "Student accesses uploaded PDFs and Video lectures for a particular enrolled course."),
    ("UC03", "Take Phase Mock Exam", "Phase-based Mock Exam", "Student completes an auto-graded assessment assigned to a specific learning phase. Includes MathJax rendering support for formulas."),
    ("UC04", "View Competency Profile", "Analytics & AI", "Student views detailed scores and personalized AI-driven learning recommendations based on their exam attempts."),
    ("UC05", "Submit Q&A Query", "Q&A Messaging", "Student sends a technical or academic question directly to the assigned lecturer."),
    
    # Lecturer
    ("UC06", "Upload Course Materials", "Course Content Viewer", "Lecturer uploads PDF/Video contents into the Cloud Storage and attaches to the course syllabus."),
    ("UC07", "Manage Question Bank", "Phase-based Mock Exam", "Lecturer adds, edits, or archives assessment questions to be randomly generated in mock exams."),
    ("UC08", "Respond to Q&A", "Q&A Messaging", "Lecturer answers pending queries from students within the required SLA timeframe."),
    ("UC09", "View Student Progress", "Analytics Dashboard", "Lecturer checks the learning progress and mock exam scores of students taking their class."),
    
    # Ops Staff
    ("UC10", "Verify Payment Details", "Core Infrastructure", "Operations Staff manually verify and approve offline bank transfers to activate student enrollment."),
    ("UC11", "Configure Course & Phases", "Core Infrastructure", "Operations Staff setup initial course data, define learning phases, and assign corresponding lecturers."),
    
    # Center Director
    ("UC12", "View High-Level Reports", "Analytics Dashboard", "Center Director reviews financial revenue, overall enrollment rates, and lecturer Q&A metrics.")
]

# Find the UC table
target_table = None
for table in doc.tables:
    if len(table.rows) > 0 and len(table.columns) >= 4:
        header_row = table.rows[0].cells
        try:
            if "ID" in header_row[0].text and "Use Case" in header_row[1].text and "Feature" in header_row[2].text:
                target_table = table
                break
        except Exception:
            continue

if target_table:
    # Keep the header, remove other rows
    while len(target_table.rows) > 1:
        row = target_table.rows[1]
        target_table._element.remove(row._element)
    
    # Add new rows
    for i, data in enumerate(uc_data):
        row_cells = target_table.add_row().cells
        row_cells[0].text = data[0]
        row_cells[1].text = data[1]
        row_cells[2].text = data[2]
        row_cells[3].text = data[3]

    try:
        doc.save(doc_path)
        print("Successfully updated UC table.")
    except PermissionError:
        print("PERMISSION_ERROR")
        sys.exit(1)
    except Exception as e:
        print(f"Error saving doc: {e}")
        sys.exit(1)
else:
    print("Could not find appropriate UC table in document.")
    sys.exit(1)
