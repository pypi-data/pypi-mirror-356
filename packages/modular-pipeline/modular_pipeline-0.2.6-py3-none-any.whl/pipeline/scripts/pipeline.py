import os

import sys

import pandas as pd
import matplotlib

from pyairtable import Api
from dotenv import load_dotenv
import streamlit as st

from pipeline.scripts.pipeline_utils import save_csv, get_table,airtable_to_df,response_to_df,run_report, main,retrieve_submissions_data, convert_to_dataframe

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json

import datetime as dt
from datetime import datetime
from datetime import timedelta

load_dotenv()

class data_pipeline():
    def __init__(self,submission_directory,
                 save_directory, use_cached_data=False, credentials=None, token=None, sheets_credentials=None):
        self.submission_records = None
        self.substack_data = None
        self.use_cached_data = use_cached_data
        self.credentials = credentials
        self.token = token
        self.sheets_credentials = sheets_credentials
        
        # Get the current working directory
        current_dir = os.getcwd()  # Gets the current working directory
        
        # Construct the submission directory as a variable
        self.submission_directory = submission_directory
        print(f'self.submission_directory:{self.submission_directory}')

        self.save_directory = save_directory
        print(f'self.save_directory:{self.save_directory}')

        self.twitter_data = None


    def set_use_cached_data(self, use_cached_data):
        self.use_cached_data = use_cached_data

    def save_data(self, data_struct, file):  
        # Define a custom serializer to handle Timestamp objects
        def custom_serializer(obj):
            if isinstance(obj, (pd.Timestamp, datetime)):
                return obj.isoformat()  # Convert Timestamp to string in ISO format
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        # Set the directory to 'pipeline/data/cleaned/'
        directory = self.save_directory

        if not os.path.exists(directory):
            os.makedirs(directory)

        path = os.path.join(directory, file)
        print(f'path: {path}')

        if file.endswith('.json'):
            if isinstance(data_struct, dict):
                # Log any None values for debug visibility
                for key, df in data_struct.items():
                    if df is None:
                        print(f"❗ Data for '{key}' is None. Check the corresponding sheet or data source.")

                # Safely convert to JSON-compatible format
                json_data_struct = {
                    key: df.to_dict(orient='records') if df is not None else []
                    for key, df in data_struct.items()
                }

                with open(path, 'w') as f:
                    json.dump(json_data_struct, f, indent=4, default=custom_serializer)
            else:
                raise ValueError("data_struct must be a dictionary for JSON saving.")

        elif file.endswith('.csv'):
            if isinstance(data_struct, pd.DataFrame):
                data_struct.to_csv(path, index=False)
            else:
                raise ValueError("data_struct must be a DataFrame for CSV saving.")

    def load_data(self,file):
        directory = self.save_directory
        path = os.path.join(directory, file)

        # Load data from JSON file
        if file.endswith('.json'):
            with open(path, 'r') as f:
                json_data = json.load(f)
                # Convert the JSON data back to a dictionary of DataFrames
                data_struct = {key: pd.DataFrame(value) for key, value in json_data.items()}
                return data_struct

        # Load data from CSV file
        elif file.endswith('.csv'):
            # Load the CSV into a DataFrame
            data_frame = pd.read_csv(path)
            return data_frame  # Return the DataFrame directly

        else:
            raise ValueError("Unsupported file format. Please provide a .json or .csv file.")

    def get_airtable_data(self, cached_data=False):

        if cached_data:
            return self.load_data('airtable_data.json') 

        if self.use_cached_data:
            return self.load_data('airtable_data.json')
        
        api = Api(os.environ['AIRTABLE_API_KEY'])

        submissions_records = get_table(api,os.environ['BASEID'], os.environ['TABLEID1'])
        submissions_records_df = airtable_to_df(submissions_records)

        contributor_records = get_table(api,os.environ['BASEID'], os.environ['TABLEID2'])
        contributor_records_df = airtable_to_df(contributor_records)

        project_records = get_table(api,os.environ['BASEID'], os.environ['TABLEID3'])
        project_records_df = airtable_to_df(project_records)

        data_struct = {
            "project_records": project_records_df,
            "contributor_records": contributor_records_df,
            "submissions_records": submissions_records_df
        }

        self.submission_records = submissions_records_df

        self.save_data(data_struct,'airtable_data.json')

        return data_struct
    
    def get_google_analytics_data(self, cached_data=False):

        if cached_data:
            return self.load_data('google_analytics.json')

        if self.use_cached_data:
            return self.load_data('google_analytics.json')

        GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        property_id = os.getenv('property_id') or st.secrets.get('property_id')

        twenty_eight_days = str(dt.date.today() - timedelta(28))
        seven_days = str(dt.date.today() - timedelta(7))
        twelve_months = str(dt.date.today() - timedelta(365))
        today = str(dt.date.today())

        cities = run_report(property_id,dimension="cityid",metric="activeUsers", credentials_json=self.credentials)
        users_timeseries = run_report(property_id,dimension="date",metric="activeUsers")

        new_v_return_7d = run_report(property_id,dimension='newVsReturning',metric='active7DayUsers',start_date=today)
        new_v_return_7d = new_v_return_7d[new_v_return_7d['newVsReturning'] != '']

        new_v_return_28 = run_report(property_id,dimension='newVsReturning',metric='active28DayUsers',start_date=today)
        new_v_return_28 = new_v_return_28[new_v_return_28['newVsReturning'] != '']

        devices_7d = run_report(property_id,dimension='platformDeviceCategory',metric='active7DayUsers',start_date=today)

        devices_28d = run_report(property_id,dimension='platformDeviceCategory',metric='active28DayUsers',start_date=today)

        devices_at = run_report(property_id,dimension='platformDeviceCategory',metric='activeUsers')

        source_7d = run_report(property_id,dimension='firstUserDefaultChannelGroup',metric='active7DayUsers',start_date=today)

        source_28d = run_report(property_id,dimension='firstUserDefaultChannelGroup',metric='active28DayUsers',start_date=today)

        source_at = run_report(property_id,dimension='firstUserDefaultChannelGroup',metric='activeUsers')

        views_7d = run_report(property_id,dimension='unifiedScreenClass',metric='screenPageViews', start_date=seven_days)

        views_28d = run_report(property_id,dimension='unifiedScreenClass',metric='screenPageViews', start_date=twenty_eight_days)

        views_at = run_report(property_id,dimension='unifiedScreenClass',metric='screenPageViews')

        new_v_return_timeseries = run_report(property_id,dimension="date",metric="newUsers")

        source_sessions_at = run_report(property_id,dimension='Sessionsource',metric='active28DayUsers')

        source_sessions_28d = run_report(property_id,dimension='Sessionsource',metric='activeUsers',start_date=twenty_eight_days)

        source_campaign_7d = run_report(property_id,dimension='sessionCampaignName',metric='active7DayUsers',start_date=today)

        source_campaign_28d = run_report(property_id,dimension='sessionCampaignName',metric='active28DayUsers',start_date=today)

        data_struct = {
            "cities": cities,
            "users_timeseries": users_timeseries,
            "new_v_return_7d": new_v_return_7d,
            "new_v_return_28d": new_v_return_28,
            "devices_7d": devices_7d,
            "devices_28d": devices_28d,
            "devices_at":devices_at,
            "source_7d":source_7d,
            "source_28d":source_28d,
            "source_at":source_at,
            "views_7d":views_7d,
            "views_28d":views_28d,
            "views_at":views_at,
            "new_v_return_timeseries":new_v_return_timeseries,
            "source_sessions_at":source_sessions_at,
            "source_sessions_28d":source_sessions_28d,
            "source_campaign_28d":source_campaign_28d,
            "source_campaign_7d":source_campaign_7d
        }

        self.save_data(data_struct,'google_analytics.json')

        # data_struct = self.load_data('google_analytics.json')

        return data_struct

    def get_sheets_data(self, cached_data=False):

        if cached_data:
            return self.load_data('google_sheets.json')
        
        SPREADSHEET_ID = os.getenv('SPREADSHEET_ID') or st.secrets.get('SPREADSHEET_ID')
        SCOPES = [os.getenv('SCOPES') or st.secrets.get('SCOPES')]

        if self.use_cached_data:
            return self.load_data('google_sheets.json')

        # Google Sheets API; includes Ghost NL Data
        log_df = main(SPREADSHEET_ID=SPREADSHEET_ID,
                      SCOPES=SCOPES,
                      SHEET_NAME="Issue Log Data",
                      skip_first_row=True,
                      creds_json=self.sheets_credentials,
                      token_json=self.token
                      )
        
        subscriber_df = main(SPREADSHEET_ID=SPREADSHEET_ID,
                      SCOPES=SCOPES,
                      SHEET_NAME='Ghost Subs',
                      skip_first_row=False,
                      creds_json=self.sheets_credentials,
                      token_json=self.token)
        
        print(f'subscriber_df: {subscriber_df}')
        # import pdb; pdb.set_trace()
        
        issue_df = main(SPREADSHEET_ID=SPREADSHEET_ID,
                      SCOPES=SCOPES,
                      SHEET_NAME='Issue CSV',
                      skip_first_row=False,
                      creds_json=self.sheets_credentials,
                      token_json=self.token)

        ON_twitter = main(SPREADSHEET_ID=SPREADSHEET_ID,
                      SCOPES=SCOPES,
                      SHEET_NAME='ON Twitter CSV',
                      skip_first_row=False,
                      creds_json=self.sheets_credentials,
                      token_json=self.token)
        
        Spencer_twitter = main(SPREADSHEET_ID=SPREADSHEET_ID,
                      SCOPES=SCOPES,
                      SHEET_NAME='Spencer Twitter CSV',
                      skip_first_row=False,
                      creds_json=self.sheets_credentials,
                      token_json=self.token)
        
        per_tweet = main(SPREADSHEET_ID=SPREADSHEET_ID,
                            SCOPES=SCOPES,
                            SHEET_NAME='ON Per Tweet CSV',
                            skip_first_row=False,
                            creds_json=self.sheets_credentials,
                            token_json=self.token)
        
        substack = main(SPREADSHEET_ID=SPREADSHEET_ID,
                            SCOPES=SCOPES,
                            SHEET_NAME='Substack Subs',
                            skip_first_row=False,
                            creds_json=self.sheets_credentials,
                            token_json=self.token)
        
        data_struct = {
            "log_df":log_df,
            "subscriber_df":subscriber_df,
            "issue_df":issue_df,
            "ON_twitter":ON_twitter,
            "Spencer_twitter":Spencer_twitter,
            'per_tweet':per_tweet,
            'substack': substack
        }

        twitter_data = {
            "ON_twitter":ON_twitter,
            "Spencer_twitter":Spencer_twitter,
            'per_tweet':per_tweet
        }

        print(f'data_struct: {data_struct}')

        # import pdb; pdb.set_trace()

        for key in data_struct.keys():
            print(data_struct[key])

        self.save_data(data_struct,'google_sheets.json')

        self.twitter_data = twitter_data
        self.substack_data = substack

        return data_struct
    
    def get_twitter_data(self, cached_data=False):
        # For now we get from local folder

        if cached_data:

            sheets = self.load_data('google_sheets.json')
            ON_twitter = sheets['ON_twitter']
            Spencer_twitter = sheets['Spencer_twitter']

            twitter_data = {
            "ON_twitter":ON_twitter,
            "Spencer_twitter":Spencer_twitter
            }
        
        else:

            SPREADSHEET_ID = os.getenv('SPREADSHEET_ID') or st.secrets.get('SPREADSHEET_ID')
            SCOPES = [os.getenv('SCOPES') or st.secrets.get('SCOPES')]

            ON_twitter = main(SPREADSHEET_ID=SPREADSHEET_ID,
                        SCOPES=SCOPES,
                        SHEET_NAME='ON Twitter CSV',
                        skip_first_row=False)
            
            Spencer_twitter = main(SPREADSHEET_ID=SPREADSHEET_ID,
                        SCOPES=SCOPES,
                        SHEET_NAME='Spencer Twitter CSV',
                        skip_first_row=False)
            
            per_tweet = main(SPREADSHEET_ID=SPREADSHEET_ID,
                            SCOPES=SCOPES,
                            SHEET_NAME='ON Per Tweet CSV',
                            skip_first_row=False)
            
            twitter_data = {
                "ON_twitter":ON_twitter,
                "Spencer_twitter":Spencer_twitter,
                'per_tweet':per_tweet
            }

        return twitter_data
    
    def get_substack_data(self, path1=None, path2=None, cached_data=False):
        """
        Retrieves the Substack data. If `cached_data=True`, loads it from `google_sheets.json`.
        Otherwise, returns the `substack` DataFrame loaded via `get_sheets_data`.

        Optionally, can also load from CSV paths `path1` and `path2` if needed.
        """
        if cached_data or self.use_cached_data:
            sheets_data = self.load_data('google_sheets.json')
            substack_df = sheets_data.get("substack")
            return {substack_df}

        if self.substack_data is not None:
            return {self.substack_data}

        if path1 and path2:
            substack1 = pd.read_csv(path1)
            substack2 = pd.read_csv(path2)

            data_struct = {
                'substack1': substack1,
                'substack2': substack2
            }

            return data_struct

        # Fallback: reload sheets if nothing else is available
        sheets_data = self.get_sheets_data()
        substack_df = sheets_data.get("substack")
        return {substack_df}
    
    def get_submissions(self, start_date, end_date):
        # Use the current directory as the base if submission_directory is not provided
        self.get_airtable_data()
        
        if self.use_cached_data:
            data = self.load_data('airtable_data.json')
            self.submission_records = data['submissions_records']

        submissions = retrieve_submissions_data(self.submission_records, start_date, end_date, self.submission_directory)
        return submissions














    