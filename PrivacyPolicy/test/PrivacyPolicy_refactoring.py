import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


# set up & teardown
@pytest.fixture(scope="session")
def run():
    # chrome options for headless cronjob worker
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)

    driver: WebDriver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
    )
    
    yield driver
    driver.quit()

# 실행
@pytest.mark.parametrize("policy_url", [
    "https://policy.devsisters.com/ko/privacy/?date=2023-09-26"
])    
def test_connect(run, policy_url):
    run.get(policy_url)
    print("접속 성공!")

# 문구 비교
@pytest.mark.parametrize("text_xpath, text_original", [
    ('//*[@id="gatsby-focus-wrapper"]//main/h2', '개인정보처리방침'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[1]/div[1]/div[1]', '2023-09-26'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[1]', '데브시스터즈㈜(이하 “회사”)는 이용자의 개인정보보호를 중요시하며 개인정보보호 관련 법률을 준수하고 있습니다. \
회사는 이용자의 개인정보가 어떠한 용도와 방식으로 이용되고 있으며 개인정보보호를 위해 어떠한 조치가 취해지고 있는지 안내하고, \
이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보처리방침을 수립·공개합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[3]', '1. 수집하는 개인정보의 항목 및 수집방법'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[4]', '1) 수집하는 개인정보의 항목'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[5]', '회사는 다음과 같은 목적으로 개인정보를 수집·이용하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/table[1]', '서비스명 수집목적 수집항목 구분\n\
DevPlay 페이스북 계정 연동 회원가입/로그인 ID, 이름, 프로필 사진, 이메일 주소 필수\n\
애플 계정 연동 이메일 주소\n\
구글 계정 연동 이메일 주소\n\
구글 플레이 게임 서비스 계정 연동 이메일 주소\n\
이메일 주소 연동 이메일 주소, 비밀번호\n\
홈페이지 대표 홈페이지(www.devsisters.com) 윤리위반행위 신고 접수 이메일 주소 필수\n\
고객센터 홈페이지(cs.devsisters.com) 고객상담 (문의/답변) 이메일 주소, 카카오 회원번호 필수\n\
구글플레이ID, 사용자ID, 기종, OS 버전  선택\n\
채용 홈페이지(careers.devsisters.com) 채용 이름, 전화번호, 이메일 주소, 이력서(경력 및 자기소개 사항) 필수\n\
브릭시티 홈페이지(www.playbrixity.com) 뉴스레터 구독 신청 및 발송 이메일 주소 필수\n\
이벤트/프로모션 이벤트/프로모션 (사전예약) 이름, 이메일 주소, 전화번호, 주소, 우편번호 선택'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[6]', '※ 안정적인 서비스 제공, 계정 및 아이템 보호, 법률 준수, 부정 이용자 방지 등의 목적으로 서비스 이용 과정에서 아래와 같은 정보들이 생성되어 수집될 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[1]', '단말기 정보(모델명, OS정보, 모바일 펌웨어 버전, 기기고유번호), PC 정보(브라우저 정보, OS정보), IP 주소, 쿠키, 접속 기록, 위치정보 및 국가정보(IP 주소로부터 도출됨), 부정이용 기록, 서비스 이용 기록 등의 정보'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[7]', '※ 무료/유료 서비스 이용 과정에서 결제 등을 위해 불가피하게 필요한 경우(복구 및 환불 등), 이메일 주소, 구매내역 확인내용, 본인이 아닌 타인에 의한 결제 사실확인을 위한 실명 및 가족관계 증명이 수집될 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[9]', '2) 개인정보 수집방법'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[10]', '회사는 다음과 같은 방법으로 개인정보를 수집합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[2]', '회사의 서비스 가입 시 동의 절차제공을 통해 수집\n\
프로모션 및 이벤트 진행을 위해서는 별도의 동의절차를 통해 수집\n\
회사와 서비스 제공 관련 제휴관계에 있는 플랫폼을 통해 자동으로 수집\n\
서비스 가입 및 사용 중 고객응대 시 이용자의 자발적 제공 또는 필요에 의해 요청 후 수집\n\
채용 홈페이지 및 채용사이트를 통하여 개인정보 수집 동의 후 수집'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[12]', '2. 개인정보의 처리 목적'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[13]', '회사는 다음의 목적을 위하여 개인정보를 처리합니다. \
처리하고 있는 개인정보는 다음의 목적 이외의 용도로는 이용되지 않으며, 이용 목적이 변경되는 경우에는 「개인정보 보호법」 제18조에 따라 별도의 동의를 받는 등 필요한 조치를 이행할 예정입니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[14]', '1) 고지사항 전달, 불만 처리 등을 위한 원활한 의사소통 경로의 확보'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[15]', '2) 유료정보 이용에 대한 문의 처리 및 계약이행 분쟁 처리, 결제 환불 등 고객 서비스 제공'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[16]', '3) 새로운 서비스 및 신상품 이벤트 정보 등의 안내'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[17]', '4) 기타 컨텐츠 및 인증 서비스(ID/PW찾기 등) 제공'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[18]', '5) 이력서: 입사 지원자 관리, 입사 지원에 따른 본인확인 파악, 채용전형의 진행, 채용 결과 등 채용 관련 정보 안내'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[19]', '6) 상품·서비스의 구매 및 배송 또는 예약 업무 처리'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[21]', '3. 개인정보의 제3자 제공'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[22]', '1) 회사는 이용자의 개인정보를 ‘2. 개인정보의 처리 목적’에서 명시한 범위 내에서만 처리하며, 이용자의 동의, \
법률의 특별한 규정 등 「개인정보 보호법」 제17조 및 제18조에 해당하는 경우에만 개인정보를 제3자에게 제공하고 그 이외에는 이용자의 개인정보를 제3자에게 제공하지 않습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[23]', '2) 회사는 원활한 서비스 제공을 위해 다음의 경우 이용자의 동의를 얻어 필요 최소한의 범위로만 제공합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/table[2]', '제공받는 자 제공목적 제공항목 보유 및 이용기간\n\
오븐게임즈㈜ 계열사 채용 시 입사지원자 정보 공유 및 입사전형 진행 이름, 전화번호, 이메일 주소, 이력서(경력 및 자기소개 사항) 인력풀에서 상시채용을 위해 5년 동안 보관\n\
스튜디오킹덤㈜ 상동 상동 상동\n\
프레스에이㈜ 상동 상동 상동'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[26]', '4. 개인정보의 보유 및 이용기간'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[27]', '1) 회사는 이용자로부터 개인정보 수집 시에 동의 받은 개인정보 보유·이용기간 또는 법령에 따른 개인정보 보유·이용기간 내에서 개인정보를 처리·보유합니다. \
각각의 개인정보 처리 및 보유 기간은 다음과 같으며, 기타 이용자의 개별적인 동의가 있는 경우에는 개별 동의에 따른 기간까지 보관합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[28]', '(1) 서비스 이용 기록'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[3]', '보존 이유: 탈퇴회원 관리, 서비스 관련 분쟁 예방 및 관리, 부정 이용 방지\n\
보존 기간: 회원 탈퇴일로부터 1개월'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[29]', '(2) 고객 상담 내용'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[4]', '보존 이유: 고객불만사항 처리 내역 관리 및 사후 분쟁 예방\n\
보존 기간: 고객상담 완료일로부터 3년'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[30]', '(3) 채용에 관한 기록'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[5]', '보존 이유: 채용전형 진행, 입사 지원서 수정, 합격 여부 확인, 입사 지원자와의 원활한 의사소통, 채용이 필요한 경우 해당 인력풀에서 상시채용으로 활용\n\
보존 기간: 채용이력서 등록일로부터 5년'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[32]', '2) 회사는 다음과 같이 관계법령에 따라 일정한 기간 동안 이용자의 정보를 보관합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/table[3]', '구 분 보존 근거 보존 기간\n\
접속에 관한 기록보존 통신비밀보호법 3개월\n\
표시·광고에 관한 기록 전자상거래 등에서의 소비자보호에 관한 법률 6개월\n\
소비자의 불만 또는 분쟁처리에 관한 기록 3년\n\
계약 또는 청약철회 등에 관한 기록 5년\n\
대금결제 및 재화 등의 공급에 관한 기록 5년\n\
신용정보의 수집, 처리 및 이용 등에 관한 기록 신용정보의 이용 및 보호에 관한 법률 3년'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[34]', '3) 위 1)항 및 2)항에 따라 보유하고 있는 개인정보에 대하여 귀하가 열람을 요구하는 경우 회사는 지체 없이 그 내용을 열람, \
확인할 수 있도록 조치하겠습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[36]', '5. 개인정보의 파기'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[37]', '1) 회사는 개인정보 보유기간의 경과, 처리목적 달성 등 개인정보가 불필요하게 되었을 때에는 지체없이 해당 개인정보를 파기합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[38]', '2) 이용자로부터 동의받은 개인정보 보유기간이 경과하거나 처리목적이 달성되었음에도 불구하고 다른 법령에 따라 개인정보를 계속 보존하여야 하는 경우에는, \
해당 개인정보를 별도의 데이터베이스(DB)로 옮기거나 보관장소를 달리하여 보존합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[39]', '3) 개인정보의 파기 절차 및 방법은 다음과 같습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[40]', '(1) 파기 절차: 회사는 파기 사유가 발생한 개인정보를 선정하여 파기합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[41]', '(2) 파기 방법: 회사는 전자적 파일형태로 기록·저장된 개인정보는 기록을 재생할 수 없도록 파기하며, \
종이 문서에 기록·저장된 개인정보는 분쇄기로 분쇄하거나 소각하여 파기합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[43]', '6. 개인정보의 처리 위탁'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[44]', '1) 회사는 서비스 제공 및 향상을 위하여 다음과 같이 개인정보 처리업무를 위탁하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/table[4]', '위탁받는 자(수탁자) 위탁업무 보유 및 이용기간\n\
Amazon Web Services Inc. 클라우드 서비스 제공을 위한 인프라 관리 이용목적 달성 시(각 ‘4. 개인정보의 보유 및 이용기간’에 따름) 또는 위탁계약 종료 시까지\n\
오븐게임즈㈜ 컨텐츠 운영\n\
스튜디오킹덤㈜\n\
Brevo 이메일 발송\n\
이에프에스㈜ 배송 물류관리\n\
Zendesk Inc. 고객 질의 응답을 위한 서비스 제공 및 직원 채용을 위한 업무\n\
㈜큐로드\n\
고객 상담 및 응대 서비스 운영\n\
㈜메타브레인 브릭시티 사전예약 사이트 운영'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[45]', '2) 회사는 위탁계약 체결 시 「개인정보 보호법」 제26조에 따라 위탁업무 수행목적 외 개인정보 처리금지, \
기술적·관리적 보호조치, 재위탁 제한, 수탁자에 대한 관리·감독, 손해배상 등 책임에 관한 사항을 계약서 등 문서에 명시하고, 수탁자가 개인정보를 안전하게 처리하는지를 관리·감독하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[46]', '3) 위탁업무의 내용이나 수탁자가 변경될 경우에는 지체없이 본 개인정보 처리방침을 통하여 공개하도록 하겠습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[48]', '7. 개인정보의 국외 이전'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[49]', '회사가 이용자께서 원활한 게임서비스를 제공받을 수 있도록 다음과 같이 국외 업체에 이용자의 개인정보 처리업무를 위탁하고 있습니다. \
채용정보 등록을 위한 개인정보 수집은 데이터베이스 동기화에 따라 국외 이전하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/table[5]', '이전받는 자 (연락처) 이전 목적 이전되는 개인정보 항목 이전되는 국가 이전 일시 및 방법 개인정보 보유 및 이용기간\n\
Amazon Web Services Inc. (https://aws.amazon.com/ko/contact-us/) 서비스 가입 및 이용 ID, 이름, 프로필 사진, 이메일 주소, 비밀번호 미국, 일본 서비스 이용 및 채용정보 등록 시 실시간 데이터베이스 동기로 이전 회원 탈퇴일로부터 1개월\n\
채용정보 등록 이름, 전화번호, 이메일 주소, 이력서(경력 및 자기소개 사항) 채용이력서 등록일로부터 5년\n\
Zendesk Inc. (https://www.zendesk.com/company/contact-info/) 고객 상담(문의/답변) 이메일 주소, 카카오 회원번호, 구글플레이ID, 사용자ID, 기종, OS 버전 아일랜드 고객상담 시 실시간 데이터베이스 동기로 이전 고객상담 완료일로부터 3년\n\
Brevo (https://www.brevo.com/contact/) 사전예약 정보 전송용 이메일 주소 등록 이메일 주소 프랑스 이메일 주소 등록 시 실시간 데이터베이스 동기로 이전 이메일 주소 등록일로부터 1년\n\
뉴스레터, 게임정보 및 이벤트 정보 안내, 마케팅, 이벤트/프로모션 알림을 위한 이메일 발송'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[51]', '8. 이용자·법정대리인의 권리 및 그 행사 방법'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[52]', '1) 이용자는 회사에 대해 언제든지 개인정보 열람·정정·삭제·처리정지 요구 등의 권리를 행사할 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[53]', '※ 만 14세 이상의 미성년자인 이용자는 이용자의 개인정보에 관하여 미성년자 본인이 권리를 행사하거나 법정대리인을 통하여 권리를 행사할 수도 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[54]', '2) 권리 행사는 개인정보 보호책임자에게 서면, 이메일 등을 통하여 하실 수 있으며, 회사는 이에 대해 지체없이 조치하겠습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[55]', '3) 권리 행사는 이용자의 법정대리인이나 위임을 받은 자 등 대리인을 통하여 하실 수도 있습니다. \
이 경우 “개인정보 처리 방법에 관한 고시(제2020-7호)” 별지 제11호 서식에 따른 위임장을 제출하셔야 합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[56]', '4) 개인정보 열람 및 처리정지 요구는 「개인정보 보호법」 제35조 제4항, 제37조 제2항에 의하여 이용자의 권리가 제한될 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[57]', '5) 이용자가 개인정보의 오류에 대한 정정을 요청하신 경우에는 정정을 완료하기 전까지 당해 개인정보를 이용 또는 제공하지 않습니다. \
또한, 잘못된 개인정보를 제3자에게 이미 제공한 경우에는 정정 처리결과를 제3자에게 지체 없이 통지하여 정정이 이루어지도록 하겠습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[58]', '6) 개인정보의 정정 및 삭제 요구는 다른 법령에서 그 개인정보가 수집 대상으로 명시되어 있는 경우에는 그 삭제를 요구할 수 없습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[59]', '7) 회사는 이용자 또는 법정대리인의 요청에 의해 해지 또는 삭제된 개인정보는 ‘4. 개인정보의 보유 및 이용기간’에 명시된 바에 따라 처리하고 그 외의 용도로 열람 또는 이용할 수 없도록 처리하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[60]', '8) 회사는 이용자 권리에 따른 열람의 요구, 정정·삭제의 요구, 처리 정지의 요구 시 열람 등 요구를 한 자가 본인이거나 정당한 대리인인지를 확인합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[62]', '9. 개인정보 자동수집 장치의 설치·운영 및 거부에 관한 사항'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[63]', '1) 회사는 이용자에게 개별적인 맞춤서비스 및 편리한 웹사이트 사용 환경을 제공하기 위해 이용 정보를 저장하고 수시로 불러오는 ‘쿠키(cookie)’를 사용합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[64]', '2) 쿠키는 웹사이트를 운영하는 데 이용되는 서버(http)가 이용자의 컴퓨터 브라우저에게 전송하는 소량의 정보이며 이용자의 PC 컴퓨터 내의 하드디스크에 저장되기도 합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[65]', '(1) 쿠키의 사용 목적: 이용자의 각 서비스 및 웹사이트 방문 및 이용 형태(방문 시간, 방문 횟수, 접속 빈도 등), \
이용자의 취향 및 관심분야 등을 파악 및 분석하여 이용자에게 최적화된 정보 제공을 위해 사용됩니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[66]', '(2) 쿠키의 설치·운영 및 거부: 이용자는 쿠키의 설치 및 수집에 대해 자율적으로 선택할 수 있습니다. \
따라서, 이용자는 웹 브라우저에서 옵션을 설정함으로써 쿠키 저장을 거부할 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[67]', '쿠키 설정 방법'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[6]', 'Internet Explorer의 경우: 웹 브라우저 상단의 [도구] > [인터넷 옵션] > [개인정보] > [고급]\n\
Chrome의 경우: 웹 브라우저 우측 상단의 [⋮] > [설정] > 좌측 상단의 [개인 정보 보호 및 보안] > [사이트 설정] > [쿠키 및 기타 사이트 데이터]'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[68]', '※ 그 외의 브라우저의 경우 브라우저별 설정 방식에 따릅니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[69]', '(3) 쿠키의 저장을 거부할 경우 서비스 이용에 어려움이 발생할 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[70]', '3) 회사는 Google Analytics와 같이 다양한 외부 웹로그 분석 도구를 사용할 수 있으며, Google Analytics의 경우 데이터가 사용되는 것을 거부할 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[7]', 'Google Analytics 차단: https://tools.google.com/dlpage/gaoptout/'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[71]', '※ 그 외의 웹로그 분석 도구의 경우 도구별 거부 방식에 따릅니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[73]', '10. 개인정보의 안전성 확보조치'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[74]', '1) 회사는 이용자들의 개인정보를 처리함에 있어 개인정보가 분실, 도난, 유출, 위∙변조 또는 훼손되지 않도록 \
「개인정보 보호법」 및 그 하위 법령에 따라 개인정보의 안전성 확보를 위하여 다음과 같은 조치를 취하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[75]', '(1) 관리적 조치: 내부관리계획 수립·시행, 전담조직 운영, 정기적 직원 교육'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[76]', '(2) 기술적 조치: 개인정보처리시스템 등의 접근권한 관리, 접근통제시스템 설치, 개인정보의 암호화, 보안프로그램 설치 및 갱신'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[77]', '(3) 물리적 조치: 전산실, 자료보관실 등의 접근통제'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[79]', '2) 회사는 개인정보의 안전성을 확보하기 위하여 법령에서 규정하고 있는 사항 이외에도 다음과 같은 활동을 시행하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[80]', '(1) 비밀번호의 일방향 암호화'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[81]', '회사는 서비스 제공 관련 제휴관계에 있는 플랫폼 회원의 비밀번호를 수집하지 않습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[82]', '(2) 해킹 등의 대비책'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[83]', '회사는 해킹 등에 의해 이용자의 개인정보가 유출되는 것을 막기 위해 외부로부터 침입을 차단하는 장치를 설치, 운용하여 외부로부터의 공격, 해킹 등을 막고 있으며, \
특히 이용자의 개인정보를 가지고 있는 서버는 외부의 인터넷 라인과 직접 연결하지 않고 별도로 관리하는 등 최고 수준의 보안을 유지하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[84]', '또한, 만약의 사태에 대비하여 시스템과 데이터를 백업하는 체제를 갖추고 있고, 백신프로그램을 이용하여 컴퓨터 바이러스에 의한 피해를 방지하기 위한 조치를 취하고 있습니다. \
백신프로그램은 주기적으로 업데이트되며, 갑작스러운 바이러스가 출현할 경우 백신이 나오는 즉시 이를 제공함으로써 개인정보가 침해되는 것을 방지하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[85]', '(3) 처리 직원의 제한 및 교육'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[86]', '회사는 개인정보처리 직원을 최소한으로 제한하고 담당직원에 대한 수시 교육을 통하여 본 개인정보 처리방침의 준수를 강조하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[87]', '(4) 개인정보보호전담기구의 운영'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[88]', '회사는 사내 개인정보보호전담기구 등을 통하여 본 개인정보 처리방침의 이행사항 및 담당자의 준수 여부를 점검하여 문제가 발견될 경우 즉시 시정조치하고 있습니다. \
단, 이용자 본인의 부주의나 인터넷상의 문제로 서비스 제공 관련 제휴관계에 있는 플랫폼의 계정(ID) 및 비밀번호, 닉네임, 이메일 등 개인정보가 유출되어 발생한 문제에 대해 회사는 일체의 책임을 지지 않습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[89]', '(5) 접속권한 및 로그기록 보존'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[90]', '회사는 접속 권한을 주기적으로 검토하고, 로그기록을 안전하게 보관하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[91]', '(6) 회사는 이용자의 개인정보 이용내역 통지를 「개인정보 보호법」 제39조의8 및 동법 시행령 제48조의6에 의거하여 법적 의무 준수를 위해 주기적으로 실시합니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[93]', '11. 개인정보 보호책임자'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[94]', '1) 회사는 개인정보 처리에 관한 업무를 총괄해서 책임지고, 개인정보 처리와 관련한 이용자의 불만처리 및 피해구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[96]', '개인정보 보호책임자 및 개인정보 보호 담당부서'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[8]', '개인정보 보호책임자: 정문희\n\
소속 및 직책: 경영기획실/ 부사장\n\
전화번호: 1899-3674\n\
이메일: privacy@devsisters.com\n\
팩스번호: 02-2148-0626'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[98]', '2) 이용자는 회사의 서비스를 이용하시면서 발생한 모든 개인정보보호 관련 문의, 불만처리, 피해구제 등에 관한 사항을 개인정보 보호책임자 및 담당부서로 문의하실 수 있습니다. \
회사는 이용자의 문의에 대해 신속하고 성실하게 답변해드리겠습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[100]', '12. 권익침해 구제방법'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[101]', '1) 이용자는 개인정보침해로 인한 구제를 받기 위하여 개인정보분쟁조정위원회, 한국인터넷진흥원 개인정보침해신고센터 등에 분쟁해결이나 상담 등을 신청할 수 있습니다. \
이 밖에 기타 개인정보침해의 신고, 상담에 대하여는 아래의 기관에 문의하실 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[9]', '개인정보분쟁조정위원회: (국번없이) 1833-6972 (www.kopico.go.kr)\n\
개인정보침해신고센터: (국번없이) 118 (privacy.kisa.or.kr)\n\
대검찰청 사이버수사과: (국번없이) 1301 (www.spo.go.kr)\n\
경찰청 사이버수사국: (국번없이) 182 (ecrm.police.go.kr)'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[103]', '2) 회사는 이용자의 개인정보자기결정권을 보장하고, 개인정보침해로 인한 상담 및 피해 구제를 위해 노력하고 있으며, 신고나 상담이 필요한 경우 아래의 담당부서로 연락해 주시기 바랍니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[104]', '개인정보보호 관련 고객 상담 및 신고'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[10]', '부서명: 경영기획실\n\
담당자: 정문희\n\
전화번호: 1899-3674\n\
이메일: privacy@devsisters.com\n\
팩스번호: 02-2148-0626'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[106]', '13. 기타'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[107]', '1) 회사는 이용자께 다른 회사의 웹사이트 또는 자료에 대한 링크를 제공할 수 있습니다. \
이 경우 회사는 외부 사이트 및 자료에 대한 아무런 통제권이 없으므로 그로부터 제공받는 서비스나 자료의 유용성에 대해 책임질 수 없으며 보증할 수 없습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[108]', '2) 회사에서 제공하는 서비스의 링크를 클릭하여 타 사이트의 페이지로 옮겨갈 경우 \
해당 사이트의 개인정보보호정책 및 약관사항은 당사와 무관하므로 새로 방문한 사이트의 정책을 확인하시기 바랍니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[109]', '3) 이용자는 제공하신 개인정보를 최신의 상태로 정확하게 입력하여 불의의 사고를 예방하여 주시기 바랍니다. \
이용자가 입력한 부정확한 정보로 인해 발생하는 사고의 책임은 본인에게 있으며, \
타인 정보의 도용 등 허위정보를 입력할 경우 계정의 이용이 제한되거나 계정이 삭제될 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[110]', '4) 이용자는 개인정보를 보호받을 권리를 보유하나 이와 동시에 본인의 정보를 스스로 보호하고 타인의 정보를 침해하지 않을 의무도 가지고 있습니다. \
비밀번호를 포함한 본인의 개인정보가 유출되지 않도록 조심하시고, 게시물을 포함한 타인의 개인정보를 훼손하지 않도록 유의해 주시기 바랍니다. \
만약 이와 같은 책임을 다하지 못하고 타인의 정보 및 존엄성을 훼손할 시에는 관련법령 등에 의해 처벌받을 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[111]', '5) 이용자가 개인정보를 입력함에 있어 부정확하거나 잘못된 정보를 입력함으로써 발생되는 서비스 이용상의 불이익 및 물질적 손해는 전적으로 본인에게 책임이 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[113]', '14. 개인정보 처리방침의 변경에 관한 사항'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[114]', '1) 본 개인정보 처리방침은 2023. 09. 26.부터 적용됩니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[115]', '2) 이전의 개인정보 처리방침은 아래 또는 본 페이지의 좌측 상단에 위치한 ‘시행일자’를 통하여 확인하실 수 있습니다.'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/ul[11]', '2022. 12. 08. ~ 2023. 09. 25. 적용 (클릭)'),
    ('//*[@id="gatsby-focus-wrapper"]//main/div[2]/p[116]', '3) 개인정보 처리방침의 내용에 변경이 있을 경우 개정 최소 7일 전에 회사 홈페이지 또는 회사가 제공하는 애플리케이션을 통해 변경 사항을 알려드리겠습니다.')
])

def test_privacy_policy_title(run, text_xpath, text_original):
    try:
        WebDriverWait(run, 10).until(EC.visibility_of_element_located((By.XPATH, text_xpath)))
        privacy_policy_text = run.find_element(By.XPATH, text_xpath)
        privacy_policy_text_displayed = privacy_policy_text.is_displayed()
        privacy_policy_text = privacy_policy_text.text
        
        assert privacy_policy_text_displayed
        assert privacy_policy_text == text_original
        
        # print(f"문구 존재 여부 : {privacy_policy_text_displayed}")
        # print(f"문구 출력 : {privacy_policy_text}")
        
    # 요소 못 찾을 때 발생하는 예외
    except NoSuchElementException as e:
        logging.error(f"요소를 찾을 수 없음 : {str(e)}")
        raise
    
    # 비교 시 False일 경우 예외
    except AssertionError as e:
        logging.error(f"비교 실패 : {str(e)}")
        raise
    
    # 다른 예외가 발생하면 예외
    except Exception as e:
        logging.error(f"에러 발생 : {str(e)}")
        raise
