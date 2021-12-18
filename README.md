# SubtitleFileTranslator


![translate_thumbnail](https://user-images.githubusercontent.com/76941589/145695538-728819cd-4dfb-4e8d-8306-16f4b25bc9c0.png)

Translate a Subtitle file from one language to another using the Google Translate API.

Features:

->Supports many languages as it uses the google API.

->Supports resuming as the API fails sometimes due to many requests.

->Supports record keeping on multiple subtitle files to be translated for better resuming.


Requirements:

Install the googletrans package via pip ( pip install googletrans )
Sometimes the googletrans package can throw an error, installing the alpha version will fix the problem -> ( pip install googletrans==4.0.0-rc1 )
