
# importing libraries

from flask import Flask, request, render_template, jsonify
import pandas as pd
import sys
import logging
from errors import InvalidUsage
import io


app = Flask(__name__) # initialising flask app

df_percent = pd.read_excel('zomato_processed.xlsx')

df_percent.set_index('name', inplace=True)

df_percent = df_percent.drop('Unnamed: 0', axis=1)

indices = pd.Series(df_percent.index)

df1 = pd.read_excel('similar_indices.xlsx')

df1 = df1.set_index('idx')

@app.route('/')
def home():
    '''
    template for home page
    '''
    return render_template('home.html')

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    '''
    handling errors
    '''
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/recommend', methods=['POST'])
def recommend():

    '''
    making recommendation based on the user's input
    '''
    
    recommend_restaurant = []
    name = request.form['Restaurant']

    # convering to lower case and then comparing to avoid case mismatches
    if name.lower() in (a.lower() for a in indices.values):
    
        idx = indices[indices == name.title()].index[0]

        
   
        top30_indexes = df1[df1.index==idx]['similar_indices'].values[0]
        value = top30_indexes

        # converting string to list
        if isinstance(value, str):
  
            temp=[]
            
            l=[]
            k=[]

            value = value.replace('[','').replace(']','').replace('\'','')
            l+=value.split(',')
            for i in l:
              k+=i.split(',')
            top30_indexes=k

        
        for each in top30_indexes:
            each = int(each)
        
            recommend_restaurant.append(list(df_percent.index)[each])
        
    
 
        df_new = pd.DataFrame(columns=['cuisines', 'mean_ratings', 'cost','location'])
    
   
        for each in recommend_restaurant:
            df_new = df_new.append(pd.DataFrame(df_percent[['cuisines','mean_ratings', 'cost','location']][df_percent.index == each].sample()))
    
        
        df_new = df_new.drop_duplicates(subset=['cuisines','mean_ratings', 'cost','location'], keep=False)
        df_new = df_new.sort_values(by='mean_ratings', ascending=False)
    
        
        df_new = df_new.rename(columns={'cuisines':'Cuisines','mean_ratings':'Average Normalized Rating on Zomato','cost':'Cost for 2 People', 'location':'Location'})
    
        return render_template('home.html',prediction_text='TOP %s RESTAURANTS LIKE %s WITH SIMILAR REVIEWS: ' % (str(len(df_new)), name.upper()) ,tables=[df_new.to_html(classes='data', header=True)])
    raise InvalidUsage('This Restaurant name does not exist. Kindly enter proper full name, eg : (Meghana Foods) instead of (Meghana)', status_code=410)


if __name__=='__main__':
    app.run()