from jyablonski_common_modules.general import check_feature_flag


def test_get_and_check_feature_flags_postgres(get_feature_flags_postgres):
    fake_check = check_feature_flag(flag="fake", flags_df=get_feature_flags_postgres)
    odds_check = check_feature_flag(flag="odds", flags_df=get_feature_flags_postgres)
    playoffs_check = check_feature_flag(
        flag="playoffs", flags_df=get_feature_flags_postgres
    )
    season_check = check_feature_flag(
        flag="season", flags_df=get_feature_flags_postgres
    )

    assert len(get_feature_flags_postgres) == 16
    assert fake_check == False
    assert odds_check == True
    assert playoffs_check == True
    assert season_check == True
