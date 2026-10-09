def build_flows(df):

    df["src_port"] = df["tcp.srcport"].fillna(df["udp.srcport"])
    df["dst_port"] = df["tcp.dstport"].fillna(df["udp.dstport"])

    df["ip_low"] = df[["ip.src", "ip.dst"]].min(axis=1)
    df["ip_high"] = df[["ip.src", "ip.dst"]].max(axis=1)
    df["is_low_to_high"] = df["ip.src"] == df["ip_low"] #IF true, src.ip == ip.low, else src.ip == ip.high

    df["time_bucket"] = (df["frame.time_epoch"] //0.75).astype(int)

    df["port_low"] = df[["src_port", "dst_port"]].min(axis=1)
    df["port_high"] = df[["src_port", "dst_port"]].max(axis=1)

    flow_cols = ["ip_low", "ip_high", "port_low", "port_high", "ip.proto","time_bucket"]

    src_bytes = df[df["is_low_to_high"]].groupby(flow_cols)["frame.len"].sum() # assign src_bytes to bytes going from low to high
    dest_bytes = df[~df["is_low_to_high"]].groupby(flow_cols)["frame.len"].sum() #assign dst_bytes to bytes going from high to low

    df = df.sort_values(by=flow_cols + ["frame.time_epoch"])
    df["iat"] = df.groupby(flow_cols)["frame.time_epoch"].diff().fillna(0)

    flows = df.groupby(flow_cols)

    flow_df = flows.agg({"frame.time_epoch": ["min", "max"],"frame.len": ["count", "sum", "mean","std"],"iat": ["mean", "std"]})
    flow_df.columns = ["start_time", "end_time","packet_count", "total_bytes", "avg_packet_size","packet_size_std","iat_mean","iat_std"]
    flow_df = flow_df.reset_index()
    src_bytes = src_bytes.rename("src_bytes").reset_index()
    dest_bytes = dest_bytes.rename("dest_bytes").reset_index()

    flow_df = flow_df.merge(src_bytes, on=flow_cols, how="left")
    flow_df = flow_df.merge(dest_bytes, on=flow_cols, how="left")

    flow_df["src_bytes"] = flow_df["src_bytes"].fillna(0)
    flow_df["dest_bytes"] = flow_df["dest_bytes"].fillna(0)

    flow_df["Label"] = df.groupby(flow_cols)["Label"].first().values

    flow_df = flow_df[flow_df["packet_count"] > 3]

    return flow_df