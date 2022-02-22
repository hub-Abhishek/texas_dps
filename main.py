from datetime import datetime
import texas_dps
import random
import yaml
from time import sleep

if __name__=='__main__':

    with open(r'cred.yaml') as file:
        z = yaml.load(file, Loader=yaml.FullLoader)

    booked = False

    while not booked:

        # runs every 6 mins
        next_cycle_after = 360

        if datetime.now().hour == 5 or datetime.now().hour == 6:
            next_cycle_after = (datetime.datetime.now().replace(hour=7, minute=0, second=0, microsecond=0) - datetime.datetime.now()).seconds
            if next_cycle_after > 600:
                next_cycle_after = 360

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
            appointement.driver.close()

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
        sleep(next_cycle_after)
