# Time-Series-Dataset-Survey-4-Forecasting-with-Deep-Learning

## Install venv
````bash
pip install -r requirements.txt
````

## Dataset Table
|   ID | Domain                | Data Structure   |  File Format   |  Data Points   | Dimensions   | Time interval           |
|-----:|:----------------------|:-----------------|:---------------|:---------------|:-------------|:------------------------|
|    0 | Windspeed             | (-/-/-)          | csv            | 105,119        | 51           | 5min                    |
|    1 | Electricity           | (-/-/-)          | csv            | 105,119        | 31           | 5min                    |
|    2 | Air Quality           | (+/+/+)          | csv            | 43,824         | 12           | 1h                      |
|    3 | Electricity           | (+/+/+)          | csv            | 2,075,259      | 8            | 1min                    |
|    4 | Air Quality           | (+/+/+)          | xlsx           | 9,471          | 16           | 1h                      |
|    5 | Air Quality           | (+/+/+)          | csv            | 2,891,393      | 7            | 1h                      |
|    6 | Traffic               | (+/o/-)          | txt            | 3,997,413      | 11           | 1h                      |
|    7 | Crime                 | (+/+/+)          | csv            | 2,678,959      | 15           | irregular               |
|    8 | Weather               | (+/+/+)          | txt            | 2,764          | 24           | 15min                   |
|    9 | Ozone Level           | (+/o/+)          | csv            | 2,536          | 74           | 1h                      |
|   10 | Fertility             | (+/+/+)          | rda            | 574            | 4            | 1yr                     |
|   11 | Mortality             | (+/+/+)          | csv            | 21,201         | 8            | 1yr                     |
|   12 | Weather, Bike-Sharing | (+/+/+)          | csv            | 731            | 15           | 1d                      |
|   13 | Weather, Bike-Sharing | (+/+/+)          | csv            | 17,379         | 16           | 1h                      |
|   14 | Electricity, Weather  | (+/+/+)          | xlsx           | 713            | 3            | 1d                      |
|   15 | Weather               | (+/+/+)          | xlsx           | 15,072         | 12           | 1h                      |
|   16 | Machine Sensor        | (-/o/-)          | txt            | -              | -            | 100ms                   |
|   17 | AD Exchange Rate      | (+/o/+)          | csv            | 9,610          | 3            | 1h                      |
|   18 | Multiple              | (+/o/+)          | csv            | 69,561         | 3            | 5min                    |
|   19 | Traffic               | (+/o/+)          | csv            | 15,664         | 3            | 5min                    |
|   20 | Cloud Load            | (+/o/+)          | csv            | 67,740         | 3            | 5min                    |
|   21 | Tweet Count           | (+/o/+)          | csv            | 158,631        | 3            | 5min                    |
|   22 | Synthetic             | (+/+/-)          | mat            | -              | -            |                         |
|   23 | Electricity           | (+/-/-)          | txt            | 140,256        | 370          | 15min                   |
|   24 | Exchange Rate         | (+/-/-)          | txt            | 7,587          | 7            | 1d                      |
|   25 | Traffic               | (+/-/-)          | txt            | 17,543         | 861          | 1h                      |
|   26 | Solar                 | (+/-/-)          | txt            | 52,559         | 136          | 10min                   |
|   27 | Weather               | (+/+/+)          | csv            | -              | -            | 1min                    |
|   28 | Water Level           | (+/+/+)          | xlsx           | 36,160         | 4            | 1d                      |
|   29 | Air Quality           | (+/+/+)          | csv            | 420,768        | 19           | 15min                   |
|   30 | Air Quality           | (+/+/+)          | csv            | 79,559         | 11           | 15min                   |
|   31 | Crime                 | (+/+/+)          | csv            | 2,129,525      | 34           | 1min                    |
|   32 | Chemicals             | (+/+/+)          | xlsx           | 120,630        | 7            | 1min                    |
|   33 | Multiple              | (+/-/-)          | txt            | 71             | 110          | 1 M.                    |
|   34 | Multiple              | (+/+/+)          | txt            | 167,562        | 3            | 1yr, 1q, 1m             |
|   35 | Traffic               | (+/+/-)          | xls            | -              | -            | 1d                      |
|   36 | Tourism               | (+/-/-)          | csv            | 309            | 794          | 1m 1q                   |
|   37 | Web Traffic           | (+/+/+)          | csv            | 290,126        | 804          | 1d                      |
|   38 | Multiple              | (+/o/+)          | csv            | 414            | 960          | 1yr, 1q, 1m, 1w, 1d, 1h |
|   39 | Machine Sensor        | (+/+/+)          | csv            | 34,840         | 9            | 1h, 1m                  |
|   40 | Synthetic             | (-/-/-)          | pickle         | -              | -            |                         |
|   41 | Electricity           | (+/+/+)          | csv            | 4,055,880      | 6            | 5min, 1h                |
|   42 | Weather               | (+/+/+)          | csv            | 633,494,597    | 125          | 1yr                     |
|   43 | Electricity           | (+/-/+)          | csv            | 257,896        | 27           | 1h                      |
|   44 | Trajectory            | (+/+/+)          | txt            | 8,241,680      | 14           | 1s                      |
|   45 | Wind                  | (+/+/-)          | csv            | 262,968        | 254          | hourly                  |
|   46 | Bike-Usage            | (+/+/+)          | csv            | 52,584         | 5            | hourly                  |
|   47 | Electricity           | (+/+/+)          | csv            | 48,048         | 16           | hourly                  |
|   48 | Illness               | (+/+/+)          | csv            | 966            | 7            | weekly                  |
|   49 | Sales                 | (+/+/+)          | csv            | 1,058,297      | 9            | daily                   |
|   50 | Weather               | (+/+/+)          | csv            | 52,696         | 21           | 10min                   |
|   51 | Traffic               | (+/-/-)          | mat            | 57,636         | 48           | hourly                  |
|   52 | Weather               | (+/+/+)          | csv            | 35,064         | 12           | hourly                  |

## Links to the datasets
| ID                 |  Direct Link                                                                                                                                                                                                                  |
|:-------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0, 1               | {\url{https://github.com/chennnnnyize/Renewables\_Scenario\_Gen\_GAN/} (accessed on 1 March~2023)                                                                                                                             |
| 2                  | {\url{https://archive.ics.uci.edu/ml/datasets/Beijing+PM2.5+Data} (accessed on 1 March 2023)                                                                                                                                  |
| 3                  | {\url{https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption} (accessed on 1 March 2023)                                                                                                     |
| 4                  | \url{https://archive.ics.uci.edu/ml/datasets/Air+quality} (accessed on 1 March 2023)                                                                                                                                          |
| 5                  | \url{https://www.microsoft.com/en-us/research/publication/forecasting-fine-grained-air-quality-based-on-big-data/?from=http\%3A\%2F\%2Fresearch.microsoft.com\%2Fapps\%2Fpubs\%2F\%3Fid\%3D246398} (accessed on 1 March 2023) |
| 6                  | {\url{https://archive.ics.uci.edu/ml/datasets/PEMS-SF} (accessed on 1 March 2023)                                                                                                                                             |
| 7                  | \url{https://www.opendataphilly.org/dataset/crime-incidents} (accessed on 1 March 2023)                                                                                                                                       |
| 8                  | {\url{https://archive.ics.uci.edu/ml/datasets/sml2010} (accessed on 1 March 2023)                                                                                                                                             |
| 9                  | \url{http://archive.ics.uci.edu/ml/datasets/Ozone+Level+Detection} (accessed on 1 March 2023)                                                                                                                                 |
| 10, 11             | \url{https://github.com/robjhyndman/demography} (accessed on 1 March 2023)                                                                                                                                                    |
| 12, 13             | \url{https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset} (accessed on 1 March 2023)                                                                                                                                 |
| 14, 15             | \url{https://www.emc.ncep.noaa.gov/mmb/nldas/LDAS8th/forcing/forcing.shtml} (accessed on 1 March 2023)                                                                                                                        |
| 16                 | \url{http://www.cs.fit.edu/\textasciitilde pkc/nasa/data/} (accessed on 1 March 2023)                                                                                                                                         |
| 17, 18, 19, 20, 21 | \url{https://github.com/numenta/NAB} (accessed on 1 March 2023)                                                                                                                                                               |
| 22                 | \url{https://github.com/maziarraissi/DeepHPMs} (accessed on 1 March 2023)                                                                                                                                                     |
| 23                 | \url{https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014}                                                                                                                                                 |
| 24, 25, 26         | \url{https://github.com/laiguokun/multivariate-time-series-data} (accessed on 1 March 2023)                                                                                                                                   |
| 27                 | \url{https://zenodo.org/record/2826939\#.Ya9-JdDMI60} (accessed on 1 March 2023)                                                                                                                                              |
| 28                 | \url{https://data.mendeley.com/datasets/bhjgdhgzjr/1} (accessed on 1 March 2023)                                                                                                                                              |
| 29, 30             | \url{https://www.emc.ncep.noaa.gov/mmb/nldas/LDAS8th/forcing/forcing.shtml} (accessed on 1 March 2023)                                                                                                                        |
| 31                 | \url{https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports--Historical-2003/tmnf-yvry} (accessed on 1 March 2023)                                                                                           |
| 32                 | \url{https://zenodo.org/record/1306527\#.YXKIxxpBw60} (accessed on 1 March 2023)                                                                                                                                              |
| 33                 | \url{https://irafm.osu.cz/cif/main.php?c=Static\\&page=download} (accessed on 1 March 2023)                                                                                                                                   |
| 34                 | \url{https://forvis.github.io/datasets/m3-data/} (accessed on 1 March 2023)                                                                                                                                                   |
| 35                 | \url{http://www.neural-forecasting-competition.com/downloads/NNGC1/datasets/download.htm} (accessed on 1 March 2023)                                                                                                          |
| 36                 | \url{https://www.kaggle.com/competitions/tourism2/data?select=tourism2\_revision2.csv} (accessed on 1 March 2023)                                                                                                             |
| 37                 | \url{https://www.kaggle.com/competitions/web-traffic-time-series-forecasting/data?select=train\_1.csv.zip} (accessed on 1 March 2023)                                                                                         |
| 38                 | \url{https://github.com/Mcompetitions/M4-methods} (accessed on 1 March 2023)                                                                                                                                                  |
| 39                 | \url{https://github.com/zhouhaoyi/ETDataset} (accessed on 1 March 2023)                                                                                                                                                       |
| 40                 | \url{https://git.opendfki.de/koochali/forgan/-/tree/master/datasets/lorenz} (accessed on 1 March 2023)                                                                                                                        |
| 41                 | \url{https://www.nrel.gov/grid/solar-power-data.html} (accessed on 1 March 2023)                                                                                                                                              |
| 42                 | \url{https://github.com/yandex-research/shifts} (accessed on 1 March 2023)                                                                                                                                                    |
| 43                 | \url{https://kilthub.cmu.edu/articles/dataset/Data\_Collected\_with\_Package\_Delivery\_Quadcopter\_Drone/12683453/1} (accessed on 1 March 2023)                                                                              |
| 44                 | \url{https://theairlab.org/trajair/\#download} (accessed on 1 March 2023)                                                                                                                                                     |
| 45                 | \url{https://www.kaggle.com/sohier/30-years-of-european-wind-generation} (accessed on 1 March 2023)                                                                                                                           |
| 46                 | \url{https://www.kaggle.com/datasets/city-of-seattle/seattle-burke-gilman-trail} (accessed on 1 March 2023)                                                                                                                   |
| 47                 | \url{https://data.mendeley.com/datasets/byx7sztj59/1} (accessed on 1 March 2023)                                                                                                                                              |
| 48, 49, 50, 51     | \url{https://drive.google.com/drive/folders/1ZOYpTUa82\_jCcxIdTmyr0LXQfvaM9vIy} (accessed on 1 March 2023)                                                                                                                    |
| 52                 | \url{https://drive.google.com/drive/folders/1ohGYWWohJlOlb2gsGTeEq3Wii2egnEPR} (accessed on 1 March 2023)                                                                                                                     |

## Compute Stats
### Compute ADF, AC, PRV
````bash
python compute_stat_measurements.py --config-file "data/example_config.json" --create-cleaned-version --compute-stats
````

### Compute MPdist
````bash
python compute_stat_measurements.py --config-file "data/example_config.json" --create-cleaned-version --compute-mpdist
````
### Example Config json
````json
{
  "ds_0": {
    "__file__": "ad_exchange.csv",
    "sort": "event",
    "Forecasting Values": ["value"]
  },
  "ds_1": {
    "__file__": "WTH.csv",
    "sort": "",
    "Forecasting Values": ["wetbulbcelsius"]
  }
}
````

