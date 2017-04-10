# wchatOA
WeChat Official Accounts Developer Mode

## How to Use ？
1. Modify the local path and url in scihub.py to localizate this APP.
2. Use `python main.py 80` or `nohup python main.py 80 > log 2>&1 &` or just `sh app.sh` to run.


## History
- version 0.1.2 - 2017/04/10
1. fix some bugs due to wrong url captured from sci-hub.cc
2. add dx.doi.org database to achive url source, when getting NULL file from sci-hub.cc

- version 0.1.0 - 2017/03/30
1. Initialize the development server
2. Support downloading paper and return dowload_url, with 'paper doi_id'
3. Support automatically Email to User, with 'paper doi_id email usr_email_list'
4. Include papers in sci-hub.cc and some Free Journals (such as eLife, Oncotarget and so on)
