import logging
import warnings
from datetime import timedelta

import pandas as pd

logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


def chunk_insulin_data(processed_basal: pd.DataFrame) -> pd.DataFrame:
    processed_basal = processed_basal.sort_values(by=['FADTC']).reset_index(drop=True)
    processed_basal['FADTC'] = pd.to_datetime(processed_basal['FADTC'])
    processed_basal['next_timestamp'] = processed_basal['FADTC'].shift(-1)
    processed_basal['FADUR'] = (processed_basal['next_timestamp'] - processed_basal['FADTC']).dt.total_seconds()
    processed_basal = processed_basal.dropna(subset=['FADUR']).reset_index(drop=True)
    processed_basal['insulin_per_second'] = processed_basal['commanded_basal_rate'] / 3600
    processed_basal['FASTRESN'] = processed_basal['insulin_per_second'] * processed_basal['FADUR']

    new_rows = []
    indices_to_remove = []

    for i in range(len(processed_basal)):
        row = processed_basal.iloc[i]

        if row['FADUR'] > 360:
            indices_to_remove.append(i)
            timestamp_current = row['FADTC']
            insulin_per_second = row['insulin_per_second']
            base_basal_rate = row['base_basal_rate']
            time_diff = row['FADUR']
            commanded_basal_rate = row['commanded_basal_rate']

            full_chunks = int(time_diff // 300)
            remainder = time_diff % 300
            for j in range(full_chunks):
                chunk_start = timestamp_current + pd.Timedelta(seconds=j * 300)
                chunk_insulin = insulin_per_second * 300
                new_rows.append({
                    'FADTC': chunk_start,
                    'FASTRESN': chunk_insulin,
                    'INSSTYPE': 'basal_chunk',
                    'FATEST': 'BASAL INSULIN',
                    'FACAT': 'BASAL',
                    'commanded_basal_rate': commanded_basal_rate,
                    'FADUR': 300,
                    'base_basal_rate': base_basal_rate
                })
            if remainder > 0:
                chunk_start = timestamp_current + pd.Timedelta(seconds=full_chunks * 300)
                chunk_insulin = insulin_per_second * remainder
                new_rows.append({
                    'FADTC': chunk_start,
                    'FASTRESN': chunk_insulin,
                    'INSSTYPE': 'basal_chunk',
                    'FATEST': 'BASAL INSULIN',
                    'FACAT': 'BASAL',
                    'commanded_basal_rate': base_basal_rate,
                    'FADUR': remainder,
                    'base_basal_rate': base_basal_rate
                })

    chunked_df = pd.DataFrame(new_rows)
    processed_basal = processed_basal.drop(index=indices_to_remove).reset_index(drop=True)
    if not processed_basal.empty:
        if 'INSSTYPE' not in processed_basal.columns:
            processed_basal['INSSTYPE'] = 'basal'
        if 'FATEST' not in processed_basal.columns:
            processed_basal['FATEST'] = 'BASAL INSULIN'
        if 'FACAT' not in processed_basal.columns:
            processed_basal['FACAT'] = 'BASAL'

    chunked_basal_df = pd.concat([processed_basal, chunked_df], ignore_index=True)
    chunked_basal_df = chunked_basal_df.sort_values(by=['FADTC']).reset_index(drop=True)
    if 'next_timestamp' in chunked_basal_df.columns:
        chunked_basal_df = chunked_basal_df.drop(columns=['next_timestamp'])
    if 'insulin_per_second' in chunked_basal_df.columns:
        chunked_basal_df = chunked_basal_df.drop(columns=['insulin_per_second'])
    return chunked_basal_df


def process_extended_bolus_group(group: pd.DataFrame) -> pd.DataFrame:
    group = group.sort_values('event_ts')

    original_value = float(group['original_value'].iloc[0])
    start_time = group['event_ts'].min()
    end_time = group['event_ts'].max()
    total_duration_seconds = (end_time - start_time).total_seconds()

    if total_duration_seconds == 0:
        group['delivered_total'] = original_value / len(group)
        return group

    insulin_per_second = original_value / total_duration_seconds

    time_intervals = []

    timestamps = sorted(group['event_ts'])

    if len(timestamps) > 0:
        first_interval = timestamps[0] - start_time
        time_intervals.append(first_interval.total_seconds())

    for i in range(1, len(timestamps)):
        interval = timestamps[i] - timestamps[i - 1]
        time_intervals.append(interval.total_seconds())

    delivered_amounts = [interval * insulin_per_second for interval in time_intervals]

    for i, amount in enumerate(delivered_amounts):
        group.iloc[i, group.columns.get_loc('delivered_total')] = amount

    return group


def preprocess_user_data(
        basal_df: pd.DataFrame,
        bolus_df: pd.DataFrame,
        carbs_df: pd.DataFrame,
        cgm_df: pd.DataFrame,
):
    # Process basal data
    basal_df['event_ts'] = pd.to_datetime(basal_df['event_ts'], format='%Y-%m-%d %H:%M:%S')
    basal_df = basal_df[['event_ts', 'commanded_basal_rate', 'base_basal_rate']]
    basal_df['event_ts'] = pd.to_datetime(basal_df['event_ts'], format='%Y-%m-%d %H:%M:%S')
    basal_df = basal_df.rename(columns={'event_ts': 'FADTC'})
    basal_df['INSSTYPE'] = 'basal'
    basal_df['FATEST'] = 'BASAL INSULIN'
    basal_df['FACAT'] = 'BASAL'
    processed_basal = basal_df.sort_values(by='FADTC')

    processed_basal = chunk_insulin_data(processed_basal)
    processed_basal = processed_basal[
        ['FADTC', 'FATEST', 'FACAT', 'FASTRESN', 'INSSTYPE', 'commanded_basal_rate', 'base_basal_rate', 'FADUR']]

    # Process bolus data
    bolus_df['event_ts'] = pd.to_datetime(bolus_df['event_ts'], format='%Y-%m-%d %H:%M:%S')
    bolus_df['INSSTYPE'] = bolus_df['requested_later'].apply(lambda x: 'extended' if x != 0 else 'normal')

    normal_bolus = bolus_df[(bolus_df['INSSTYPE'] == 'normal') & (bolus_df['bolus_delivery_status'] == 0)]
    normal_bolus = normal_bolus[['event_ts', 'bolus_id', 'delivered_total', 'INSSTYPE']].copy()
    normal_bolus['delivered_total'] /= 1000

    extended_bolus = bolus_df[bolus_df['INSSTYPE'] == 'extended'].copy()

    total_delivered = \
        extended_bolus[
            extended_bolus['bolus_delivery_status'] == "Bolus Completed"][
            ['bolus_id', 'delivered_total']]
    total_delivered = total_delivered.rename(columns={'delivered_total': 'original_value'})

    extended_bolus = extended_bolus[
        extended_bolus['bolus_delivery_status'] == "Bolus Started"]

    processed_extended_bolus_list = []

    for bolus_id in extended_bolus['bolus_id'].unique():
        group = extended_bolus[extended_bolus['bolus_id'] == bolus_id].copy()

        group = group.merge(total_delivered, on='bolus_id')

        processed_group = process_extended_bolus_group(group)
        processed_extended_bolus_list.append(processed_group)

    if processed_extended_bolus_list:
        extended_bolus = pd.concat(processed_extended_bolus_list)
    else:
        extended_bolus = pd.DataFrame(columns=extended_bolus.columns)

    extended_bolus['delivered_total'] /= 1000
    extended_bolus['original_value'] /= 1000

    extended_bolus = extended_bolus[['event_ts', 'bolus_id', 'delivered_total', 'original_value']]
    extended_bolus['INSSTYPE'] = 'extended'

    processed_bolus = pd.concat([normal_bolus, extended_bolus]).sort_values(by='event_ts')

    processed_bolus = processed_bolus.rename(columns={'event_ts': 'FADTC', 'delivered_total': 'INSNMBOL'})
    processed_bolus['FATEST'] = 'BOLUS INSULIN'
    processed_bolus['FACAT'] = 'BOLUS'

    processed_bolus['INSEXBOL'] = processed_bolus.apply(
        lambda row: row['INSNMBOL'] if row['INSSTYPE'] == 'extended' else None, axis=1)
    processed_bolus['INSNMBOL'] = processed_bolus.apply(
        lambda row: row['INSNMBOL'] if row['INSSTYPE'] == 'normal' else None, axis=1)
    processed_bolus = processed_bolus[
        ['FADTC', 'FATEST', 'FACAT', 'INSNMBOL', 'INSEXBOL', 'INSSTYPE', 'original_value', 'bolus_id']]

    carbs_df = carbs_df[['event_ts', 'carbs']]
    carbs_df['event_ts'] = pd.to_datetime(carbs_df['event_ts'], format='%Y-%m-%d %H:%M:%S')
    carbs_df = carbs_df.rename(columns={'event_ts': 'MLDTC', 'carbs': 'MLDOSE'})
    processed_carbs = carbs_df.sort_values(by='MLDTC')

    cgm_df = cgm_df[['event_ts', 'current_glucose_display_value']]
    cgm_df['event_ts'] = pd.to_datetime(cgm_df['event_ts'], format='%Y-%m-%d %H:%M:%S')
    cgm_df = cgm_df.rename(columns={'event_ts': 'LBDTC', 'current_glucose_display_value': 'LBORRES'})
    processed_glucose = cgm_df.sort_values(by='LBDTC')

    insulin_df = pd.concat([processed_bolus, processed_basal]).sort_values(by='FADTC')
    insulin_df = insulin_df[
        ['FADTC', 'FATEST', 'FACAT', 'FASTRESN', 'INSNMBOL', 'INSEXBOL', 'INSSTYPE', 'original_value', 'bolus_id',
         'commanded_basal_rate', 'base_basal_rate', 'FADUR']]

    return processed_basal, processed_bolus, processed_carbs, processed_glucose, insulin_df


def get_last_x_hr(dataframe: pd.DataFrame, real_time, revert_by: float) -> pd.DataFrame:
    x_hour_ago = pd.to_datetime(real_time) - timedelta(hours=revert_by)
    filtered_df = dataframe[(pd.to_datetime(dataframe['FADTC']) > x_hour_ago) & \
                            (pd.to_datetime(dataframe['FADTC']) < pd.to_datetime(real_time))] \
        .sort_values(by='FADTC', ascending=False)
    return filtered_df


def avg_basal_rate(basal_insulin_data: pd.DataFrame):
    basal_insulin_data['HOUR'] = pd.to_datetime(basal_insulin_data['FADTC']).dt.hour

    basal_insulin_df = basal_insulin_data[
        (basal_insulin_data['FACAT'] == 'BASAL') & (basal_insulin_data['FATEST'] == 'BASAL INSULIN') & (
            basal_insulin_data['INSSTYPE'].isin(['basal', 'basal_chunk']))]

    hours_template = pd.DataFrame({'HOUR': range(24)})

    for _, row in basal_insulin_df.iterrows():
        hour = row['HOUR']
        hours_template.loc[hours_template['HOUR'] == hour, 'FASTRESN'] = row['FASTRESN']

    for i in range(1, 23):  # Avoid the first and last hour to ensure we always have a previous and next value
        if pd.isna(hours_template.at[i, 'FASTRESN']):
            prev_val = hours_template.at[i - 1, 'FASTRESN']
            next_val = hours_template.at[i + 1, 'FASTRESN']
            if not pd.isna(prev_val) and not pd.isna(next_val) and prev_val != next_val:
                hours_template.at[i, 'FASTRESN'] = float(prev_val + next_val) / 2

    hours_template['FASTRESN'] = hours_template['FASTRESN'].fillna(method='ffill').fillna(method='bfill')
    hours_template.loc[hours_template['FASTRESN'] == 0.0, 'FASTRESN'] = 0.01
    avg_basal_rate_dict = hours_template.set_index('HOUR')['FASTRESN'].to_dict()
    basal_rate_structure_list = [{'i': i, 'start': f'{hour:02d}:00:00', 'minutes': hour * 60, 'rate': rate} for i,
    (hour, rate) in enumerate(avg_basal_rate_dict.items())]

    profile = {'dia': 5, 'basalprofile': basal_rate_structure_list}

    return basal_rate_structure_list, profile


def compute_basal_duration(basal_records: pd.DataFrame) -> pd.DataFrame:
    basal_records['DURATION'] = (pd.to_datetime(basal_records['FADTC'].shift(-1)) - \
                                 pd.to_datetime(basal_records['FADTC'])).dt.total_seconds() / 60
    return basal_records


def datetime_to_zoned_iso(time, timezone):
    return time.strftime(f'%Y-%m-%dT%H:%M:%S{timezone}')
