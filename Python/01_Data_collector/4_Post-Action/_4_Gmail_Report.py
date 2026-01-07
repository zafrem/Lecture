import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import _1_technical_analysis_Stochastic as stochastic
import os

smtp_server = "smtp.gmail.com"
smtp_port = 587
username = "your_email@gmail.com"
password = "your_password"

from_address = "your_email@gmail.com"  # Send email
to_address = "recipient_email@example.com"  # Recv email

# MIME email Create
message = MIMEMultipart()
message['From'] = from_address
message['To'] = to_address
message['Subject'] = "Stochastic Report"

# Main text
body = "This is main body - Stochanstic Report plantext.."
message.attach(MIMEText(body, 'plain'))

# attach Image
screenshop_file_name = 'stochastic_report.png'

if os.path.exists(screenshop_file_name):
    os.remove(screenshop_file_name)

df = stochastic.init_pre_df()
plt, df = stochastic.stochastic(df)
plt.savefig(screenshop_file_name, bbox_inches='tight')

fp = open(screenshop_file_name, 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

msgImage.add_header('Content-ID', '<image1>')
msgImage.add_header('Content-Disposition', 'inline', filename=os.path.basename(screenshop_file_name))
msgImage.add_header("Content-Transfer-Encoding", "base64")
message.attach(msgImage)

os.remove(screenshop_file_name)

# attach File
attach_file = open('stochastic_report.docx','rb')
attach_mime = MIMEBase('application','octet-stream')
attach_mime.set_payload((attach_file).read())
encoders.encode_base64(attach_mime)
message.add_header('Content-Disposition', "attachment; filename= " + "stochastic_report.docx")
message.attach(attach_mime)

# SMTP Server connection and Send mail
server = smtplib.SMTP(smtp_server, smtp_port)
try:
    server.starttls()  # TLS(Transport Layer Security)
    server.login(username, password)  # login
    server.send_message(message)  # Send Mail
    print("Success")
except Exception as e:
    print(f"Fail: {e}")
finally:
    server.quit()  # SMTP Terminate