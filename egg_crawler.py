import os
import sys
import subprocess

# 1. 자동 필수 부품(Selenium) 설치 시스템 (초보자용 편의)
try:
    import selenium
except ImportError:
    print("⚙️ Selenium 부품이 없습니다. 로봇이 스스로 자동 설치를 시작합니다...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    import selenium

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json
from urllib.request import Request, urlopen

def fetch_real_prices():
    print("🤖 [V2 크롤러 가동] 이마트 실시간 접속을 시도합니다 (Chrome 브라우저 위장 모드)")
    
    # 2. 브라우저 설정 (감지 회피 및 백그라운드 실행)
    options = Options()
    options.add_argument('--headless') # 화면 없이 몰래 실행
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    crawled_data = []
    
    try:
        driver = webdriver.Chrome(options=options)
        
        target_url = "https://emart.ssg.com/search.ssg?target=all&query=%EA%B3%84%EB%9E%80+30%EA%B5%AC"
        print(f"🔗 접속 목표: {target_url}")
        driver.get(target_url)
        
        time.sleep(3) # 브라우저 로딩 대기 3초
        
        page_src = driver.page_source
        # 3. 이마트 보안(Akamai) 차단 여부 검사
        if "Access Denied" in page_src or "You don't have permission" in page_src:
             print("🚨 [비상 사태] 이마트 보안망(Akamai 방어막)이 깃허브 서버 IP를 봇으로 감지하고 차단했습니다!!")
             driver.quit()
             return crawled_data

        print("✅ [접속 성공] 보안망 강행 돌파 성공! 실제 가격 추출을 시작합니다.")
        
        # 4. 가격 데이터 리얼타임 추출
        price_elements = driver.find_elements(By.CSS_SELECTOR, "em.ssg_price")
        
        if not price_elements:
            print("❌ 상품 목록이나 가격표를 화면에서 찾지 못했습니다.")
        else:
            first_price_text = price_elements[0].text
            clean_price = int(first_price_text.replace(',', '').strip())
            print(f"🎉 성공적으로 실제 최저가를 찾아냈습니다: {clean_price}원")
            
            # 테스트를 위해 가격이 확실히 바뀌는 것 확인 (역삼점 1개)
            mart_data = {
                "id": "seoul-0",
                "region": "seoul",
                "name": "이마트 역삼점 (리얼 데이터 성공결과)",
                "lat": 37.4999,
                "lng": 127.0376,
                "price": clean_price,
                "stock": "재고 있음",
                "address": "역삼로 310",
                "updated": time.strftime("%m월 %d일 %H:%M")
            }
            crawled_data.append(mart_data)
            
        driver.quit()
        
    except Exception as e:
        print(f"❌ [에러 발생] 크롤링 조종 중 작동 문제가 발생했습니다: {e}")
        
    return crawled_data

def upload_to_firebase(data):
    if not data:
        print("\n🗃️ 추출된 데이터가 없어 Firebase 업로드를 멈춥니다.")
        return
        
    print("\n🗃️ [DB 저장] 실제 추출 데이터를 Firebase에 밀어 넣습니다...")
    firebase_url = "https://egg-map-c20f2-default-rtdb.asia-southeast1.firebasedatabase.app/eggs.json"
    
    try:
        req = Request(firebase_url, method='PUT')
        req.add_header('Content-Type', 'application/json')
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        urlopen(req, data=json_data)
        print("🎉 [저장 완료] 놀랍게도 시스템이 완벽하게 돌아갔습니다!")
    except Exception as e:
        print(f"❌ [저장 실패] 전송 오류: {e}")

if __name__ == "__main__":
    result = fetch_real_prices()
    upload_to_firebase(result)
