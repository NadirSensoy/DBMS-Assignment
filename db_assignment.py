import psycopg2
from psycopg2 import sql
from datetime import datetime

# Veritabanı bağlantısı
conn = psycopg2.connect(
    host="localhost",
    database="DB_Assignment",
    user="postgres",
    password="postgres"
)

# Veritabanı üzerinde işlem yapmak için bir imleç oluştur
cur = conn.cursor()

# Veri ekleme
def insert_data(table_name, data):
    columns = data.keys()
    values = [data[column] for column in columns]

    query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(columns))
    )

    cur.execute(query, values)
    conn.commit()

# Veri sorgulama
def select_data(table_name, condition=None):
    query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))

    if condition:
        query += sql.SQL(" WHERE {}").format(condition)

    cur.execute(query)
    return cur.fetchall()

# Veri güncelleme
def update_data(table_name, data, condition):
    set_clause = sql.SQL(', ').join(
        sql.SQL("{} = %s").format(sql.Identifier(column)) for column in data.keys()
    )

    query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
        sql.Identifier(table_name),
        set_clause,
        sql.SQL(condition)
    )

    cur.execute(query, list(data.values()))
    conn.commit()

# Veri silme
def delete_data(table_name, condition):
    query = sql.SQL("DELETE FROM {} WHERE {}").format(
        sql.Identifier(table_name),
        sql.SQL(condition)
    )

    cur.execute(query)
    conn.commit()


def show_all_data(table_name):
    query = sql.SQL("SELECT * FROM {};").format(
        sql.Identifier(table_name)
    )
    cur.execute(query)
    rows = cur.fetchall()

    print(f"\n{table_name} Tablosu:")
    for row in rows:
        print(row)

# Kullanıcı arayüzü
while True:
    print("1. Veri Ekleme")
    print("2. Veri Sorgulama")
    print("3. Veri Güncelleme")
    print("4. Veri Silme")
    print("5. Çıkış")

    choice = input("Yapmak istediğiniz işlemi seçin (1-5): ")

    if choice == '1':
        print("1. Hasta")
        print("2. Doktor")
        print("3. Randevu")
        print("4. Muayene")
        print("5. Hastalik")
        print("6. Tedavi")
        print("7. Ilac")
        print("8. Recete")
        print("9. Laboratuvar Testi")
        print("10. Hastane Personel")
        print("11. Personel Maas")
        print("12. Bolum")
        print("13. Departman")
        print("14. Hastane Donanim")
        print("15. Ameliyat")

        table_choice = input("Hangi tabloya veri eklemek istiyorsunuz? (1-15): ")

        # 1. Hasta Tablosu
        if table_choice == '1':
            table_name = 'hasta'
            data = {
                'ad': input("Ad: "),
                'soyad': input("Soyad: "),
                'dogum_tarihi': input("Doğum Tarihi (YYYY-MM-DD): "),
                'cinsiyet': input("Cinsiyet: "),
                'telefon': input("Telefon: ")
            }
            insert_data(table_name, data)
            print("Hasta verisi eklendi.")

        # 2. Doktor Tablosu
        elif table_choice == '2':
            table_name = 'doktor'
            data = {
                'ad': input("Ad: "),
                'soyad': input("Soyad: "),
                'uzmanlik_alani': input("Uzmanlık Alanı: "),
                'telefon': input("Telefon: ")
            }
            insert_data(table_name, data)
            print("Doktor verisi eklendi.")

        # 3. Randevu Tablosu
        elif table_choice == '3':
            if table_name == 'randevu':
                cur.execute("""
                            INSERT INTO randevu (hasta_id, doktor_id, randevu_tarihi, saat)
                            VALUES (%s, %s, %s, %s)
                        """, (hasta_id, doktor_id, randevu_tarihi, saat))
            elif table_name == 'muayene_randevusu':
                cur.execute("""
                            INSERT INTO muayene_randevusu (hasta_id, doktor_id, randevu_tarihi, saat, muayene_tarihi, muayene_sonucu)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (hasta_id, doktor_id, randevu_tarihi, saat, datetime.now(), muayene_sonucu))
            elif table_name == 'ameliyat_randevusu':
                cur.execute("""
                            INSERT INTO ameliyat_randevusu (hasta_id, doktor_id, randevu_tarihi, saat, ameliyat_tarihi, ameliyat_turu, ameliyat_notu)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (hasta_id, doktor_id, randevu_tarihi, saat, datetime.now(), ameliyat_turu, ameliyat_notu))
            else:
                print("Geçersiz tablo adı.")
            print("Randevu verisi eklendi.")

        # 4. Muayene Tablosu
        elif table_choice == '4':
            table_name = 'muayene'
            data = {
                'randevu_id': input("Randevu ID: "),
                'muayene_tarihi': input("Muayene Tarihi (YYYY-MM-DD): "),
                'muayene_sonucu': input("Muayene Sonucu: ")
            }
            insert_data(table_name, data)
            print("Muayene verisi eklendi.")

        # 5. Hastalik Tablosu
        elif table_choice == '5':
            table_name = 'hastalik'
            data = {
                'hastalik_adi': input("Hastalık Adı: "),
                'aciklama': input("Açıklama: ")
            }
            insert_data(table_name, data)
            print("Hastalık verisi eklendi.")

        # 6. Tedavi Tablosu
        elif table_choice == '6':
            table_name = 'tedavi'
            data = {
                'muayene_id': input("Muayene ID: "),
                'hastalik_id': input("Hastalık ID: "),
                'tedavi_tarihi': input("Tedavi Tarihi (YYYY-MM-DD): "),
                'recete': input("Reçete: ")
            }
            insert_data(table_name, data)
            print("Tedavi verisi eklendi.")

        # 7. Ilac Tablosu
        elif table_choice == '7':
            table_name = 'ilac'
            data = {
                'ilac_adi': input("İlaç Adı: "),
                'dozaj': input("Dozaj: "),
                'birim_fiyat': input("Birim Fiyat: ")
            }
            insert_data(table_name, data)
            print("İlaç verisi eklendi.")

        # 8. Recete Tablosu
        elif table_choice == '8':
            table_name = 'recete'
            data = {
                'muayene_id': input("Muayene ID: "),
                'ilac_id': input("İlaç ID: "),
                'miktar': input("Miktar: ")
            }
            insert_data(table_name, data)
            print("Reçete verisi eklendi.")

        # 9. Laboratuvar Testi Tablosu
        elif table_choice == '9':
            table_name = 'laboratuvar_testi'
            data = {
                'muayene_id': input("Muayene ID: "),
                'test_adi': input("Test Adı: "),
                'sonuc': input("Sonuç: ")
            }
            insert_data(table_name, data)
            print("Laboratuvar Testi verisi eklendi.")

        # 10. Hastane Personel Tablosu
        elif table_choice == '10':
            table_name = 'hastane_personel'
            data = {
                'ad': input("Ad: "),
                'soyad': input("Soyad: "),
                'pozisyon': input("Pozisyon: ")
            }
            insert_data(table_name, data)
            print("Hastane Personel verisi eklendi.")

        # 11. Personel Maas Tablosu
        elif table_choice == '11':
            table_name = 'personel_maas'
            data = {
                'personel_id': input("Personel ID: "),
                'miktar': input("Miktar: "),
                'tarih': input("Tarih (YYYY-MM-DD): ")
            }
            insert_data(table_name, data)
            print("Personel Maaş verisi eklendi.")

        # 12. Bolum Tablosu
        elif table_choice == '12':
            table_name = 'bolum'
            data = {
                'bolum_adi': input("Bölüm Adı: "),
                'bolum_aciklama': input("Bölüm Açıklama: ")
            }
            insert_data(table_name, data)
            print("Bölüm verisi eklendi.")

        # 13. Departman Tablosu
        elif table_choice == '13':
            table_name = 'departman'
            data = {
                'departman_adi': input("Departman Adı: "),
                'sorumlu_personel_id': input("Sorumlu Personel ID: ")
            }
            insert_data(table_name, data)
            print("Departman verisi eklendi.")

        # 14. Hastane Donanim Tablosu
        elif table_choice == '14':
            table_name = 'hastane_donanim'
            data = {
                'donanim_adi': input("Donanım Adı: "),
                'miktar': input("Miktar: ")
            }
            insert_data(table_name, data)
            print("Hastane Donanım verisi eklendi.")

        # 15. Ameliyat Tablosu
        elif table_choice == '15':
            table_name = 'ameliyat'
            data = {
                'hasta_id': input("Hasta ID: "),
                'doktor_id': input("Doktor ID: "),
                'ameliyat_tarihi': input("Ameliyat Tarihi (YYYY-MM-DD): "),
                'ameliyat_turu': input("Ameliyat Türü: "),
                'ameliyat_notu': input("Ameliyat Notu: ")
            }
            insert_data(table_name, data)
            print("Ameliyat verisi eklendi.")

        else:
            print("Geçersiz seçim. Lütfen 1-15 arasında bir sayı seçin.")


    elif choice == '2':

        print("1. Hasta")
        print("2. Doktor")
        print("3. Randevu")
        print("4. Muayene")
        print("5. Hastalik")
        print("6. Tedavi")
        print("7. Ilac")
        print("8. Recete")
        print("9. Laboratuvar Testi")
        print("10. Hastane Personel")
        print("11. Personel Maas")
        print("12. Bolum")
        print("13. Departman")
        print("14. Hastane Donanim")
        print("15. Ameliyat")

        table_choice = input("Hangi tablodan veri sorgulamak istiyorsunuz? (1-15): ")

        # 1. Hasta Tablosu
        if table_choice == '1':
            table_name = 'hasta'
            condition = input("Sorgu koşulunu girin (örneğin: ad = 'John'): ")
            result = select_data(table_name, condition)
            print(result)

        # 2. Doktor Tablosu
        elif table_choice == '2':
            table_name = 'doktor'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 3. Randevu Tablosu
        elif table_choice == '3':
            table_name = 'randevu'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 4. Muayene Tablosu
        elif table_choice == '4':
            table_name = 'muayene'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)


        # 5. Hastalik Tablosu
        elif table_choice == '5':
            table_name = 'hastalik'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 6. Tedavi Tablosu
        elif table_choice == '6':
            table_name = 'tedavi'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 7. Ilac Tablosu
        elif table_choice == '7':
            table_name = 'ilac'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 8. Recete Tablosu
        elif table_choice == '8':
            table_name = 'recete'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 9. Laboratuvar Testi Tablosu
        elif table_choice == '9':
            table_name = 'laboratuvar_testi'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 10. Hastane Personel Tablosu
        elif table_choice == '10':
            table_name = 'hastane_personel'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 11. Personel Maas Tablosu
        elif table_choice == '11':
            table_name = 'personel_maas'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 12. Bolum Tablosu
        elif table_choice == '12':
            table_name = 'bolum'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 13. Departman Tablosu
        elif table_choice == '13':
            table_name = 'departman'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 14. Hastane Donanim Tablosu
        elif table_choice == '14':
            table_name = 'hastane_donanim'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        # 15. Ameliyat Tablosu
        elif table_choice == '15':
            table_name = 'ameliyat'
            condition = input("Sorgu koşulunu girin: ")
            result = select_data(table_name, condition)
            print(result)

        else:

            print("Geçersiz seçim. Lütfen 1-15 arasında bir sayı seçin.")


    # 3. Veri Güncelleme

    elif choice == '3':

        print("1. Hasta")
        print("2. Doktor")
        print("3. Randevu")
        print("4. Muayene")
        print("5. Hastalik")
        print("6. Tedavi")
        print("7. Ilac")
        print("8. Recete")
        print("9. Laboratuvar Testi")
        print("10. Hastane Personel")
        print("11. Personel Maas")
        print("12. Bolum")
        print("13. Departman")
        print("14. Hastane Donanim")
        print("15. Ameliyat")

        table_choice = input("Hangi tabloyu güncellemek istiyorsunuz? (1-15): ")

        if table_choice == '1':
            table_name = 'hasta'
            # Hasta tablosundaki mevcut hasta ID'leri görüntüleme
            existing_hasta_ids = select_data(table_name, "")
            print("Mevcut Hasta ID'leri:")
            for row in existing_hasta_ids:
                print(row[0])
            hasta_id = input("Hangi Hasta ID'yi güncellemek istiyorsunuz?: ")
            condition = f"hasta_id = {hasta_id}"
            data = {
                'ad': input("Yeni Ad: "),
                'soyad': input("Yeni Soyad: "),
                'dogum_tarihi': input("Yeni Doğum Tarihi (YYYY-MM-DD): "),
                'cinsiyet': input("Yeni Cinsiyet: "),
                'telefon': input("Yeni Telefon: ")
            }
            update_data(table_name, data, condition)
            print("Hasta verisi güncellendi.")

        elif table_choice == '2':
            table_name = 'doktor'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'ad': input("Yeni Ad: "),
                'soyad': input("Yeni Soyad: "),
                'uzmanlik_alani': input("Yeni Uzmanlık Alanı: "),
                'telefon': input("Yeni Telefon: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '4':
            table_name = 'muayene'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'randevu_id': input("Yeni Randevu ID: "),
                'muayene_tarihi': input("Yeni Muayene Tarihi (YYYY-MM-DD): "),
                'muayene_sonucu': input("Yeni Muayene Sonucu: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '5':
            table_name = 'hastalik'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'hastalik_adi': input("Yeni Hastalik Adi: "),
                'aciklama': input("Yeni Aciklama: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '6':
            table_name = 'tedavi'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'muayene_id': input("Yeni Muayene ID: "),
                'hastalik_id': input("Yeni Hastalik ID: "),
                'tedavi_tarihi': input("Yeni Tedavi Tarihi (YYYY-MM-DD): "),
                'recete': input("Yeni Recete: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '7':
            table_name = 'ilac'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'ilac_adi': input("Yeni Ilac Adi: "),
                'dozaj': input("Yeni Dozaj: "),
                'birim_fiyat': input("Yeni Birim Fiyat: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '8':
            table_name = 'recete'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'muayene_id': input("Yeni Muayene ID: "),
                'ilac_id': input("Yeni Ilac ID: "),
                'miktar': input("Yeni Miktar: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '9':
            table_name = 'laboratuvar_testi'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'muayene_id': input("Yeni Muayene ID: "),
                'test_adi': input("Yeni Test Adi: "),
                'sonuc': input("Yeni Sonuc: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '10':
            table_name = 'hastane_personel'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'ad': input("Yeni Ad: "),
                'soyad': input("Yeni Soyad: "),
                'pozisyon': input("Yeni Pozisyon: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '11':
            table_name = 'personel_maas'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'personel_id': input("Yeni Personel ID: "),
                'miktar': input("Yeni Miktar: "),
                'tarih': input("Yeni Tarih (YYYY-MM-DD): ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '12':
            table_name = 'bolum'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'bolum_adi': input("Yeni Bolum Adi: "),
                'bolum_aciklama': input("Yeni Bolum Aciklama: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '13':
            table_name = 'departman'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'departman_adi': input("Yeni Departman Adi: "),
                'sorumlu_personel_id': input("Yeni Sorumlu Personel ID: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '14':
            table_name = 'hastane_donanim'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'donanim_adi': input("Yeni Donanim Adi: "),
                'miktar': input("Yeni Miktar: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        elif table_choice == '15':
            table_name = 'ameliyat'
            existing_ids = select_data(table_name, "")
            print(f"Mevcut {table_name} ID'leri:")
            for row in existing_ids:
                print(row[0])
            record_id = input(f"Hangi {table_name} ID'yi güncellemek istiyorsunuz?: ")
            condition = f"{table_name}_id = {record_id}"
            data = {
                'hasta_id': input("Yeni Hasta ID: "),
                'doktor_id': input("Yeni Doktor ID: "),
                'ameliyat_tarihi': input("Yeni Ameliyat Tarihi (YYYY-MM-DD): "),
                'ameliyat_turu': input("Yeni Ameliyat Türü: "),
                'ameliyat_notu': input("Yeni Ameliyat Notu: ")
            }
            update_data(table_name, data, condition)
            print(f"{table_name} verisi güncellendi.")

        else:
            print("Geçersiz seçim. Lütfen 1-15 arasında bir sayı seçin.")


    elif choice == '4':

        print("1. Hasta")
        print("2. Doktor")
        print("3. Randevu")
        print("4. Muayene")
        print("5. Hastalik")
        print("6. Tedavi")
        print("7. Ilac")
        print("8. Recete")
        print("9. Laboratuvar Testi")
        print("10. Hastane Personel")
        print("11. Personel Maas")
        print("12. Bolum")
        print("13. Departman")
        print("14. Hastane Donanim")
        print("15. Ameliyat")

        table_name = input("Veri silmek istediğiniz tablo adını girin (1-15): ")
        show_all_data(table_name)  # Mevcut ID'leri göster
        condition = input(f"\nHangi {table_name} ID'sini silmek istiyorsunuz?: ")
        delete_data(table_name, f"{table_name}_id = {condition}")
        print(f"{table_name} verisi silindi.")


    elif choice == '5':
        break

    else:
        print("Geçersiz seçim. Lütfen 1-5 arasında bir sayı seçin.")

# Bağlantıyı kapat
cur.close()
conn.close()
