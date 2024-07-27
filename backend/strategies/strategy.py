from abc import abstractmethod, ABC
import smtplib
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class Strategy(ABC):
    
    def add_ta(self, data):
        pass
    
    def buy_signal(self):
        pass
    
    def sell_signal(self):
        pass
    
    def format_alert(self):
        self.buy_signal()
        buys = self.prices[self.prices['buy_signal']==True]
        buys = buys[buys['Date'] >= (datetime.now() - timedelta(days=7))] # need to only make this current day
        buys = buys[['Date', 'Ticker']] # need to add current price here as we
        
        message_lines = []
        for _, row in buys.iterrows():
            message_lines.append(f"Ticker: {row['Ticker']}, Date: {row['Date'].strftime('%Y-%m-%d')}")
        
        return message_lines
        
        
    def send_alert(self):
        HOST = os.getenv('EMAIL_HOST')
        PORT = os.getenv('EMAIL_PORT')
        FROM_EMAIL = os.getenv("FROM_EMAIL")
        TO_EMAIL = os.getenv('EMAIL_LIST').split(',')
        PASSWORD = os.getenv('EMAIL_PASSWORD')

        MESSAGE = self.format_alert()
        MESSAGE = "\n".join(MESSAGE)
        email_message = f"From: {FROM_EMAIL}\nTo: {', '.join(TO_EMAIL)}\nSubject: Portfolio Alert\n\n{MESSAGE}"

        try:
            smtp = smtplib.SMTP(HOST, PORT)
            status_code, response = smtp.ehlo()
            print(f"[*] Echoing the server: {status_code} {response}")

            status_code, response = smtp.starttls()
            print(f"[*] Starting TLS connection: {status_code} {response}")

            status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
            print(f"[*] Logging in: {status_code} {response}")

            for recipient in TO_EMAIL:
                smtp.sendmail(FROM_EMAIL, recipient.strip(), email_message)

            smtp.quit()
            print("[*] Email(s) sent successfully!")
        
        except Exception as e:
            print(f"[!] Error sending email: {e}")