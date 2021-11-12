area_info = {
    "해운대": ["부산", "남해", 1],
    "송정": ["부산", "남해", 2],
    "임랑": ["부산", "남해", 3],
    "다대포": ["부산", "남해", 4],
    "진하": ["울산", "동해", 5],
    "대진": ["영덕", "동해", 6],
    "경포해변": ["강릉", "동해", 7],
    "금진해변": ["강릉", "동해", 8],
    "사천해변": ["강릉", "동해", 9],
    "추암": ["동해", "동해", 10],
    "삼척": ["삼척", "동해", 11],
    "용화": ["삼척", "동해", 12],
    "죽도": ["양양", "동해", 13],
    "갯마을": ["양양", "동해", 14],
    "인구": ["양양", "동해", 15],
    "동산": ["양양", "동해", 16],
    "남애3리": ["양양", "동해", 17],
    "설악": ["양양", "동해", 18],
    "기사문": ["양양", "동해", 19],
    "만리포": ["태안", "서해", 20],
    "곽지과물": ["제주", "제주", 21],
    "중문ㆍ색달": ["제주", "제주", 22],
    "이호테우": ["제주", "제주", 23],
    "남열해돋이": ["고흥", "남해", 24],
}


def bearing_16_to_kr(vec):
    if not vec:
        return ""
    vec = int(vec)
    if vec == 0 or vec == 3600:
        return "북"
    elif vec > 0 and vec <= 225:
        return "북북동"
    elif vec > 225 and vec <= 450:
        return "북동"
    elif vec > 450 and vec <= 675:
        return "동북동"
    elif vec > 675 and vec <= 900:
        return "동"
    elif vec > 900 and vec <= 1125:
        return "동남동"
    elif vec > 1125 and vec <= 1350:
        return "남동"
    elif vec > 1350 and vec <= 1575:
        return "남남동"
    elif vec > 1575 and vec <= 1800:
        return "남"
    elif vec > 1800 and vec <= 2025:
        return "남남서"
    elif vec > 2025 and vec <= 2250:
        return "남서"
    elif vec > 2250 and vec <= 2475:
        return "서남서"
    elif vec > 2475 and vec <= 2700:
        return "서"
    elif vec > 2925 and vec <= 3150:
        return "서북서"
    elif vec > 3150 and vec <= 2375:
        return "북서"
    elif vec > 2375 and vec < 3600:
        return "북북서"


def data_to_one_down_float_str(data):
    if not data:
        return ""
    if len(data) == 1:
        return f"0.{data}"
    return f"{data[:-1]}.{data[-1]}"
