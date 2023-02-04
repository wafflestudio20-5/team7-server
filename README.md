# :waffle: team7-7elog-server
>  ***team 7elog의 server repository입니다.***
<div align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>
    <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=Django&logoColor=white"/>
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=MySQL&logoColor=white"/>
    <img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=flat&logo=Amazon AWS&logoColor=white"/>
    <img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=flat&logo=Amazon EC2&logoColor=white"/>
</div>

## :bulb: About the project: velog

[![image](https://user-images.githubusercontent.com/110763772/216703613-2c99599b-9ed5-4189-ab01-b0cdbb80682f.png)](https://velog.io/)

- 개발자들을 위한 블로그 서비스  
    - server : [https://api.7elog.store](https://api.7elog.store/)  
    - web: [https://7elog.store](https://7elog.store/)  

## :technologist: 팀원 - backend

|Contributor|Contribution|
|:------:|:--------:|
|[장승현](https://github.com/jang1751)|AWS 배포|
|[현준기](https://github.com/orbizzz)|User API|
|[김서연](https://github.com/kimtjdus)|Post API|
|[김아연](https://github.com/kay1918)|Comment API|

## :hammer_and_wrench: 기술 스택
- framework: Django
- db: MySQL
- language: python

## :clipboard: commit convention
- 프로젝트 생성 ⇒ :tada: Feat: ~~
- 기능 추가 ⇒ :sparkles: Feat: ~~
- 버그 수정 ⇒ :bug: Fix: ~~
- 디자인 변경 ⇒ :lipstick: Design: ~~
- 코드 포멧 변경 ⇒ :art: Style: ~~
- 코드 리펙토링 ⇒ :recycle: Refactor: ~~
- 문서 수정 ⇒ :memo: Docs: ~~
- 파일 및 폴더명 수정 ⇒ :truck: Rename: ~~


## :card_file_box: model diagram
<div align="center">
    <img src="https://user-images.githubusercontent.com/110763772/216666595-22780410-827a-488d-8769-e18869608cbb.png" width="600" height="600"/>
</div>


## :sparkles: Features
### 구현 완료
- dj_rest_auth와 jwt token을 활용한 Signup, Login, Logout, SocialLogin(Google)
- User Edit, User Search, User Delete
- Post 작성 및 수정, Comment 작성 및 수정
- Post에 대한 추가적인 정보인 Tag, Series 구현
- Post 생성 날짜에 따른 필터링 기능, Tag 필터링 기능, Series 필터링 기능
- Post Content에 쓰이는 Image들을 PostId 및 ImageUrl을 토대로 PostImage 클래스의 인스턴스로 저장


## API
- API docs : [https://api.7elog.store/api/v1/docs/](https://api.7elog.store/api/v1/docs/) 
- User API : [https://ahyeon98.notion.site/User-Api-002777e5240e4d82afe1f573730ad1c9](https://ahyeon98.notion.site/User-Api-002777e5240e4d82afe1f573730ad1c9)

-------------
### Pre-commit Guide
가상환경 생성 후, 터미널에서 다음을 실행하면 pre-commit 설정 가능합니다.

    pip install -r requirements.txt (requirements.txt 위치 주의)
    npm install
    npm run prepare (team7-server로 이동하여 실행해야 함)




