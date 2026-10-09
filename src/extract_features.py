def extract_features(flow_df):

    flow_df["duration"] = (flow_df["end_time"] - flow_df["start_time"]).clip(lower=1e-4)
    flow_df = flow_df[flow_df["duration"] > 0]

    flow_df["throughput"] = flow_df["total_bytes"] / flow_df["duration"]
    flow_df["packets_per_sec"] = flow_df["packet_count"] /flow_df["duration"]
    flow_df["bytes_per_packet"] = flow_df["total_bytes"] / flow_df["packet_count"]
    flow_df["burstiness"] = flow_df["packet_count"] / (flow_df["iat_std"] + 1e-4)
    flow_df["packet_size_cv"] = flow_df["packet_size_std"] / (flow_df["avg_packet_size"] + 1e-4)
    flow_df["bytes_ratio_asymmetry"] = 1 - (flow_df[["src_bytes","dest_bytes"]].min(axis=1) / flow_df[["src_bytes","dest_bytes"]].max(axis=1))

    return flow_df
