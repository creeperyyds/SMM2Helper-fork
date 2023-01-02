from dataclasses import dataclass
import requests
from enum import Enum

from config import TGRCODE_API


class TGRCodeAPIException(BaseException):
    pass


@dataclass
class Maker:
    region: str
    maker_id: str
    name: str
    country: str
    last_active: str
    mii_image_url: str
    courses_played: int
    courses_cleared: int  # cleared + deaths = attempted
    courses_deaths: int
    likes: int
    maker_points: int
    easy_highscore: int
    normal_highscore: int
    expert_highscore: int
    super_expert_highscore: int
    versus_rating: int
    versus_rank: str
    versus_won: int  # won + lost = plays
    versus_lost: int
    versus_disconnected: int
    coop_clears: int
    coop_plays: int
    versus_kills: int
    versus_killed_by_others: int
    uploaded_levels: int
    last_uploaded_level: str
    super_world_id: str


@dataclass
class Course:
    name: str
    description: str
    uploaded_date: str
    data_id: str
    course_id: str
    game_style: str
    theme: str
    difficulty: str
    tag_1: str
    tag_2: str
    world_record: str
    upload_time: str
    clears: int
    attempts: int
    clear_rate: str
    likes: int
    boos: int
    plays: int
    maker: Maker
    record_holder: Maker


def deserialize_course(course: dict) -> Course:
    return Course(
        name=course['name'],
        description=course['description'],
        uploaded_date=course['uploaded_pretty'],
        course_id=course['course_id'],
        data_id=course['data_id'],
        game_style=course['game_style_name'],
        theme=course['theme_name'],
        difficulty=course['difficulty_name'],
        tag_1=course['tags_name'][0],
        tag_2=course['tags_name'][1],
        world_record=course['world_record_pretty'],
        upload_time=course['upload_time_pretty'],
        clears=course['clears'],
        attempts=course['attempts'],
        clear_rate=course['clear_rate_pretty'],
        likes=course['likes'],
        boos=course['boos'],
        plays=course['plays'],
        maker=deserialize_maker(course['uploader']),
        record_holder=deserialize_maker(course['record_holder'])
    )


def deserialize_maker(maker: dict) -> Maker:
    return Maker(
        region=maker['region_name'],
        maker_id=maker['code'],
        name=maker['name'],
        country=maker['country'],
        last_active=maker['last_active_pretty'],
        mii_image_url=maker['mii_image'],
        courses_played=maker['courses_played'],
        courses_cleared=maker['courses_cleared'],
        courses_deaths=maker['courses_deaths'],
        likes=maker['likes'],
        maker_points=maker['maker_points'],
        easy_highscore=maker['easy_highscore'],
        normal_highscore=maker['normal_highscore'],
        expert_highscore=maker['expert_highscore'],
        super_expert_highscore=maker['super_expert_highscore'],
        versus_rating=maker['versus_rating'],
        versus_rank=maker['versus_rank_name'],
        versus_won=maker['versus_won'],
        versus_lost=maker['versus_lost'],
        versus_disconnected=maker['versus_disconnected'],
        coop_clears=maker['coop_clears'],
        coop_plays=maker['coop_plays'],
        versus_kills=maker['versus_kills'],
        versus_killed_by_others=maker['versus_killed_by_others'],
        uploaded_levels=maker['uploaded_levels'],
        last_uploaded_level=maker['last_uploaded_level_pretty'],
        super_world_id=maker['super_world_id']
    )


def search_endless_mode(count: int = 10, difficulty_id: str = 'e') -> list[Course]:
    response = requests.get(
        url=f'{TGRCODE_API}/search_endless_mode',
        data={'difficulty': difficulty_id, 'count': count}
    )
    try:
        courses = response.json()['courses']
    except requests.exceptions.JSONDecodeError:
        raise TGRCodeAPIException(response.text)
    ret: list[Course] = []
    for course in courses:
        ret.append(deserialize_course(course))
    return ret


if __name__ == '__main__':
    print(search_endless_mode())