# xero-app-scraper
Scrape the Xero UK Appstore

Collect next data for every app:
- Name of app
- Appstore URL
- App URL
- Root domain
- Reviews
- Reviews score
- Categories
- Added in year
- Support email

An example record is:
- Xavier Analytics
- https://apps.xero.com/uk/function/accountant-tools-extras/app/xavier-analytics
- https://xavier-analytics.com/xero
- xavier-analytics.com
- 36
- 5.0
- Accounting, Reporting, Accountant tools
- 2018
- support@xavier-analytics.com

___
## How it works

#### Step 1
After some investigation of the https://apps.xero.com/uk website I found out that every function/industry list page makes an API request. For example a request for 'Agriculture' industry apps:
```
https://apps.xero.com/api/apps/uk?industry=agriculture&pageSize=24
```

Without any parameter this API returns a list of apps splited by 50 apps per page.

This source allows to get almost all desired data:
![app_links](https://pai-pai-github-images.s3.amazonaws.com/xero-app-scraper-step-1.png)

#### Step 2
The collected at the previous step data contains a link to the each app page. These links are used to get missed in API data.

The result of this step is another csv file:
![app_details](https://pai-pai-github-images.s3.amazonaws.com/xero-app-scraper-step-2.png)

___
### Result:
After merge two csv data with help of pandas package the final file contains all of the desired data:
![xero_apps](https://pai-pai-github-images.s3.amazonaws.com/xero-app-scraper-result.png)

## Technology stack
- Scrapy
