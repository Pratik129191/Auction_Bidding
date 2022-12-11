from locust import HttpUser, task, between
from random import randint


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    # @task
    # def register(self):
    #     print('registering')
    #     self.client.post(
    #         '/register/',
    #         name='/register/',
    #         json={
    #             'username': 'Pratik',
    #             'password': 'salute1234',
    #             'first_name': 'Pratik',
    #             'last_name': 'Mukherjee',
    #             'email': 'codingtricks.csc@gmail.com',
    #             'phone': '8653081695',
    #             'birth_date': '2001-07-27',
    #             'address': 'Kanaipur, Bantul, Bagnan, Howrah'
    #         }
    #     )
    @task(2)
    def view_dashboard(self):
        print('Viewing Dashboard')
        self.client.get('/dashboard/', name='/dashboard/')

    @task(1)
    def login(self):
        print('Logging In')
        self.client.post(
            '/login/',
            name='/login/',
            json={
                'username': 'tapati',
                'password': 'soumya1234'
            }
        )

    @task
    def logout(self):
        print('logging out')
        self.client.post(
            '/logout/',
            name='/logout/',
            json={
                'username': 'tapati',
                'password': 'soumya1234'
            }
        )

    @task(3)
    def view_auctions(self):
        print('View Auctions')
        self.client.get('/marketplace/', name='/marketplace')

    @task(4)
    def view_auction(self):
        print('View PArticular Auction')
        auction_id = randint(1, 1000)
        self.client.get(f'/marketplace/{auction_id}/', name='/marketplace/:id')

    @task(5)
    def bid_amount(self):
        print('Bid Amount')
        auction_id = randint(1, 1000)
        bid = randint(300, 10000)
        self.client.post(
            f'/marketplace/{auction_id}/',
            name='marketplace/:id',
            json={
                'amount': bid
            }
        )

    @task(6)
    def view_own_bids(self):
        print('View Own Bids')
        self.client.get('/my-bids/', name='/my-bids/')

    # @task(7)
    def confirm_bids(self):
        print('Confirm Bids')
        self.client.post(
            '/confirm-bids/',
            name='/confirm-bids/',
            json={
                'confirmed': True
            }
        )

    @task(8)
    def view_about(self):
        print('Viewing About')
        self.client.get('/about/', name='/about/')

    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

