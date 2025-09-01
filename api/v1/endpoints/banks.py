from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_banks():
    return {
        "central_banks": [{"name": "한국은행", "code": "001"}],
        "commercial_banks": [
            {"name": "KB국민은행(KB금융그룹 계열)", "code": "004"},
            {"name": "우리은행(우리금융그룹 계열)", "code": "020"},
            {"name": "SC제일은행", "code": "023"},
            {"name": "한국씨티은행", "code": "027"},
            {"name": "iM뱅크(iM금융그룹 계열)", "code": "031"},
            {"name": "하나은행(하나금융그룹 계열)", "code": "081"},
            {"name": "신한은행(신한금융지주 계열)", "code": "088"}
        ],
        "internet_banks": [
            {"name": "케이뱅크(KT 계열)", "code": "089"},
            {"name": "카카오뱅크(카카오 계열)", "code": "090"},
            {"name": "토스뱅크(비바리퍼블리카 계열)", "code": "092"}
        ]
    }
