import pandas as pd
from datetime import datetime, timedelta


def reading_in_dataframes_based_on_date():
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    recent_df = pd.read_csv("datasets/spaces/{}_spaces_v0.csv".format(today_date))

    past_df = pd.read_csv("datasets/spaces/{}_spaces_v0.csv".format(yesterday))

    return [past_df,
            recent_df]


def comparing_yesterday_today_to_get_new_daos(df_list):
    prev_df = df_list[0]
    new_df = df_list[1]

    old_daos = prev_df['name'].tolist()
    new_daos = new_df['name'].tolist()

    dao_diff = []

    for dao_name in new_daos:
        if dao_name not in old_daos:
            dao_diff.append(dao_name)
    new_daos = new_df[new_df['name'].isin(dao_diff)][['name', 'no_of_members']]
    return new_daos


def comparing_yesterday_today_to_get_membership_count_table(df_list):
    prev_df_member_count = df_list[0][['id', 'name', 'no_of_members']].copy(deep=True)
    new_df_member_count = df_list[1][['id', 'name', 'no_of_members']].copy(deep=True)

    prev_df_member_count.columns = ['id', 'name', 'prev_no_of_members']
    new_df_member_count.columns = ['id', 'name', 'new_no_of_members']

    combined_df = pd.merge(prev_df_member_count,
                           new_df_member_count,
                           how='left',
                           left_on=['id', 'name'],
                           right_on=['id', 'name']
                           )

    return combined_df


def comparing_yesterday_today_to_get_membership_count_table(df_list):
    prev_df_member_count = df_list[0][['id', 'name', 'no_of_members']].copy(deep=True)
    new_df_member_count = df_list[1][['id', 'name', 'no_of_members']].copy(deep=True)

    prev_df_member_count.columns = ['id', 'name', 'prev_no_of_members']
    new_df_member_count.columns = ['id', 'name', 'new_no_of_members']

    combined_df = pd.merge(prev_df_member_count,
                           new_df_member_count,
                           how='left',
                           left_on=['id', 'name'],
                           right_on=['id', 'name']
                           )

    return combined_df


def getting_greatest_delta(df_with_prev_and_new):
    df_with_prev_and_new['delta'] = df_with_prev_and_new['new_no_of_members'] - df_with_prev_and_new['prev_no_of_members']
    return df_with_prev_and_new.sort_values(by='delta',
                                            ascending=False).head(5)



list_of_dao_snap_data = reading_in_dataframes_based_on_date()
print("New DAO Additions")
print(comparing_yesterday_today_to_get_new_daos(list_of_dao_snap_data))

aggregated_table_with_no_of_members = comparing_yesterday_today_to_get_membership_count_table(list_of_dao_snap_data)
top_changes = getting_greatest_delta(aggregated_table_with_no_of_members)


