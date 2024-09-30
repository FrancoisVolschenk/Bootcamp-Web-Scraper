with open("update_images.sql", "w") as fl_sql:
    with open("urls.csv", "r") as fl_urls:
        for line in fl_urls:
            id, url, _ = line.strip().split(',')
            fl_sql.write(f"UPDATE Issues SET CoverImage = '{url}' WHERE IssueID = {id};\n")
            fl_sql.flush()