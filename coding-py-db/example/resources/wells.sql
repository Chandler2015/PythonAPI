select
    "internal" as dataSource,
    id AS chosenID,
    well_name as wellName,
    api_14 AS api14,
    perf_lateral_length as perfLateralLength,
    county,
    state,
    "US" as country
from
    `global`.`wells`
