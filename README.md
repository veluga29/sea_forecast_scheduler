# Sea Forecast Service - Scheduled Crawler

:page_facing_up: Personal project / :date: 2021.10 - 2021.11 

원하는 해변의 기상 정보 조회를 제공하는 Sea Forecast Service의 Scheduled Crawler part입니다.

​    

## :bookmark: Tech stack

* Python 3.9
* Scrapy 2.5
* Celery 5.2
* RabbitMQ 5.0
* Heroku 

​    

## :bookmark: Core features

### :paperclip: Scrapy

- `ForecastSpider` :pushpin: [코드 확인](https://github.com/veluminous/sea_forecast_scheduler/blob/ecee40917977bf61963e384a4c5fd65475438adb/beach_forecast_scraper/spiders/forecast_spider.py#L5)

  - Scrapy로 기상청의 서핑 해수욕장 기상 정보를 크롤링하는 spider 클래스를 구현했습니다.
  - `https://marine.kma.go.kr/custom/leisure.pop?work=beach&id=`에서 해변의 id만 변경하면서 크롤링합니다.
    - 24번을 제외한 1~26번 해변의 정보를 크롤링합니다. (24번 페이지는 빈 정보가 있어 생략했습니다.)
    - 각 해변의 중요 기상 정보를 파싱해 파이프라인으로 넘깁니다.

- `PostgreSQLPipeline` :pushpin: [코드 확인](https://github.com/veluminous/sea_forecast_scheduler/blob/ecee40917977bf61963e384a4c5fd65475438adb/beach_forecast_scraper/pipelines.py#L14)

  - 크롤링한 정보를 Psycopg2 라이브러리로 PostgreSQL DB에 저장하는 pipeline 클래스를 구현했습니다.

  - `BeachForecastList` 테이블에는 최신 기상 정보만 담기도록 쿼리를 짰습니다.

  - `BeachForecastListHistory` 테이블에는 지속적으로 기상 정보가 쌓이도록 쿼리를 짰습니다.

    > :bulb: Reference: [Store Scrapy crawled data in PostgresSQL](https://medium.com/codelog/store-scrapy-crawled-data-in-postgressql-2da9e62ae272)


​    

### :paperclip: Celery

* `tasks.py` :pushpin: [코드 확인](https://github.com/veluminous/sea_forecast_scheduler/blob/ecee40917977bf61963e384a4c5fd65475438adb/tasks.py#L17)

  - 브로커로 RabbitMQ를 사용했습니다.

  - Scrapy의 저수준 API `Crawler`를 사용해 스크립트에서 scrapy를 실행할 수 있도록 했습니다.

    > :bulb: Reference: [Running Scrapy In Celery Tasks](https://codeburst.io/running-scrapy-in-celery-tasks-d81e159921ea)

  - Celery 서버를 실행해두면 Celery beat이 1시간에 한 번씩 `run_scraper_task` 크롤링 작업을 메시지 큐에 던져 실행하도록 구현했습니다.

​    

## :bookmark: Trouble shooting

* 페이지의 특정 부분에 대하여 크롤링이 잘 이루어지지 않는 문제 :pushpin: [코드 확인](https://github.com/veluminous/sea_forecast_scheduler/blob/ecee40917977bf61963e384a4c5fd65475438adb/beach_forecast_scraper/spiders/utils.py#L29)
  * 풍향이 분명 string인데 number로 크롤링되는 현상이 발생했습니다.
  * 기온, 풍속, 습도, 해면기압이 소수점 형태의 number인데, 소수점 없이 크롤링되는 현상이 발생했습니다.
  * 클라이언트 측에서 어떤 처리가 있는지 의심했고, 네트워크 tab을 통해 특정 함수가 담긴 js파일을 확인했습니다.
  * 해당 js 파일의 알고리즘을 Python으로 옮겨 util로서 활용해 해결했습니다.
* Windows 환경에서 Celery 서버가 제대로 기능하지 않는 문제
  * `celery -A tasks worker -l INFO`로 서버를 실행하면, task를 메시지 큐에 던져도 작업이 완료되지 않는 문제가 발생했습니다.
  * Windows의 경우, Celery 4.x부터 공식적으로 지원하지 않아 오류가 잦아 보였습니다. ([Celery docs](https://docs.celeryproject.org/en/master/faq.html?highlight=windows#does-celery-support-windows))
  * `celery -A tasks worker -l INFO -P threads`로 서버를 실행하면, 메시지 큐에 던진 작업이 완료되는 것을 확인했습니다.
  * 로컬(Windows) 환경에서는 `-P threads` 옵션을 붙이고, Heroku에서는 해당 옵션 없이 실행하는 방식으로 해결했습니다.

