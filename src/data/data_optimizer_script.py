
import pandas as pd
import os



class dataframe_optimiser():
    def __init__(self, conversion):
        self.conversion = conversion

    def convert_series(self ,array_of_series):
        returned_series =[]
        for series in array_of_series:
            print("converting: " ,series.name ,"\t\t\tsize (MB):", round(series.memory_usage(deep=True) * 1e-6 ,2)
                  ,end="\t")
            #             series=eval("series"+test.conversion)
            series =eval(self.conversion)
            print("->\t", round(series.memory_usage(deep=True) * 1e-6 ,2))
            returned_series.append(series)
        return returned_series



def optimize_chunk(chunk,i,original_data_size,new_data_size):
    sample_data=chunk

    initial_memory_usage =sample_data.memory_usage(deep=True).sum() * 1e-6

    # instantiate category_converter object from dataframe_optimiser class
    timestamp_converter =dataframe_optimiser("pd.to_datetime(series)")
    # convert array of series from dataframe to optimised datatype
    [sample_data["timestamp"] ] =timestamp_converter.convert_series([sample_data["timestamp"]])

    # instantiate category_converter object from dataframe_optimiser class
    category_converter =dataframe_optimiser("series.astype('category')")
    # convert array of series from dataframe to optimised datatype
    [sample_data["title"] ,sample_data["world"] ,sample_data["event_code"] ,sample_data["event_count"]
     ,sample_data["installation_id"] ] =category_converter.convert_series \
        ([sample_data["title"] ,sample_data["world"] ,sample_data["event_code"] ,sample_data["event_count"]
         ,sample_data["installation_id"]])


    final_memory_usage =sample_data.memory_usage(deep=True).sum() * 1e-6
    print("The initial space on disk was (MB): " ,round(initial_memory_usage ,2) ," and the final space on disk is (MB): "
          ,round(final_memory_usage ,2))



    original_data_size+=initial_memory_usage
    new_data_size+=final_memory_usage

    return original_data_size,new_data_size,sample_data



i = 0

final_data=None
original_data_size=0
new_data_size=0
chunksize = 10 ** 6
for chunk in pd.read_csv("../../data/raw/train.csv", chunksize=chunksize):
    i += 1
    print(i)
    print(chunk.head())
    original_data_size, new_data_size,sample_data=optimize_chunk(chunk,i,original_data_size,new_data_size)
    print("The total original data size was: "+str(round(original_data_size,2))+" and the new total data size is: "+str(round(new_data_size,2)))
    if  i==1:
        final_data=sample_data
    final_data.append(sample_data)
    # if i == 2:
    #     break
# ### Store data as a pickle
    # By storing the data as a pickle, the size on disk is reduced to 67% of the original size, and loads 10x faster.
final_data.to_pickle("../../data/processed/memory_optimized_data.pkl")