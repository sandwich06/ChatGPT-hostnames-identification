import os
import csv
import time
import json
import openai
import pandas as pd

openai.organization = "org-aNatCq1nRd9GcY4ljciaPeM6"
openai.api_key = "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"


def write_csv(datarow):
    path="result_new.csv"
    with open(path,'a+',newline='',encoding='utf-8') as f:
        csv_write=csv.writer(f)
        datarow=datarow
        csv_write.writerow(datarow)

def post_message(prompt):

    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        max_tokens=1000,
        temperature=0,

    )
    #print(response)
    try:
        response = response.choices[0].text
        response = response.strip()
        if(response[0]!='{'):
            response = '{'+response+'}'
        else:
            response = response + '}'
    except:
        response = ""
    #response = response.replace("\'", "\"")
    return response


filename = 'iot_class_data_class_output_hostname_df.csv'
dataset = pd.read_csv(filename)
print(dataset.shape)

dataset = dataset.drop_duplicates(subset="remote_hostname")
print(dataset.shape)

index = 1
for hostname in dataset['remote_hostname']:
    print(hostname)
    try:
        response=post_message("You must respond ONLY with JSON that looks like this:"
                              " {\"company\": company,\"purpose\": purpose}"
                              " The company and purpose of domain("+hostname+").")

        #response=post_message("You must respond ONLY with JSON that looks like this: {\"company\": company, \"purpose\": purpose} The domain("+hostname+") belongs to which company(Most used name) and The domain("+hostname+") belongs to which company(Most used name)..")
        data = json.loads(response)
        print(response)
    except:
        response=post_message("You must respond ONLY with JSON that looks like this: {\"company\": company,\"purpose\": purpose} The company and purpose of domain("+hostname+").")
        time.sleep(2)
        write_csv([hostname,'None','None'])
    else:

        write_csv([hostname,data['company'],data['purpose']])
    print(index)
    index = index+1
    time.sleep(1)

'''
for i in range(5):
    response = post_message(
        '"What company owns the domain [google.com] and what is its purpose?" Respond in json{"domain": String,"owner": String, "purpose": String}')
    print(response)

response4=post_message("only tell me the purpose of domain(gvt2.com) ,no other excuses and texts")
print(response4)
response1 = post_message("tell me who own the domain(gvt2.com), You must respond ONLY with JSON that looks like this: {'hostname': 'company'} and no extra text,only give me the owner")
print(response1)
response2 = post_message(
    "only tell me the domain(googleusercontent.com) belongs to which company, only give me the company, no extra text")

response1 = post_message("only tell me who own the domain(" + hostname + "),only give me the owner, no extra text")
response2 = post_message(
    "only tell me the domain(" + hostname + ") belongs to which company, only give me the company, no extra text")
response3 = post_message("only tell me What is this domain(" + hostname + ") used for,no extra text")
response4 = post_message("only tell me the purpose of domain(" + hostname + "),no extra text")
write_csv([hostname, response1, response2, response3, response4])
'''