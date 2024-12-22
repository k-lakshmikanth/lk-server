import requests

api_token = '7955220166:AAG1LduLJE8_qiMtAKJKQbsUNAop_jtPqDk'
webhook_url = input("Enter the URL of your webhook: ")

response = requests.post(
    f'https://api.telegram.org/bot{api_token}/setWebhook',
    data={'url': webhook_url}
)

if response.status_code == 200:
    print('Webhook has been set successfully!')
else:
    print('Failed to set webhook. Please check your API token and URL.')

print(requests.get(f"https://api.telegram.org/bot{api_token}/getWebhookInfo").json())