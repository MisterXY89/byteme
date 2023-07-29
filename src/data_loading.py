import pandas as pd


def load_swipe_items(userMail="bwoollam1d@nytimes.com"):
    # exclude userMail from swipe_items
    df = pd.read_csv("data/MOCK_DATA.csv")
    print(df)
    print(df.columns)

    df = df[df["userMail"] != userMail].head(5)

    return df.to_dict(orient="records")


def save_swipe_preferences(swipe_dict):
    # save swipe_preferences to file using pandas
    df = pd.DataFrame(swipe_dict)
    print(df)
    df.to_csv("data/swipe_preferences.csv", index=False)


if __name__ == "__main__":
    swipe_items = load_swipe_items("bwoollam1d@nytimes.com")
    print(swipe_items)
