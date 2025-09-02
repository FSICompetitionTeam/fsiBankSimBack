from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_banks():
    return {
        "central_banks": [{"name": "한국은행", "code": "001"}],
        "commercial_banks": [
            {"name": "KB국민은행", "code": "004"},
            {"name": "우리은행", "code": "020"},
            {"name": "SC제일은행", "code": "023"},
            {"name": "한국씨티은행", "code": "027"},
            {"name": "iM뱅크", "code": "031"},
            {"name": "하나은행", "code": "081"},
            {"name": "신한은행", "code": "088"},
            {"name": "Bithumb(국민은행)", "code": "094"},  # 추가
            {"name": "Korbit(신한은행)", "code": "096"}   # 추가
        ],
        "internet_banks": [
            {"name": "케이뱅크", "code": "089"},
            {"name": "카카오뱅크", "code": "090"},
            {"name": "토스뱅크", "code": "092"},
            {"name": "Upbit(케이뱅크)", "code": "093"},   # 추가
            {"name": "Coinone(카카오뱅크)", "code": "095"} # 추가
        ]
    }