from wrappity import wrap, unwrap, inspect

person1 = {'name':'John','surname':'Doe','age':40,'personal_details': {'kids':['Minnie','Moe'], 'wife':'Jane'},'address':{'street':'Rosemary Road 5','city':'Flower City','state':'Kansas'}}
person2 = {'name':'Jack','surname':'Doe','age':35,'personal_details': {'partner': 'Juan'},'address':{'street':'Dead end','city':'Forgotten City','state':'Oklahoma'}}

def greet_kids(person):
	for kid in wrap(person).personal_details.kids._ or []:
		print(f'Hi {kid}!')

greet_kids(person1)
greet_kids(person2)

def greet_significant_other(person):
	pd = wrap(person).personal_details
	significant_other = (pd.wife or pd.partner)._
	if significant_other:
		print(f'Greetings dear {significant_other}!')

greet_significant_other(person1)
greet_significant_other(person2)

person3 = {'name':'Jill','surname':'Newjoiner'}
greet_kids(person3)
greet_significant_other(person3)
