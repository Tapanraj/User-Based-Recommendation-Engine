import math

from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:
    
    # class variables:    
    # none
    
    ##################################
    # class instantiation method - initializes instance variables
    #
    # usersItemRatings:
    # users item ratings data is in the form of a nested dictionary:
    # at the top level, we have User Names as keys, and their Item Ratings as values;
    # and Item Ratings are themselves dictionaries with Item Names as keys, and Ratings as values
    # Example: 
    #     {"Angelica":{"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
    #      "Bill":{"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}}
    #
    # k:
    # the number of nearest neighbors
    # defaults to 1
    #
    # m:
    # the number of recommedations to return
    # defaults to 10
    #
    def __init__(self, usersItemRatings, metric='pearson', k=1, m=10):
        
        # set self.usersItemRatings
        self.usersItemRatings = usersItemRatings
            
        # set self.k
        if k > 0:   
            self.k = k
        else:
            print ("    (FYI - invalid value of k (must be > 0) - defaulting to 1)")
            self.k = 1
         
        # set self.m
        if m > 0:   
            self.m = m
        else:
            print ("    (FYI - invalid value of m (must be > 0) - defaulting to 10)")
            self.m = 10
            

    #################################################
    # pearson correlation similarity
    # notation: if UserX is Angelica and UserY is Bill, then:
    # userXItemRatings = {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0, "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}
    # userYItemRatings = {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}
    def pearsonFn(self, userXItemRatings, userYItemRatings):
        
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        
        n = len(userXItemRatings.keys() & userYItemRatings.keys())
        
        for item in userXItemRatings.keys() & userYItemRatings.keys():
            x = userXItemRatings[item]
            y = userYItemRatings[item]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)
       
        if n == 0:
            print ("    (FYI - personFn n==0; returning -2)")
            return -2
        
        denominator = math.sqrt(sum_x2 - pow(sum_x, 2) / n) * math.sqrt(sum_y2 - pow(sum_y, 2) / n)
        if denominator == 0:
            print ("    (FYI - personFn denominator==0; returning -2)")
            return -2
        else:
            return round((sum_xy - (sum_x * sum_y) / n) / denominator, 2)
            

    #################################################
    # make recommendations for userX from the most similar k nearest neigibors (NNs)
    def recommendKNN(self, userX):
        
        # define dictionary user_pearson to store pearson correlation between two users
        # define dictionary normalised_dict to store normalised pearson correlation between two users
        user_pearson = {}
        normalised_dict = {}
        for userY in self.usersItemRatings.keys():
            if userY != userX:
               user_pearson[userY] = self.pearsonFn(self.usersItemRatings[userX], self.usersItemRatings[userY])
               normalised_dict[userY]= (user_pearson[userY]+1)/2
               
        # the below dictionary dict_similar_users stores the sorted similar users from most similar to least similar
        dict_similar_users = dict(sorted(normalised_dict.items(), key = itemgetter(1), reverse = True))
        
        # store value of k in n to use it in a loop
        n = self.k
        
        # corr_sum calculates the sum total factor that has to be divided to calculate weighted average
        corr_sum=0
        for names in dict_similar_users:
            if n == 0:  
                break
            corr_sum += dict_similar_users[names]
            n -= 1
        
        # weighted stores all the weighted ratings of k nearest neighbors
        weighted = {}
        
        # store value of k in n to use it in a loop
        n = self.k
        
        for names in dict_similar_users:
            if n == 0:  
                break
            weighted[names] = dict_similar_users[names]/corr_sum
            n -= 1
        
        # lst_songs is a set of all the songs that were rated by all users
        lst_songs = set()
        for k,v in self.usersItemRatings.items():
            lst_songs = lst_songs | v.keys()
        
        # Now I have converted lst_songs from a set to a list
        lst_songs = list(lst_songs)

        # ratt stores the calculated ratings according to the nearest neighbors
        ratt = {}
        for songs in lst_songs:
            rat = 0
            for user in weighted:
                if songs in self.usersItemRatings[user].keys():
                    rat += weighted[user] * self.usersItemRatings[user][songs]
            ratt[songs]=rat

        # final_recommendation stores the sorted final recommendation for each user
        final_recommendation = {}
        for song in ratt.keys():
            if (song not in self.usersItemRatings[userX].keys()) & (ratt[song] != 0):
                final_recommendation[song] = round(ratt[song],2)
        final_recommendation = dict(sorted(final_recommendation.items(), key = itemgetter(1), reverse = True))        
        
        # returning final_recommendation
        return final_recommendation
        
       


        
