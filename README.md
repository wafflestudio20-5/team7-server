# :waffle: team7-server
team7 server repository

## :bulb: About the project
프로젝트(서비스) 소개  
server : [https://api.7elog.store](https://api.7elog.store/)  
web: [https://7elog.store](https://7elog.store/)  

## :technologist: 팀원 - backend
장승현  
현준기  
김서연  
김아연  

## :wrench: 기술 스택


## :pencil: commit convention


## :card_file_box: model diagram
<img src="https://user-images.githubusercontent.com/110763772/216666595-22780410-827a-488d-8769-e18869608cbb.png" width="600" height="600"/>


## :sparkles: Features
구현 완료한 기능
- dj_rest_auth와 jwt token을 활용한 Signup, Login, Logout, SocialLogin(Google)
- User Edit, User Search, User Delete
- Post 작성 및 수정, Comment 작성 및 수정
- Post에 대한 추가적인 정보인 Tag, Series 구현
- Post 생성 날짜에 따른 필터링 기능, Tag 필터링 기능, Series 필터링 기능
- Post Content에 쓰이는 Image들을 PostId 및 ImageUrl을 토대로 PostImage 클래스의 인스턴스로 저장(아직 연동 X)

### Pre-commit Guide
가상환경 생성 후, 터미널에서 다음을 실행하면 pre-commit 설정 가능합니다.

    pip install -r requirements.txt (requirements.txt 위치 주의)
    npm install
    npm run prepare (team7-server로 이동하여 실행해야 함)




