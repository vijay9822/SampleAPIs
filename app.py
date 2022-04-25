from flask import Flask
import pandas as pd
from datetime import date

app = Flask(__name__)
app.config["DEBUG"] = True


def read_csv():
    return pd.read_csv('Players.csv')

def remove_null(df, col, flag):
    if flag == 0:
        return df[df[col].notna()]
    elif flag == 1:
        return df.dropna(subset=col, thresh=1)
    elif flag == 2:
        return df[df[col].isnull()]



@app.route('/')
def home():
    return "<h2>Hey Hooman! please read me</h2><h4>*copy and paste these URL's to get them to work*</h4><h4>*I wasn't that perfect to create hypertexts sorry for the inconvinience ;)*</h4><h4>** / at the end of URL mean it's expecting one input**</h4><p>http://localhost:5000/players-on-or-after/<year></p><p>http://localhost:5000/avg-age-of-players-in-different-teams</p><p>http://localhost:5000/max-left-handed-in-country</p><p>http://localhost:5000/country-null</p><p>http://localhost:5000/players-in-country/<country><p/>"


@app.route('/players-on-or-after/<year>')
def players_on_or_after(year):
    df = read_csv()
    names = []
    df = remove_null(df, 'DOB', 0)
    [names.append(row["Player_Name"]) if row['DOB'][-2:] >= year[-2:] else None for index, row in df.iterrows()]
    return "players percentage born on or after {} is: {}".format("19"+year[-2:], (len(names)/len(df))*100)


@app.route('/avg-age-of-players-in-different-teams')
def avg_age_of_players_in_different_teams():
    df = read_csv()
    df = remove_null(df, 'DOB', 0)
    age = []
    for index, row in df.iterrows():
        age.append(date.today().year - int("19" + row['DOB'][-2:]))
    df['Age'] = age
    dct = {k: v["Age"].tolist() for k, v in df.groupby("Country")}
    new_dct = {}
    for con, ages in dct.items():
        new_dct[con] = sum(ages) // len(ages)
    return "Average age in every team: {}".format(new_dct)


@app.route('/max-left-handed-in-country')
def max_left_handed_in_country():
    df = read_csv()
    df = remove_null(df, ['Batting_Hand', 'Country'], 1)
    d = {k: v.value_counts(sort=False).to_dict() for k, v in df.groupby('Country', sort=False)['Batting_Hand']}
    max_num = 0
    country = ''
    for k1, v1 in d.items():
        if v1.get('Left_Hand') is not None and max_num < v1.get('Left_Hand'):
            max_num = v1.get('Left_Hand')
            country = k1
    return "{} has max number of {} left hand batsmen.".format(country, max_num)


@app.route('/country-null')
def country_null():
    df = read_csv()
    names = []
    df = remove_null(df, 'Country', 2)
    [names.append(row["Player_Name"]) for index, row in df.iterrows()]
    return "These players don't have country specified in data set: {}".format(names)


@app.route('/players-in-country/<country>')
def players_in_country(country):
    country = country[0:1].upper() + country[1:]
    df = read_csv()
    df = remove_null(df, 'Country', 0)
    dct = {k: v["Player_Name"].tolist() for k, v in df.groupby("Country")}
    return "players from {} are: {}".format(country, dct.get(country))


if __name__ == "__main__":
    app.run()
