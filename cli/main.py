from playwright.sync_api import sync_playwright
import json
import os
import time
from datetime import datetime


class SessionManager:
    def __init__(self, session_dir="browser_sessions"):
        self.session_dir = session_dir
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)

    def save_session(self, context, session_name):
        """
        Menyimpan session browser ke file
        """
        try:
            # Mendapatkan storage state (cookies dan localStorage)
            storage = context.storage_state()
            
            # Menambahkan timestamp
            storage['timestamp'] = datetime.now().isoformat()
            
            # Menyimpan ke file
            session_path = os.path.join(self.session_dir, f"{session_name}.json")
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(storage, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving session: {str(e)}")
            return False

    def get_session_path(self, session_name):
        """
        Mendapatkan path file session
        """
        return os.path.join(self.session_dir, f"{session_name}.json")

    def is_session_valid(self, session_name, max_age_hours=24):
        """
        Memeriksa apakah session masih valid berdasarkan umur
        """
        try:
            session_path = self.get_session_path(session_name)
            if not os.path.exists(session_path):
                return False
            
            with open(session_path, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            if 'timestamp' not in storage:
                return False
            
            # Memeriksa umur session
            stored_time = datetime.fromisoformat(storage['timestamp'])
            age = datetime.now() - stored_time
            
            return age.total_seconds() < (max_age_hours * 3600)
        except Exception:
            return False

def scrape_with_session(url, session_name="default_session"):
    """
    Penggunaan SessionManager untuk scraping
    """
    session_manager = SessionManager()
    
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        
        # Cek apakah ada session yang valid
        if session_manager.is_session_valid(session_name):
            # Jika ada, gunakan session tersebut
            context = browser.new_context(storage_state=session_manager.get_session_path(session_name))
        else:
            # Jika tidak ada, buat context baru
            context = browser.new_context()
        
        page = context.new_page()
        
        try:
            # Jika tidak ada session valid, lakukan login
            if not session_manager.is_session_valid(session_name):
                print("Session tidak valid atau tidak ada, melakukan login...")

                page.goto(url)
                page.wait_for_timeout(20000)
                page.get_by_text('Accept & Continue').click()
                page.wait_for_timeout(20000)

                session_manager.save_session(context, session_name)
                print("Session baru telah disimpan")
            
            # Lakukan scraping dengan session yang sudah ada
            print(f"Mengakses {url}")
            page.goto(url)
            page.wait_for_timeout(20000)

            accept_button = page.get_by_text('Accept & Continue')
            if accept_button.count() > 0:
                accept_button.click()
            else:
                print("Perizinan accept tidak ditemukan, Lanjut tahap scrolling")

            #fungsi scroll untuk render data
            scroll_container = page.locator('div[data-bdd="qp-split-scroll"]')
            if not scroll_container.count():
                raise Exception("Elemen scroll container tidak ditemukan di halaman.")

            print("Memulai scrolling seperti manusia...")
            previous_count = 0
            start_time = time.time()

            while True:
                # Hitung jumlah elemen saat ini
                current_count = scroll_container.locator('li[data-bdd^="quick-picks-list-item-"]').count()

                if current_count == previous_count and (time.time() - start_time > 10):
                    print("Tidak ada elemen baru selama 10 detik. Scrolling selesai.")
                    break
                elif current_count > previous_count:
                    start_time = time.time() 

                previous_count = current_count
                page.evaluate(
                    """
                    (container) => {
                        container.scrollBy(0, 100);  
                    }
                    """, scroll_container.element_handle()
                )
                page.wait_for_timeout(50)  


            print("Mengambil data tiket...")
            scroll_container = page.locator('ul[data-bdd="quick-picks-list"]')
            tickets = scroll_container.locator('li[data-bdd^="quick-picks-list-item-"]')

            vip_ticket_data = []
            standard_ticket_data = []
            resale_ticket_data = []

            for i in range(tickets.count()):
                try:
                    ticket_element = tickets.nth(i)
                    Vip = False
                    #nama Event
                    name_event = page.locator('h1[class="sc-1eku3jf-14 ghwxrG"]').text_content(timeout=5000).strip()

                    #tanggal Event
                    date_event = page.locator('span[class="sc-1eku3jf-16 dCPMfd"]').text_content(timeout=5000).strip()

                    #lokasi Event
                    location_event = page.locator('a[class="sc-1akkrr6-1 dvPJxG"]').text_content(timeout=5000).strip()  

                    # Lokasi barisan kursi
                    section_locator = ticket_element.locator('span[data-bdd="quick-pick-item-desc"]')
                    section_text = section_locator.text_content(timeout=5000).strip() if section_locator.count() else None
                    
                    # harga
                    price_locator = ticket_element.locator('button[data-bdd="quick-pick-price-button"]')
                    price_text = price_locator.text_content(timeout=5000).strip() if price_locator.count() else None
                   
                    # periksa jenis tiket apakah tiket adalah Resale atau VIP
                    ticket_type_locator = ticket_element.locator('div[data-bdd="branding-ticket-text"] span')
                    vip_locator = ticket_element.locator('div[data-bdd="quick-picks-vip-star-branding"]')
                    resale_locator = ticket_element.locator('span[data-bdd="quick-picks-resale-branding"]')

                    #tahap filterasi untuk ticket
                    if vip_locator.count() > 0:
                        Vip = True
                    if resale_locator.count() > 0:
                        ticket_type = "Verified Resale Ticket" 
                    else:
                        ticket_type = ticket_type_locator.text_content(timeout=5000).strip() if ticket_type_locator.count() else None

                    if (price_text and price_text != "Unknown Price") or (ticket_type and ticket_type != "Unknown Ticket Type"):
                        ticket_info = {
                            "section": section_text if section_text else "Unknown Section",
                            "ticket_type": ticket_type if ticket_type else "Unknown Ticket Type",
                            "price": price_text if price_text else "Unknown Price"
                        }

                        if Vip:
                            vip_ticket_data.append(ticket_info)
                        elif ticket_type == "Verified Resale Ticket":
                            resale_ticket_data.append(ticket_info)
                        else:
                            standard_ticket_data.append(ticket_info)


                except Exception as e:
                    print(f"Error processing ticket: {str(e)}")

            # Gabungkan hasil akhir menjadi satu data
            all_ticket_data = {
                "name_event": name_event,
                "date_event": date_event,
                "location_event": location_event,
                "vip_tickets": vip_ticket_data,
                "standard_tickets": standard_ticket_data,
                "resale_tickets": resale_ticket_data
            }

            # Debugging output
            print("\nData Tiket VIP:")
            for ticket in all_ticket_data["vip_tickets"]:
                print(ticket)

            print("\nData Tiket Standard:")
            for ticket in all_ticket_data["standard_tickets"]:
                print(ticket)

            print("\nData Tiket Resale:")
            for ticket in all_ticket_data["resale_tickets"]:
                print(ticket)

            return all_ticket_data
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return None
        
        finally:
            browser.close()

#mencari harga termurah


#save output
def save_to_json(data,filename="result.json"):
    with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Hasil scraping berhasil disimpan di file {filename}")

# Contoh penggunaan dengan multiple URLs
def main():
    url = input("Masukkan URL: ")
    result = scrape_with_session(url)
    # print(result)
    # if result:
    #     print("Ticket Information:")
    #     print(result['vip_items'])
    #     for ticket in result['ticket_data']:
    #         print(f"Section: {ticket['section']}")
    #         print(f"Ticket Type: {ticket['ticket_type']}")
    #         print(f"Price: {ticket['price']}")
    #         print("-" * 30)
    print('menyimpan Output ke json')
    save_to_json(result)        

if __name__ == "__main__":
    main()