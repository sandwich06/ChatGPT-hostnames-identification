import os
import csv
import time
import json
import openai
import pandas as pd

openai.organization = "org-aNatCq1nRd9GcY4ljciaPeM6"
openai.api_key = "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"


def write_csv(datarow):
    path="infer.csv"
    with open(path,'a+',newline='',encoding='utf-8') as f:
        csv_write=csv.writer(f)
        datarow=datarow
        csv_write.writerow(datarow)

def post_message(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "assistant", "content": prompt}
        ]
    )

    print(response.choices[0].message)
    return response.choices[0].message

filename = 'iot_class_data_class_output_hostname_df.csv'
dataset = pd.read_csv(filename)
print(dataset.shape)

device_id = dataset.drop_duplicates(subset="device_id")
print(device_id.shape)

for id in device_id['device_id']:
    hostnames = dataset[dataset['device_id'] == id]
    hn= ""
    for hostname in hostnames['remote_hostname']:
        hn = hn + hostname +","
    response = post_message('You must respond ONLY with JSON that looks like this: {"device_id": type} If a IOT device contacts ' +hn+ ' what is most probale type of this device')
    try:
        response= json.loads(response['content'])
    except:
        write_csv([id, "None"])
    else:
        write_csv([id,response["device_id"]])
    time.sleep(20)