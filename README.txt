IMPORTANT: run data_preprocessing.ipynb first. bar_plot.ipynb are to be run before clustering.ipynb 

titles_mod.csv is a legacy file
titles_mod2.csv is the preprocessed data

data_preprocessing.ipynb uses linear regression to impute missing scores, votes and popularity values.
It also merges credit.csv and titles.csv into one dataframe.
Lastly, it case strip, remove punctations, tokenise and perform stemming on descriptions of movies.
The dataframe will be outputed as titles_mod2.csv

'countries.ipynb' provides a detailed data analysis and visualization methodology for exploring IMDB scores and movie production data, 
with a focus on production countries. The code performs the following steps:
    1. The code defines 'imdb_score' as the feature of interest and 'production_countries' as the group-by column. 
    It calculates and visualizes the average IMDB scores for the original production country dataset, presenting the top countries 
    in a bar chart, ana also further enriches the analysis by calculating the count of movies produced per country (not by an
    individual country)

    2. The methodology extends to explore individual production countries' IMDB scores, which means that the list of production countries
    is equal to 1. It calculates average IMDB scores again as before and introduces a count of movies produced per country. The resulting 
    bar chart provides insights into the performance of individual countries

    3. The code filters out lists where 'production_countries' is an empty list and calculates the median IMDB score for each 
    production country. It also determines the count of movies produced per country while filtering for countries with more than 5 movies,
    since when it is less than 5, the data is not worth studying. The analysis includes a box plot that visually represents IMDB scores 
    for these selected countries, with a red dashed line indicating the overall median IMDb score


actor.ipynb is used to calculate the pearson coefficients between the imdb_score of a movie and the average "actor" or "director" scores 
of each movie's cast.

It does this by first processing the actors/directors into an array, which is then iterated over to calculate the average imdb score for 
each actor or director.

The scores are then put in the form of a pandas dataframe, which is then used to find the pearson coefficient.


The purpose of the bar_plot.ipynb is to create various kinds of bar plots so that we can visualize some aspects of the data.
These includes bar plots of runtime of all genres, Average IMDB scores of all genres, and
finally, the bar plot of Average vote of every genres that will be important in the clustering.ipynb program


For clustering.ipynb, it creates runtime clustering for each top  4 genres by using the VAT technique.
Additionally, pearson correlation score and clusteroid of runtime and genre will be measured. 
Finally, plots of Calinski-Harabasz Indexes of each top 4 genres are made, however,
these plots are not used in the report.
