import streamlit_authenticator as stauth
import yaml

usernames = ['admin', 'editor']
names = ['Admin User', 'Editor']
passwords = ['pass123', 'edit456']

hashed = stauth.Hasher(passwords).generate()

config = {
    'credentials': {
        'usernames': {
            usernames[0]: {'name': names[0], 'password': hashed[0]},
            usernames[1]: {'name': names[1], 'password': hashed[1]}
        }
    },
    'cookie': {
        'name': 'agentic_auth_cookie',
        'key': 'supersecretkey',
        'expiry_days': 1
    },
    'preauthorized': {'emails': []}
}

with open('config.yaml', 'w') as f:
    yaml.dump(config, f, sort_keys=False)
print("✅ config.yaml generated.")