# Maktabkhooneh Course Downloader

I used to download maktabkhooneh courses using IDM on windows but then I switched to Ubuntu and I thought to myself, I am a programmer! I shall write a code for it!

In fact in writing a automated program is better than downloading episodes one by one, so I got into it and here is the result.

## Installation
First you need to download the repo in any way that is suitable for you but I recommend doing this:

```bash
git clone https://github.com/haadijafari/Maktabkhooneh_Course_Downloader.git
```
Enter the downloaded repository.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install project requirements.
(I recommend using a virtual environment)

```bash
pip install -r requirements.txt
```
selenium,
python-dotenv,
requests
will be installed.

Edit the [.env](https://pip.pypa.io/en/stable/) file and set these values:

```text
TESSERA=Your account email or phone number (username for login)
PASSWORD=Your account password
URL=URL to the desired course
COURSE_NAME=Your Course name
# course name will used to name a folder to save the videos in that folder

```

## Usage
You can run the project using this command:

```bash
python maktab.py
```
if you don't have the download option in the choosen course then run this command instead:
```bash
python maktab_noDownloadOption.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT License](https://choosealicense.com/licenses/mit/)
