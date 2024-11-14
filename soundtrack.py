from sql_blocks import (
    Select, Field, OrderBy,
    Where, SortType
)
import duckdb


OrderBy.sort = SortType.DESC
BASIC_FIELDS = {'track_name':Field, 'artist_name': Field}
WORK = BASIC_FIELDS | {
    'acousticness': [Field, OrderBy], 'loudness': Where.lt(0.66),
}
SPORTS = BASIC_FIELDS | {
    'energy': [Field, OrderBy], 'danceability': Where.gt(0.54)
}
STUDY = BASIC_FIELDS | {
    'spiritual': [Field, OrderBy], 'instrumentalness': Where.gt(0.1)
}


def music_to(params: dict, file_ext: str = 'csv'):
    table_name = f"'music.{file_ext}' m"
    query = Select(table_name, **params).limit(20)
    return duckdb.sql( str(query) )


# How to use: --------------------------------------------
# >> from soundtrack import music_to, WORK, SPORTS, STUDY
# >> music_to(SPORTS)
#   +-------------------------------------+------------------------+--------------------+
#   |             track_name              |      artist_name       |       energy       |
#   |               varchar               |        varchar         |       double       |
#   +-------------------------------------+------------------------+--------------------+
#   | lucky denver mint                   | jimmy eat world        | 0.9969969032065865 |
#   | dirthouse                           | static-x               | 0.9959958709421154 |
#   | destroyer                           | static-x               | 0.9959958709421154 |
#   | what's my name? (re-recorded re...  | dmx                    | 0.9919917418842309 |
#   | last call in jonestown              | polkadot cadaver       | 0.9919917418842309 |
#   | goody two shoes                     | adam ant               | 0.9919917418842309 |
#   | midnite dynamite                    | kix                    | 0.9909907096197598 |
#   | highly evolved                      | the vines              | 0.9909907096197598 |
#   | i go to work (re-recorded)          | kool moe dee           | 0.9899896773552888 |
#   | you came                            | kim wilde              | 0.9899896773552888 |
#   | beautiful life                      | ace of base            | 0.9889886450908175 |
#   | the hand that feeds                 | nine inch nails        | 0.9859855482974041 |
#   | happy new year                      | hiphop tamizha         | 0.9859855482974041 |
#   | oh, how to do now                   | the monks              | 0.9859855482974041 |
#   | livin' & rockin'                    | 311                    | 0.9859855482974041 |
#   | no more hot dogs                    | hasil adkins           | 0.9849845160329331 |
#   | dig                                 | mudvayne               | 0.9839834837684619 |
#   | twisted transistor                  | korn                   | 0.9839834837684619 |
#   | voodoo mon amour                    | diablo swing orchestra | 0.9839834837684619 |
#   | fried my little brains              | the kills              | 0.9829824515039908 |
#   +-------------------------------------+------------------------+--------------------+
#   | 20 rows                                                                 3 columns |
#   +-----------------------------------------------------------------------------------+
