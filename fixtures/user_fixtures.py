import io

image_upload = {"profile_pic": (io.BytesIO(b"test image"), 'test.png')}
invalid_image = {"profile_pic": (io.BytesIO(b"invalid image"), 'test.txt')}

user_1 = {
    "user_name": "Peter",
    "first_name": "Peter",
    "last_name": "wanyama",
    "gender": "male",
    "dob": "1999-01-02",
    "phone_no": "+254746738877",
    "email": "peter@gmail.com",
    "password": "Abc123",
    "role": 4,
    "status": "active"
}

user_2 = {
    "user_name": "kama",
    "first_name": "kamau",
    "last_name": "wanyama",
    "gender": "male",
    "dob": "1999-01-02",
    "phone_no": "+254746738877",
    "email": "kama@gmail.com",
    "password": "Abc123",
    "role": 4,
    "status": "active"
}

admin_user = {
    "user_name": "john",
    "first_name": "john",
    "last_name": "junior",
    "gender": "male",
    "dob": "1999-01-02",
    "phone_no": "+254746738877",
    "email": "john@gmail.com",
    "password": "Abc123",
    "role": 1,
    "status": "active"
}

create_user_1 = {
    "user_name": "Juma",
    "first_name": "Peter",
    "last_name": "wanyama",
    "gender": "male",
    "dob": "1999-01-02",
    "phone_no": "+254746738877",
    "email": "juma@gmail.com",
    "password": "Abc123"
}

user_login = {
    "user_name": "Peter",
    "password": "Abc123"
}
