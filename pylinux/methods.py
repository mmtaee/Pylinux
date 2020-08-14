from django.contrib.auth.tokens import PasswordResetTokenGenerator

import six
from datetime import datetime



class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.email)+six.text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()



class MaxRequestUser(object):

    def __init__(self, request, *args, **kwargs):
        self.date = datetime.now().date()
        self.ip = request.META.get('REMOTE_ADDR')
        self.session = request.session

    def get_request_count(self):
        data = self.session.get('try')
        if data:
            count = int(data['count'])
        else:
            count = 0
        return count

    def add_request_count(self):
        data = self.session.get('try')
        if data:
            date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            count = int(data['count'])
            if date < self.date:
                kwargs = {
                    'date': self.date.strftime("%Y-%m-%d"),
                    'count' : 1,
                }
            elif date == self.date :
                kwargs = {
                    'date': self.date.strftime("%Y-%m-%d"),
                    'count' : count +  1,
                }
        elif not data :
            kwargs = {
                'date': self.date.strftime("%Y-%m-%d"),
                'count' : 1,
            }
        data = self.session['try'] = kwargs
        self.session.modified = True
        return data['count']



def check_profanity(text):
    with open('profanity.txt', 'r') as f:
        profanity_file = f.readlines()
        profanity_file = [i.strip() for i in profanity_file]

    text = text.replace("&lt;" ," ").replace("&gt;", " ").replace("\n" , " ").replace("\r", "")\
                .replace("<p>", " ").replace("</p>", " ").replace("*", "").replace("/", "")\
                .replace("+", "").replace("-", "").replace(".", "").replace("0", "")\
                .replace("@", "").replace("#", "").replace("!", "").replace("$", "")\
                .replace("%", "").replace("^", "").replace("&", "").replace("(", "")\
                .replace(")", "").replace("_", "").replace("]", "").replace("[", "")\
                .replace("}", "").replace("{", "").replace(">", "").replace("<", "")\
                .replace("?", "").replace("~", "").replace(",", "").replace(".", "").split(" ")
    found_profanity = (word for word in text if word.strip().lower() in profanity_file and word!="")
    for profanity in found_profanity:
        if profanity :
            return False
    return True

    
