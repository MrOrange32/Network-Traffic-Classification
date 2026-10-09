def write_output(flow_df, models):

    flow_df.to_csv("full_dataset.csv", index=False)
    if len(models.features) > 6:
        with open("Project Metrics All 9 Features.csv", "w") as f:
            print('Name, Best Training Score, Testing Score',file=f)
            for line in models.outputs:
                print(line, file=f)

        with open("Project_Data.csv", "w") as f:
            print(flow_df, file =f)

    with open("Project Metrics with Reduced 6 Features.csv", "w") as f:
        print('Name, Best Training Score, Testing Score',file=f)
        for line in models.outputs:
            print(line, file=f)

        with open("Project_Data.csv", "w") as f:
            print(flow_df, file =f)
