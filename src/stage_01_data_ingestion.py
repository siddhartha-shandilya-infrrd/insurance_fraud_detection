import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from configs.config import ARTIFACTS, SOURCE_DATA_DIR, VALID_FILE_SCHEMA_PATH
from src.data_processing.data_validation import Raw_Data_Validation
from src.data_processing.data_transformation import Raw_Data_Transformation


STAGE = "stage_01_data_ingestion" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def dataValidation(valid_data_schema_path,remote_data_path):
    """
        Method Name: valid_data
        Description: This method validates the input data file based on "Schema" file.
        Output:Bolean -> whether the data file is valid or not
                                Written By: Siddhartha Shandilya
        Version: 1.0
        Revisions: None
        
    """
    data_validation = Raw_Data_Validation(remote_data_path, valid_data_schema_path)
    filename_pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,NumberofColumns,ColName = data_validation.get_value_from_schema()
    logging.info(f"we are getting followign scehma {filename_pattern},{LengthOfDateStampInFile},{LengthOfTimeStampInFile},{NumberofColumns},{ColName}")
    
    onlyfiles = [f for f in os.listdir(remote_data_path)]
    for filename in onlyfiles:
        raw_file_name_status = data_validation.raw_file_validation(filename, LengthOfDateStampInFile, LengthOfTimeStampInFile)
        if raw_file_name_status == 1:
            column_length_validaion_status = data_validation.raw_file_column_length_validation(NumberofColumns)
            if column_length_validaion_status == 1:
                column_name_validation_status = data_validation.raw_file_column_name_validation(colName=ColName)
                if column_name_validation_status == 1:
                    cloumn_missing_value_status = data_validation.validateMissingValuesInWholeColumn()
                    if cloumn_missing_value_status == 1:
                        logging.info(f"Raw Data Validation Completed for {filename}")
        else:
            logging.info(f"Raw Data Validation Failed for {filename}")


def dataTransformation():
    data_transformation = Raw_Data_Transformation()
    logging.info("Raw Data Transformation Started")
    data_transformation.replaceMissingWithNull()
    logging.info("!!!Raw Data Transformation Comleted !!!")

def main():
    ## read config files
    logging.info("Raw Data Validation Started")
    dataValidation(VALID_FILE_SCHEMA_PATH,SOURCE_DATA_DIR)
    #Raw Data Transformation Started
    dataTransformation()
    return 1


if __name__ == '__main__':
    
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e