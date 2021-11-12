import scrapy
from .utils import area_info, bearing_16_to_kr, data_to_one_down_float_str


class ForecastSpider(scrapy.Spider):
    name = "forecast"

    def start_requests(self):
        base_url = "https://marine.kma.go.kr/custom/leisure.pop?work=beach&id="
        urls = []
        for i in range(1, 26):
            # 김녕해수욕장 제외
            if i == 24:
                continue
            urls.append(f"{base_url}{i}")
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        try:
            beach_forecast_list = {
                "live_info": {},
                "forecast_info": {"short_term": {}, "sea_long_term": {}},
            }

            # Save area information
            beach = response.css("h1 > span::text").get()
            beach_forecast_list["beach"] = beach
            beach_forecast_list["region"] = area_info[beach][0]
            beach_forecast_list["ocean"] = area_info[beach][1]
            beach_forecast_list["beach_id"] = area_info[beach][2]

            # Save livecast information
            live_info = response.css(".port-weather-content-metric")
            buoy_live_info = live_info.css(".metric-table td::text").getall()

            beach_forecast_list["live_info"]["significant_wh"] = buoy_live_info[1]
            beach_forecast_list["live_info"]["max_wh"] = buoy_live_info[2]
            beach_forecast_list["live_info"]["average_wh"] = buoy_live_info[3]
            beach_forecast_list["live_info"]["wave_period"] = buoy_live_info[4]
            beach_forecast_list["live_info"]["water_temp"] = buoy_live_info[5]
            aws_live_info = live_info.css("#tbAws.metric-table td::text").getall()
            beach_forecast_list["live_info"]["prec_availability"] = aws_live_info[1]
            beach_forecast_list["live_info"]["prec_15"] = aws_live_info[2]
            beach_forecast_list["live_info"]["prec_60"] = aws_live_info[3]
            beach_forecast_list["live_info"]["prec_day"] = aws_live_info[4]
            beach_forecast_list["live_info"]["temp"] = data_to_one_down_float_str(
                aws_live_info[5]
            )
            beach_forecast_list["live_info"]["wind_direction"] = bearing_16_to_kr(
                aws_live_info[6]
            )
            beach_forecast_list["live_info"]["wind_speed"] = data_to_one_down_float_str(
                aws_live_info[7]
            )
            beach_forecast_list["live_info"]["humidity"] = data_to_one_down_float_str(
                aws_live_info[8]
            )
            beach_forecast_list["live_info"][
                "sea_level_pressure"
            ] = data_to_one_down_float_str(aws_live_info[9])

            # Save short-term surfing forecast information
            forecast_info = response.css(".metric-table.forecastNew3")

            hour_cnt_in_date = forecast_info.css(
                '[scope="colgroup"]::attr(colspan)'
            ).getall()
            date_list = forecast_info.css('[scope="colgroup"]::text').getall()
            dates = []
            for hour_cnt, date in zip(hour_cnt_in_date, date_list):
                dates += [date] * int(hour_cnt)
            beach_forecast_list["forecast_info"]["short_term"]["date"] = dates

            beach_forecast_list["forecast_info"]["short_term"][
                "time"
            ] = forecast_info.css(".time_hr::text").getall()[0:-1]
            beach_forecast_list["forecast_info"]["short_term"][
                "weather_img"
            ] = forecast_info.css(".PD_none img::attr(src)").getall()
            beach_forecast_list["forecast_info"]["short_term"][
                "prec_prob"
            ] = forecast_info.css("tbody tr:nth-child(4) td::text").getall()
            beach_forecast_list["forecast_info"]["short_term"][
                "prec"
            ] = forecast_info.css("tbody tr:nth-child(5) td::text").getall()
            beach_forecast_list["forecast_info"]["short_term"][
                "temp"
            ] = forecast_info.css(".minus::text").getall()[0:-1]
            beach_forecast_list["forecast_info"]["short_term"][
                "wind_direction"
            ] = forecast_info.css(".wind img::attr(style)").getall()[0:-1]
            beach_forecast_list["forecast_info"]["short_term"][
                "wind_speed"
            ] = forecast_info.css(".wind_ws::text").getall()[0:-1]
            beach_forecast_list["forecast_info"]["short_term"][
                "humidity"
            ] = forecast_info.css(".humidity p.content::text").getall()[0:-1]
            beach_forecast_list["forecast_info"]["short_term"][
                "wh"
            ] = forecast_info.css(".content::text").getall()[17:]

            # Save sea forecast information
            sea_forecast_info = response.css(".port-weather-warning div:nth-child(4)")

            date_cnt = sea_forecast_info.css("[colspan]::attr(colspan)").getall()
            date_list = sea_forecast_info.css("[colspan]::text").getall()
            dates = []
            for cnt, date in zip(date_cnt, date_list):
                dates += [date] * int(cnt)
            beach_forecast_list["forecast_info"]["sea_long_term"]["date"] = dates
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "hour"
            ] = sea_forecast_info.css("thead tr:nth-child(2) th::text").getall()
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "wave_period"
            ] = sea_forecast_info.css("tbody tr:nth-child(1) p::text").getall()
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "wave_direction"
            ] = sea_forecast_info.css("tbody tr:nth-child(2) img::attr(style)").getall()
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "wh"
            ] = sea_forecast_info.css("tbody tr:nth-child(3) p::text").getall()
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "water_temp"
            ] = sea_forecast_info.css("tbody tr:nth-child(4) p::text").getall()

            # Save ultraviolet index forecast information
            uv_forecast_info = response.css(".port-weather-warning div:nth-child(10)")
            beach_forecast_list["forecast_info"]["sea_long_term"][
                "uv_idx"
            ] = uv_forecast_info.css("th::text").get()

            yield beach_forecast_list

        except Exception as e:
            return
