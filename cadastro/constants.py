from .models import Person

person = Person.objects.get(id=1)

sender_email = person.email
password_email = person.password_email
receive_email = "josecarlosrodriguesrod.pinto@gmail.com"


