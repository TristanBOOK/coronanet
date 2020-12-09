import os
import pandas as pd
import ipdb

class Coronanet:

    def get_raw_data(self):
        raw_data_path = os.getenv('CORONANET_DATA')
        if raw_data_path:
            data_path = f'{raw_data_path}/csv/coronanet_release_allvars.csv'
            df = pd.read_csv(data_path, encoding='mac_roman')
            return df
        else:
            print("Create a env variable with this path $HOME/code/.../coronanet/data/")
            print('Add in .zshrc this line: export CORONANET_DATA="$HOME/code/.../coronanet/data/" ')
            return


    def get_data(self):
        """
        This function returns a Python dict.
        Its values should be pandas.DataFrame loaded from csv files
        """
        #ipdb.set_trace()
        path = os.path.abspath(__file__)
        path1 = os.path.dirname(os.path.dirname(path))
        csv_path = os.path.join(path1, 'data' ,'csv')
        #ipdb.set_trace()

        return df
        # Hints: Build csv_path as "absolute path" in order to call this method from anywhere.
        # Do not hardcode your path as it only works on your machine ('Users/username/code...')
        # Use __file__ as absolute path anchor independant of your computer
        # Make extensive use of `import ipdb; ipdb.set_trace()` to investigate what `__file__` variable is really
        # Use os.path library to construct path independent of Unix vs. Windows specificities


##if __name__ == '__main__':
#    # For introspections purpose to quickly get this functions on ipython
#    from coronanet.data import Coronanet
    #import coronanet.data
#    coronanet_instance = Coronanet()
#    df = coronanet_instance.get_raw_data()
#    print(df.head())



