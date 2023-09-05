user={
    'Name':'abdo',
    'password':'123',
    'age':20,
    'gender':'male',
    'adress':'13 str ibrahem hasen alsayed',
    'job':'Developer',
    'subscrbtion': False
}
q = input('enter your copuon:')
if q == '123':
    user['subscrbtion'] = True
print(user)
