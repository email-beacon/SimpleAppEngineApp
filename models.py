class UserRequest:
    def __init__(self, api_key, user_id, encoded_user_email,
                 beacon_id="", group="", campaign="", sent_date="", custom_1="", custom_2="", custom_3=""):
        self.api_key = api_key
        self.user_id = user_id
        self.encoded_user_email = encoded_user_email

        self.beacon_id = beacon_id
        self.group = group
        self.campaign = campaign
        self.sent_date = sent_date
        self.custom_1 = custom_1
        self.custom_2 = custom_2
        self.custom_3 = custom_3

    def __repr__(self):
        return unicode("UserRequest(" + "<" + self.api_key + ">," + "<" + self.user_id + ">," +
                       "<" + self.encoded_user_email + ">," + "<" + self.beacon_id + ">," +
                       "<" + self.group + ">," + "<" + self.campaign + ">," + "<" + self.sent_date + ">," +
                       "<" + self.custom_1 + ">," + "<" + self.custom_2 + ">," + "<" + self.custom_3 + ">," + ")")

    def validate_on_submit(self):
        if self.api_key == "" or self.user_id == "" or self.encoded_user_email == "":
            return False
        else:
            return True

    def as_sql_string(self):
        # Set NULL
        if self.beacon_id == "": self.beacon_id = "NULL"
        if self.group == "":
            self.group = "NULL"
        else:
            self.group = "'" + self.group + "'"
        if self.campaign == "": self.campaign = "NULL"
        if self.sent_date == "": self.sent_date = "NULL"
        if self.custom_1 == "":
            self.custom_1 = "NULL"
        else:
            self.custom_1 = "'" + self.custom_1 + "'"
        if self.custom_2 == "":
            self.custom_2 = "NULL"
        else:
            self.custom_2 = "'" + self.custom_2 + "'"
        if self.custom_3 == "":
            self.custom_3 = "NULL"
        else:
            self.custom_3 = "'" + self.custom_3 + "'"
        return "INSERT INTO requests (api_key, user_id, encoded_user_email, " \
               "beacon_id, group_, campaign, sent_date, custom_1, custom_2, custom_3) " \
               "VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format("'" + self.api_key + "'", "'" + self.user_id + "'", "'" + self.encoded_user_email + "'",
                                                                        self.beacon_id, self.group, self.campaign,
                                                                        self.sent_date, self.custom_1, self.custom_2, self.custom_3)