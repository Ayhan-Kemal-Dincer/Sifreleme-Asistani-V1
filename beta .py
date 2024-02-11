import random
import string
import sqlite3

class PasswordManager:
    def __init__(self):
        self.conn = sqlite3.connect("passwords.db")
        self.cursor = self.conn.cursor()
        self.create_database()

    def create_database(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                              (website TEXT, username TEXT, password TEXT)''')
        self.conn.commit()

    def generate_secure_password(self, length=12, require_digits=True, require_special_chars=True):
        if length < 8 or length > 16:
            raise ValueError("Şifre uzunluğu en az 8 karakter ve en fazla 16 karakter olmalı")

        characters = string.ascii_letters
        if require_digits:
            characters += string.digits
        if require_special_chars:
            characters += string.punctuation

        secure_password = ''.join(random.choice(characters) for i in range(length))
        return secure_password

    def save_password(self, website, username, password):
        self.cursor.execute("INSERT INTO passwords VALUES (?, ?, ?)", (website, username, password))
        self.conn.commit()

    def get_password(self, website, username):
        self.cursor.execute("SELECT password FROM passwords WHERE website=? AND username=?", (website, username))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    def list_websites(self):
        self.cursor.execute("SELECT DISTINCT website FROM passwords")
        websites = self.cursor.fetchall()
        return [website[0] for website in websites]

    def close_connection(self):
        self.conn.close()

def main():
    manager = PasswordManager()
    
    while True:
        print("\nŞifre Yönetimi Menüsü:")
        print("1. Yeni Şifre Oluştur")
        print("2. Şifre Kaydet")
        print("3. Şifre Görüntüle")
        print("4. Kayıtlı Siteleri Listele")
        print("5. Çıkış")

        choice = input("Seçiminizi Girin: ")

        if choice == "1":
            try:
                length = int(input("Şifre Uzunluğunu Belirtin: "))
                if length < 8 or length > 16:
                    raise ValueError("Hata: Şifre uzunluğu en az 8 karakter ve en fazla 16 karakter olmalıdır.")
                
                require_digits = input("Rakamlar içermesi gerekiyor mu? (Evet/Hayır): ").lower() == "evet"
                require_special_chars = input("Özel karakterler içermesi gerekiyor mu? (Evet/Hayır): ").lower() == "evet"
                password = manager.generate_secure_password(length, require_digits, require_special_chars)
                print("Oluşturulan Güvenli Şifre:", password)
            except ValueError as e:
                print(str(e))
                continue

        elif choice == "2":
            try:
                website = input("Web sitesi adı: ")
                username = input("Kullanıcı adı: ")
                password = input("Şifre: ")
                manager.save_password(website, username, password)
                print("Şifre kaydedildi.")
            except Exception as e:
                print("Hata: Şifre kaydedilemedi -", str(e))

        elif choice == "3":
            try:
                website = input("Web sitesi adı: ")
                username = input("Kullanıcı adı: ")
                password = manager.get_password(website, username)
                if password:
                    print("Şifre:", password)
                else:
                    print("Şifre bulunamadı.")
            except Exception as e:
                print("Hata: Şifre görüntülenemedi -", str(e))

        elif choice == "4":
            websites = manager.list_websites()
            print("Kayıtlı Siteler:")
            for website in websites:
                print(website)

        elif choice == "5":
            print("Çıkış yapılıyor.")
            break

if __name__ == "__main__":
    main()