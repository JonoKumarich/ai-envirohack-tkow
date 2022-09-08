# AI EnviroHack - Te Korowai o Waiheke

This is part of our submission for the 2022 AIEnvirohack Hackathon. The repo contains a trained model that can be used for predicting the presence of a rat in an image.

# Installation
Clone the repo locally and run `$ pip install -r requirements.txt` on a fresh python virtual environment. 

# Command Usage Guide:

**1) Perform single prediction:**
    
`$ python main.py predict-image "<imagepath>"`

This method will output the probability of a single specified image containing a rat.

**2) Perform batch prediction:**
    
`$ python main.py batch-prediction "<filepath>"`

This method will output the probabilities of an image containing a rat for all photos contained inside a folder path.

`--save_results` can be added to save the output to a csv file.

**3) Re-fit the model:**
    
`$ python main.py update-model "<filepath>" --overwrite-model`

This command will update the model to incorporate newly collected and labeled data.

The filepath must point to a folder structure like the following:
```
<foldername>    
│
└───rat
│   │   img01.png
│   │   img02.png
│   │   ...
|
└───folder2
    │   img11.png
    │   img12.png
    │   ...

```

Images may be either .jpg or .png file types.









