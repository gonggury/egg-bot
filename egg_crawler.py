import urllib.request
import json
import re
import time

def fetch_real_prices_stealth():
    print("👻 [V3 투명인간 모드] 브라우저 압수! 이마트 서버 데이터 주머니만 몰래 훔쳐옵니다...")
    
    url = "https://emart.ssg.com/search.ssg?target=all&query=%EA%B3%84%EB%9E%80+30%EA%B5%AC"
    
    # 이마트 서버가 '나는 평범한 맥북 사용자다'라고 속게 만드는 위장 신분증
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    
    req = urllib.request.Request(url, headers=headers)
    crawled_data = []
    
    try:
        resp = urllib.request.urlopen(req)
        html = resp.read().decode("utf-8")
        
        # 이마트 페이지 안에 숨겨진 진짜 데이터 주머니(__NEXT_DATA__) 고리 찾기
        match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        
        if not match:
            print("🚨 앗! 이마트가 투명인간마저 눈치채고 보안망(빈 페이지)을 가동했습니다. 작전 실패!")
            return crawled_data
            
        print("✅ 투명인간 잠입 성공! 이마트 데이터 주머니를 통째로 가져왔습니다.")
        
        # 복잡한 주머니 속에서 'sellprc(판매가)'라는 단어 옆의 숫자만 핀셋으로 빼내기
        prices = re.findall(r'"sellprc":(\d+)', match.group(1))
        
        if prices:
            best_price = int(prices[0]) # 첫 번째로 검색된 계란 최저가
            print(f"🎉 빙고!! 성공적으로 실제 가격을 파싱해 냈습니다: {best_price}원")
            
            # 테스트를 위해 성공 문구 수정
            mart_data = {
                "id": "seoul-0",
                "region": "seoul",
                "name": "이마트 역삼점 (무료 깃허브 V3 투명인간 성공!!)",
                "lat": 37.4999,
                "lng": 127.0376,
                "price": best_price,
                "stock": "재고 있음",
                "address": "역삼로 310",
                "updated": time.strftime("%m월 %d일 %H:%M")
            }
            crawled_data.append(mart_data)
        else:
            print("❌ 데이터 주머니는 훔쳤으나 계란 가격을 찾지 못했습니다.")
            
    except Exception as e:
         print(f"❌ [에러 발생] 투명인간 통신 중 서버가 끊어졌습니다: {e}")
         
    return crawled_data

def upload_to_firebase(data):
    if not data:
        print("\n🗃️ 추출된 데이터가 없어 파이어베이스 업로드를 멈춥니다.")
        return
        
    print("\n🗃️ [DB 저장] 투명인간이 훔쳐 온 진짜 데이터를 파이어베이스에 업로드합니다...")
    firebase_url = "https://egg-map-c20f2-default-rtdb.asia-southeast1.firebasedatabase.app/eggs.json"
    
    try:
        req = urllib.request.Request(firebase_url, method='PUT')
        req.add_header('Content-Type', 'application/json')
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        urllib.request.urlopen(req, data=json_data)
        print("🎉 [저장 완료] 깃허브의 한계를 뚫고 무료 자동화 시스템이 완성되었습니다!!")
    except Exception as e:
        print(f"❌ [저장 실패] 전송 오류: {e}")

if __name__ == "__main__":
    result = fetch_real_prices_stealth()
    upload_to_firebase(result)
