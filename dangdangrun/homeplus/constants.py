from typing import List, Union

from .models import Store

# 크롤링에 오류가 발생하는 경우 주석처리
# ("점포가 존재하지 않습니다" 오류 발생)
stores = [
    #
    # 서울특별시
    #
    Store(id=177, name="가양점", region="서울특별시"),
    Store(id=92, name="강동점", region="서울특별시"),
    # Store(id=51, name="강서점", region="서울특별시"),
    Store(id=37, name="금천점", region="서울특별시"),
    Store(id=38, name="동대문점", region="서울특별시"),
    Store(id=170, name="면목점", region="서울특별시"),
    Store(id=179, name="목동점", region="서울특별시"),
    Store(id=186, name="방학점", region="서울특별시"),
    Store(id=121, name="서울남현점", region="서울특별시"),
    Store(id=122, name="서울상봉점", region="서울특별시"),
    Store(id=180, name="시흥점", region="서울특별시"),
    Store(id=62, name="신내점", region="서울특별시"),
    Store(id=194, name="신도림점", region="서울특별시"),
    Store(id=24, name="영등포점", region="서울특별시"),
    Store(id=98, name="월곡점", region="서울특별시"),
    Store(id=184, name="월드컵점", region="서울특별시"),
    Store(id=75, name="잠실점", region="서울특별시"),
    Store(id=172, name="중계점", region="서울특별시"),
    Store(id=115, name="합정점", region="서울특별시"),
    #
    # 인천/경기
    #
    # Store(id=27, name="가좌점", region="인천/경기"),
    Store(id=18, name="간석점", region="인천/경기"),
    Store(id=102, name="경기하남점", region="인천/경기"),
    Store(id=163, name="계산점", region="인천/경기"),
    Store(id=109, name="고양터미널점", region="인천/경기"),
    # Store(id=168, name="구월점", region="인천/경기"),
    Store(id=20, name="김포점", region="인천/경기"),
    # Store(id=67, name="김포풍무점", region="인천/경기"),
    Store(id=25, name="동수원점", region="인천/경기"),
    Store(id=191, name="병점점", region="인천/경기"),
    Store(id=32, name="부천상동점", region="인천/경기"),
    # Store(id=43, name="부천소사점", region="인천/경기"),
    # Store(id=91, name="부천여월점", region="인천/경기"),
    Store(id=14, name="북수원점", region="인천/경기"),
    Store(id=93, name="분당오리점", region="인천/경기"),
    Store(id=117, name="서수원점", region="인천/경기"),
    Store(id=94, name="송탄점", region="인천/경기"),
    Store(id=39, name="시화점", region="인천/경기"),
    Store(id=181, name="안산고잔점", region="인천/경기"),
    # Store(id=53, name="안산선부점", region="인천/경기"),
    Store(id=167, name="안양점", region="인천/경기"),
    Store(id=173, name="야탑점", region="인천/경기"),
    Store(id=15, name="영통점", region="인천/경기"),
    Store(id=118, name="오산점", region="인천/경기"),
    Store(id=178, name="원천점", region="인천/경기"),
    Store(id=36, name="의정부점", region="인천/경기"),
    Store(id=99, name="인천논현점", region="인천/경기"),
    Store(id=124, name="인천송도점", region="인천/경기"),
    Store(id=116, name="인천숭의점", region="인천/경기"),
    Store(id=114, name="인천연수점", region="인천/경기"),
    Store(id=120, name="인천청라점", region="인천/경기"),
    Store(id=188, name="인하점", region="인천/경기"),
    # Store(id=161, name="일산점", region="인천/경기"),
    # Store(id=19, name="작전점", region="인천/경기"),
    Store(id=96, name="진접점", region="인천/경기"),
    Store(id=100, name="킨텍스점", region="인천/경기"),
    Store(id=87, name="파주문산점", region="인천/경기"),
    Store(id=125, name="파주운정점", region="인천/경기"),
    Store(id=83, name="평촌점", region="인천/경기"),
    Store(id=108, name="평택안중점", region="인천/경기"),
    Store(id=68, name="포천송우점", region="인천/경기"),
    # Store(id=101, name="화성동탄점", region="인천/경기"),
    Store(id=105, name="화성향남점", region="인천/경기"),
    #
    # 대전
    #
    Store(id=86, name="대전가오점", region="대전"),
    # Store(id=29, name="동대전점", region="대전"),
    Store(id=182, name="문화점", region="대전"),
    Store(id=88, name="서대전점", region="대전"),
    Store(id=185, name="유성점", region="대전"),
    #
    # 충남
    #
    # Store(id=79, name="계룡점", region="충남"),
    Store(id=70, name="논산점", region="충남"),
    Store(id=73, name="보령점", region="충남"),
    # Store(id=171, name="천안신방점", region="충남"),
    Store(id=85, name="천안점", region="충남"),
    #
    # 충북
    #
    Store(id=57, name="동청주점", region="충북"),
    # Store(id=90, name="오창점", region="충북"),
    # Store(id=183, name="청주성안점", region="충북"),
    Store(id=40, name="청주점", region="충북"),
    #
    # 세종
    #
    Store(id=123, name="세종점", region="세종"),
    Store(id=81, name="조치원점", region="세종"),
    #
    # 광주
    #
    Store(id=78, name="광주계림점", region="광주"),
    Store(id=77, name="광주하남점", region="광주"),
    Store(id=30, name="동광주점", region="광주"),
    #
    # 전북
    #
    Store(id=58, name="김제점", region="전북"),
    Store(id=64, name="익산점", region="전북"),
    Store(id=190, name="전주완산점", region="전북"),
    Store(id=76, name="전주점", region="전북"),
    Store(id=106, name="전주효자점", region="전북"),
    #
    # 전남
    #
    Store(id=52, name="광양점", region="전남"),
    Store(id=80, name="목포점", region="전남"),
    Store(id=41, name="순천점", region="전남"),
    # Store(id=175, name="순천풍덕점", region="전남"),
    #
    # 대구
    #
    # Store(id=42, name="남대구점", region="대구"),
    Store(id=187, name="내당점", region="대구"),
    Store(id=103, name="대구수성점", region="대구"),
    Store(id=164, name="동촌점", region="대구"),
    Store(id=72, name="상인점", region="대구"),
    Store(id=31, name="성서점", region="대구"),
    Store(id=22, name="칠곡점", region="대구"),
    #
    # 경북
    #
    Store(id=119, name="경산점", region="경북"),
    Store(id=21, name="경주점", region="경북"),
    Store(id=54, name="구미점", region="경북"),
    Store(id=89, name="문경점", region="경북"),
    Store(id=112, name="안동점", region="경북"),
    Store(id=74, name="영주점", region="경북"),
    Store(id=66, name="죽도점", region="경북"),
    Store(id=193, name="포항점", region="경북"),
    #
    # 강원
    #
    Store(id=95, name="강릉점", region="강원"),
    Store(id=61, name="삼척점", region="강원"),
    Store(id=113, name="원주점", region="강원"),
    Store(id=97, name="춘천점", region="강원"),
    #
    # 울산
    #
    Store(id=34, name="울산남구점", region="울산"),
    Store(id=84, name="울산동구점", region="울산"),
    Store(id=165, name="울산북구점", region="울산"),
    Store(id=23, name="울산점", region="울산"),
    #
    # 부산
    #
    Store(id=65, name="동래점", region="부산"),
    # Store(id=59, name="부산감만점", region="부산"),
    Store(id=195, name="부산반여점", region="부산"),
    Store(id=110, name="부산연산점", region="부산"),
    Store(id=104, name="부산정관점", region="부산"),
    Store(id=169, name="서면점", region="부산"),
    Store(id=12, name="서부산점", region="부산"),
    Store(id=26, name="센텀시티점", region="부산"),
    Store(id=33, name="아시아드점", region="부산"),
    # Store(id=44, name="영도점", region="부산"),
    Store(id=174, name="장림점", region="부산"),
    Store(id=176, name="해운대점", region="부산"),
    #
    # 경남
    #
    Store(id=63, name="거제점", region="경남"),
    Store(id=16, name="김해점", region="경남"),
    Store(id=56, name="마산점", region="경남"),
    Store(id=60, name="밀양점", region="경남"),
    # Store(id=71, name="삼천포점", region="경남"),
    Store(id=69, name="진주점", region="경남"),
    Store(id=82, name="진해점", region="경남"),
    Store(id=17, name="창원점", region="경남"),
    #
    # 제주
    #
    Store(id=55, name="서귀포점", region="제주"),
]

stores = [store for store in stores]

stores_by_name = {store.name: store for store in stores}
stores_by_id = {store.id: store for store in stores}

regions = list(dict.fromkeys(store.region for store in stores))


def get_store_by_name(name: str) -> Store:
    return stores_by_name[name]


def get_store_by_id(id: int) -> Store:
    return stores_by_id[id]


def get_stores_in_region(regions: Union[str, List[str]]) -> List[Store]:
    if isinstance(regions, str):
        regions = [regions]

    return list(filter(lambda store: store.region in regions, stores))
