# A DRIVER LICENSE SCANNER APP

- How to run de app:

1. Download the repo
2. If you don't have Python and pipenv installed, install Python and pipenv
3. Run `pipenv install` to install all dependencies under the root folder
4. Run `flask --app index run` under the root folder

- This app supports the newest Missouri dl by default
  [accepted MO DL format](https://www.fourstateshomepage.com/wp-content/uploads/sites/36/2020/06/Class-F-REAL-ID-Samantha-Driver.jpg)
- To add support for other states, follow the steps below
  1. Download a nice scanned image of the desired state's DL
  2. Use the `getRawData(path, type='upload')` function to process your scanned image. Print the returned data
  3. In the returned data, find the element that contains the state name and all the elements/fields that needs to be extracted. If the element/field is divided into several boxes, you only need the first one from the left
  4. In the config.py file, add your data from step 4 to `STATE_COORDINATES`, follow the exisiting format
  5. In the config.py file, add new allowed deviation settings to `STATE_DEVIATIONS`, follow the existing format. This numbers can be different for different states depending on the layout of the DL. You might need to do some trial and error to find the best setting
  6. run the app
