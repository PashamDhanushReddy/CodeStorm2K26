import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codestorm_project.settings')
django.setup()

from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io

html_content = """
<!DOCTYPE html>
<html>
<head>
<style>
    @page {
        size: a4 portrait;
        margin: 2cm;
    }
    body {
        font-family: Helvetica, Arial, sans-serif;
        color: #1e293b;
    }
    .card {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 0;
    }
    .header-table {
        width: 100%;
        padding: 20px;
    }
    .header-left {
        width: 25%;
        text-align: center;
    }
    .header-right {
        width: 75%;
        border-left: 2px solid #e2e8f0;
        padding-left: 20px;
    }
    .college-name {
        color: #4a196e;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .college-sub {
        color: #475569;
        font-size: 10px;
    }
    .gradient-line {
        background-color: #a855f7;
        height: 3px;
        width: 100%;
    }
    .content {
        padding: 40px;
        text-align: center;
    }
    .success-icon {
        width: 80px;
        height: 80px;
        background-color: #f0fdf4;
        border: 1px solid #dcfce3;
        border-radius: 40px;
        margin: 0 auto 20px auto;
        text-align: center;
        line-height: 80px;
        font-size: 40px;
        color: #10b981;
    }
    .title {
        color: #0f172a;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .desc {
        color: #475569;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 30px;
    }
    .team-name {
        color: #4338ca;
        font-weight: bold;
    }
    .box-green {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
        color: #166534;
        font-weight: bold;
    }
    .box-purple {
        background-color: #f5f3ff;
        border: 1px solid #ede9fe;
        border-radius: 10px;
        padding: 15px;
        text-align: left;
        color: #334155;
    }
    .footer {
        border-top: 1px solid #e2e8f0;
        padding: 20px 40px;
        font-size: 12px;
        color: #64748b;
    }
</style>
</head>
<body>
    <div class="card">
        <table class="header-table">
            <tr>
                <td class="header-left">
                    <!-- Placeholder for logo -->
                    <div style="font-size: 40px; color: #f97316;">&#127795;</div>
                    <div style="font-size: 12px; font-weight: bold; color: #4a196e;">NRCM</div>
                </td>
                <td class="header-right">
                    <div class="college-name">NARSIMHA REDDY<br/>ENGINEERING COLLEGE</div>
                    <div class="college-sub">An Autonomous Institution | Affiliated to JNTUH | Approved by AICTE<br/>Accredited by NBA & NAAC with 'A' Grade</div>
                </td>
            </tr>
        </table>
        
        <div class="gradient-line"></div>
        
        <div class="content">
            <div class="success-icon">&#10003;</div>
            <div class="title">Registration Successful!</div>
            <div class="desc">
                Your team <span class="team-name">pandas33</span> has been successfully registered for<br/>
                <span class="team-name">CodeStorm 2K26</span>. Get ready for the ultimate 36-hour<br/>
                hackathon challenge!
            </div>
            
            <div class="box-green">
                &#10003; &nbsp; Team registration confirmed
            </div>
            
            <div class="box-purple">
                <strong style="color: #4c1d95;">Next Steps:</strong> Keep an eye on your email for further updates about the hackathon schedule and venue details.
            </div>
        </div>
        
        <div class="footer">
            <strong>This is an auto-generated confirmation.</strong><br/>
            For any queries, please contact our support team.
        </div>
    </div>
</body>
</html>
"""

pdf_file = io.BytesIO()
pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_file)
if not pisa_status.err:
    with open('test_receipt.pdf', 'wb') as f:
        f.write(pdf_file.getvalue())
    print("PDF generated successfully: test_receipt.pdf")
else:
    print("Error generating PDF")
