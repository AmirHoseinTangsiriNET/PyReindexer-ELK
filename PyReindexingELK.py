import requests

# Set your Elasticsearch configuration
source_host = input("[+]Please Enter Source ELK Host: (Exmaple: http://192.168.1.1:9200)")
dest_host = input("[+]Please Enter Dest ELK Host: (Exmaple: http://192.168.1.1:9200)")
auth = ("Username", "Password")  # Replace with your credentials

# Retrieve the list of indexes using Elasticsearch _cat/indices API
response = requests.get(f"{source_host}/_cat/indices?h=index", auth=auth)
index_names = response.text.splitlines()

# Open a file for writing the output
with open("reindex_output.txt", "w") as output_file:
    # Iterate through the list of indexes and perform reindexing
    for index_name in index_names:
        payload = {
            "source": {
                "remote": {
                    "host": source_host,
                    "username": auth[0],
                    "password": auth[1],
                    "socket_timeout": "1m",
                    "connect_timeout": "1m"
                },
                "index": index_name
            },
            "dest": {
                "index": index_name
            }
        }
        
        response = requests.post(f"{dest_host}/_reindex", json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            output_message = f"Reindexing completed for index {index_name}.\n"
        else:
            output_message = f"Error reindexing index {index_name}. Status code: {response.status_code}\n"
        
        # Write the output to the file
        output_file.write(output_message)
        
        # Display the output in the terminal
        print(output_message)

print("All reindexing operations completed.")
