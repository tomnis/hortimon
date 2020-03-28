#!/usr/bin/python3

import os
import requests
import schedule
import time

ethermine_api_url = 'https://api.ethermine.org'
etherchain_url = 'https://etherchain.org'

# for base unit conversion
wei_in_ether = 10 ** 18


def send_notifications(payout, to_numbers, balance):
    post_data = {
            "message" : "eth payout:\n   %.5f\n\nbalance:\n   %.5f" % (payout, balance),
            "to_numbers" : to_numbers
            }

    print(post_data)
    post_url = "http://isengard.lan/sms/send"
    r = requests.post(post_url, json=post_data)
    print("POST to notifier server response: " + str(r.status_code))
    return r



def get_balance(address_num):
    url = etherchain_url + '/api/account/' + address_num
    r = requests.get(url)
    balance_wei = r.json()['balance']
    return wei_to_ether(balance_wei)



def wei_to_ether(wei):
    return float(wei) / wei_in_ether



def check_payouts(address, to_numbers):
    url = ethermine_api_url + '/miner/' + address + '/payouts'
    r = requests.get(url)
    # responses are sorted by most recent
    last_payout = r.json()['data'][0]
    print(last_payout)
    payout = wei_to_ether(last_payout['amount'])
    paid_on = last_payout['paidOn']

    current_time = time.time()
    # check if the payout was in the last 5 minutes, + some slack)
    if (current_time - paid_on < (5 * 60 + 8)):
        address_num = address[2:]
        send_notifications(payout, to_numbers, get_balance(address_num))
    else:
        print("current time is: " + str(current_time) + ", not going to send texts")

def main():
    address = os.environ["ETHMON_ADDRESS"]
    print("ethmon_address: " + address)
    to_numbers = os.environ["ETHMON_TO_NUMBERS"]
    print("ethmond_to_numbers: " + to_numbers)


    schedule.every(5).minutes.do(lambda: check_payouts(address, to_numbers))

    while True:
        schedule.run_pending()
        time.sleep(300)



if __name__ == "__main__":
    main()
    #check_payouts()
