import base64
import os
from PIL import Image, ImageDraw, ImageFont
import io

def generate_circle_icon(color, size, text, text_color):
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, size-1, size-1), fill=color)
    
    # Try to load a font, otherwise fallback
    try:
        font = ImageFont.truetype("arial.ttf", int(size*0.6))
    except:
        font = ImageFont.load_default()
        
    # Draw text (checkmark or bell)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((size-w)/2, (size-h)/2 - int(size*0.1)), text, fill=text_color, font=font)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_gradient_line(width, height):
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    for i in range(width):
        r = int(249 - (249-168) * (i/width))
        g = int(115 - (115-85) * (i/width))
        b = int(22 - (22-247) * (i/width))
        draw.line([(i, 0), (i, height)], fill=(r, g, b))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# 1. Main large checkmark (light green bg, dark green check)
checkmark_large_b64 = generate_circle_icon((220, 252, 231), 100, "v", (16, 185, 129))

# 2. Logo image
logo_path = r'C:\Users\sanja\OneDrive\Desktop\codestorm\website\static\website\images\logo.jpg'
with open(logo_path, 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode('utf-8')
    
# 3. Gradient line
gradient_b64 = generate_gradient_line(1000, 4)

html = f"""<!DOCTYPE html>
<html>
<head>
<style>
    @page {{
        size: a4 portrait;
        margin: 2cm;
    }}
    body {{
        font-family: Helvetica, Arial, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
    }}
    .outer-table {{
        width: 100%;
        border: 1px solid #e2e8f0;
        border-radius: 8px; /* May not work fully, but safe fallback */
    }}
    .header-table {{
        width: 100%;
        padding: 20px 20px 10px 20px;
    }}
    .header-left {{
        width: 25%;
        text-align: center;
        vertical-align: middle;
    }}
    .header-right {{
        width: 75%;
        border-left: 1px solid #e2e8f0;
        padding-left: 20px;
        vertical-align: middle;
    }}
    .college-name {{
        color: #4a196e;
        font-size: 16px;
        font-weight: bold;
        line-height: 1.2;
    }}
    .college-sub {{
        color: #475569;
        font-size: 9px;
        line-height: 1.2;
        margin-top: 4px;
    }}
    .content {{
        padding: 40px;
        text-align: center;
    }}
    .title {{
        color: #0f172a;
        font-size: 26px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }}
    .desc {{
        color: #475569;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 30px;
    }}
    .team-name {{
        color: #4338ca;
        font-weight: bold;
    }}
    .box-green {{
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
        color: #166534;
        font-weight: bold;
        font-size: 13px;
    }}
    .box-purple {{
        background-color: #f5f3ff;
        padding: 15px;
        text-align: left;
        color: #334155;
        font-size: 12px;
        line-height: 1.5;
    }}
    .footer {{
        border-top: 1px solid #e2e8f0;
        padding: 15px 40px;
        font-size: 11px;
        color: #64748b;
        line-height: 1.4;
    }}
</style>
</head>
<body>
    <table class="outer-table" cellpadding="0" cellspacing="0">
        <tr>
            <td>
                <!-- Header -->
                <table class="header-table" cellpadding="0" cellspacing="0">
                    <tr>
                        <td class="header-left">
                            <img src="data:image/jpeg;base64,{logo_b64}" width="70" />
                        </td>
                        <td class="header-right">
                            <div class="college-name">NARSIMHA REDDY<br/>ENGINEERING COLLEGE</div>
                            <div class="college-sub">An Autonomous Institution | Affiliated to JNTUH | Approved by AICTE<br/>Accredited by NBA & NAAC with 'A' Grade</div>
                        </td>
                    </tr>
                </table>
                
                <!-- Gradient Line -->
                <img src="data:image/png;base64,{gradient_b64}" width="100%" height="3" style="display:block; margin: 10px 0;" />
                
                <!-- Main Content -->
                <div class="content">
                    <img src="data:image/png;base64,{checkmark_large_b64}" width="80" height="80" />
                    
                    <div class="title">Registration Successful!</div>
                    <div class="desc">
                        Your team <span class="team-name">{{{{ team_name }}}}</span> has been successfully registered for<br/>
                        <span class="team-name">CodeStorm 2K26</span>. Get ready for the ultimate 36-hour<br/>
                        hackathon challenge!
                    </div>
                    
                    <div class="box-green">
                        v &nbsp; Team registration confirmed
                    </div>
                    
                    <div class="box-purple">
                        <strong style="color: #4c1d95;">Next Steps:</strong> Keep an eye on your email for further updates about the hackathon schedule and venue details.
                        <br/><br/>
                        Join WhatsApp Group: <a href="{{{{ whatsapp_link }}}}" style="color: #4338ca;">{{{{ whatsapp_link }}}}</a>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <strong>This is an auto-generated confirmation.</strong><br/>
                    For any queries, please contact our support team.
                </div>
            </td>
        </tr>
    </table>
</body>
</html>"""

out_path = r'C:\Users\sanja\OneDrive\Desktop\codestorm\website\templates\website\pdf_receipt.html'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Template successfully written!")
