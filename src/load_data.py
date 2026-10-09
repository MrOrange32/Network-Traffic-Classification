from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def load_data():
        
    df1 = pd.read_csv(DATA_DIR /"youtube1080.csv")
    df1["Label"] = "streaming"
 
    df2 = pd.read_csv(DATA_DIR /"youtube480.csv")
    df2["Label"] = "streaming"

    df3 = pd.read_csv(DATA_DIR /"youtube_jump_forward.csv")
    df3["Label"] = "streaming"

    df4 = pd.read_csv(DATA_DIR /"youtube_pause_play.csv")
    df4["Label"] = "streaming"

    df5 = pd.read_csv(DATA_DIR /"browsing_google.csv")
    df5["Label"] = "browsing"

    df6 = pd.read_csv(DATA_DIR /"browsing_columbia.csv")
    df6["Label"] = "browsing"

    df7 = pd.read_csv(DATA_DIR /"browsing_news.csv")
    df7["Label"] = "browsing"

    df8 = pd.read_csv(DATA_DIR /"browsing_scrolling.csv")
    df8["Label"] = "browsing"

    df9 = pd.read_csv(DATA_DIR /"file_download_5MB.csv")
    df9["Label"] = "file download"

    df10 = pd.read_csv(DATA_DIR /"file_download_50MB1.csv")
    df10["Label"] = "file download"

    df11 = pd.read_csv(DATA_DIR /"file_download_500MB2.csv")
    df11["Label"] = "file download"

    df_list = [df1,df2, df3,df4, df5,df6,df7,df8, df9, df10, df11]
    df = pd.concat(df_list, ignore_index=True)
    
    return df
