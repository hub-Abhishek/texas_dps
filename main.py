import texas_dps
import random
import yaml
from time import sleep

if __name__=='__main__':

    with open(r'cred.yaml') as file:
        z = yaml.load(file, Loader=yaml.FullLoader)

    booked = False

    while not booked:

        for zip_code in z['zip_code'].split(','):
            if booked:
                break

            iterator = ''.join([chr(random.choice(range(65, 91))) for x in range(26)])
            appointement = texas_dps.dps_appointement(iterator=iterator,
                                                      idno='',
                                                      fname=f"{z['fname']}{iterator}",
                                                      lname=z['lname'],
                                                      dob=z['dob'],
                                                      ssn=z['ssn'],
                                                      phone=z['phone'],
                                                      mail=z['mail'],
                                                      zip_code=zip_code)
            appointement.initialize()
            sleep(4)
            appointement.login()
            sleep(3)
            status, date = appointement.get_new_appointment()

            if status:
                iterator = ''
                appointement_final = texas_dps.dps_appointement(iterator=iterator,
                                                          idno='',
                                                          fname=z['fname'],
                                                          lname=z['lname'],
                                                          dob=z['dob'],
                                                          ssn=z['ssn'],
                                                          phone=z['phone'],
                                                          mail=z['mail'],
                                                          zip_code=z['zip_code'])
                appointement_final.initialize()
                sleep(2)
                appointement_final.login()
                sleep(2)
                status, final_date = appointement_final.get_new_appointment()
                sleep(2)
                if date == final_date:
                    appointement_final.book_appointment()
                    booked=True
                    break
        print('Not booked in this cycle')
        sleep(3600)
