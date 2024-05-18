from locust import HttpUser, task, between, TaskSet

formData = {
    "userName": "John Doe",
    "userContact": "john.doe@example.com",
    "creditCardNumber": "4111111111111111",
    "creditCardExpirationDate": "12/25",
    "creditCardCVV": "123",
    "userComment": "Please handle with care.",
    "discountCode": "",
    "shippingMethod": "Standard",
    "giftMessage": "Happy Birthday!",
    "billingAddressStreet": "123 Main St",
    "billingAddressCity": "Springfield",
    "billingAddressState": "IL",
    "billingAddressZip": "62701",
    "billingAddressCountry": "USA",
    "giftWrapping": True,
    "termsAndConditionsAccepted": True
}

books = [
    {"name": "Learning Python",
    "quantity": 1,
    "category": "Programming",
    "id": "1"},
    {"name": "JavaScript - The Good Parts",
    "quantity": 1,
    "category": "Web Development",
    "id": "2"},
    {"name": "Domain-Driven Design: Tackling Complexity in the Heart of Software",
    "quantity": 1,
    "category": "Web Development",
    "id": "3"},
    {"name": "Design Patterns: Elements of Reusable Object-Oriented Software",
    "quantity": 1,
    "category": "Software Development",
    "id": "4"}
]


payload = {
    "user": {
        "name": formData["userName"],
        "contact": formData["userContact"]
    },
    "creditCard": {
        "number": formData["creditCardNumber"],
        "expirationDate": formData["creditCardExpirationDate"],
        "cvv": formData["creditCardCVV"]
    },
    "userComment": formData["userComment"],
    "discountCode": formData["discountCode"],
    "shippingMethod": formData["shippingMethod"],
    "giftMessage": formData["giftMessage"],
    "billingAddress": {
        "street": formData["billingAddressStreet"],
        "city": formData["billingAddressCity"],
        "state": formData["billingAddressState"],
        "zip": formData["billingAddressZip"],
        "country": formData["billingAddressCountry"]
    },
    "giftWrapping": formData["giftWrapping"],
    "termsAndConditionsAccepted": formData["termsAndConditionsAccepted"],
    "notificationPreferences": ["email"],
    "device": {
        "type": "Smartphone",
        "model": "Samsung Galaxy S10",
        "os": "Android 10.0.0"
    },
    "browser": {
        "name": "Chrome",
        "version": "85.0.4183.127"
    },
    "appVersion": "3.0.0",
    "screenResolution": "1440x3040",
    "referrer": "https://www.google.com",
    "deviceLanguage": "en-US"
}

class BaseTaskSet(TaskSet):
    def checkout(self, payload):
        # Making the POST request
        with self.client.post("/checkout", json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to complete checkout: {response.text}")
            else:
                response.success()

# Multiple non-fraudulent, non-conflicting orders
class TestSet1(BaseTaskSet):
    @task
    def task_1_1(self):
        payload['items'] = [books[0]]
        self.checkout(payload)
    @task
    def task_1_2(self):
        payload['items'] = [books[1]]
        self.checkout(payload)    
    @task
    def task_1_3(self):
        payload['items'] = [books[2]]
        self.checkout(payload)    

# Multiple Mixed orders: Fraudulent/Non-fraudulent, non-conficting
class TestSet2(BaseTaskSet):
    @task
    def task_1_1(self):
        payload['items'] = [books[0]]
        payload['discountCode'] = "123"
        self.checkout(payload)
    @task
    def task_1_2(self):
        payload['items'] = [books[1]]
        payload['discountCode'] = ""
        self.checkout(payload)    
    @task
    def task_1_3(self):
        payload['items'] = [books[2]]
        payload['discountCode'] = "123"
        self.checkout(payload)    
    @task
    def task_1_4(self):
        payload['items'] = [books[3]]
        payload['discountCode'] = ""
        self.checkout(payload)    


# Conflicting orders
class TestSet3(BaseTaskSet):
    @task
    def task_1_1(self):
        payload['items'] = [books[0]]
        self.checkout(payload)
    @task
    def task_1_2(self):
        payload['items'] = [books[0]]
        self.checkout(payload)    
    @task
    def task_1_3(self):
        payload['items'] = [books[0]]
        self.checkout(payload)    
    @task
    def task_1_4(self):
        payload['items'] = [books[0]]
        self.checkout(payload)


class WebsiteUser1(HttpUser):
    tasks = [TestSet1]
    wait_time = between(1, 2)
    host = "http://localhost:8081"

class WebsiteUser2(HttpUser):
    tasks = [TestSet2]
    wait_time = between(1, 2)
    host = "http://localhost:8081"

class WebsiteUser3(HttpUser):
    tasks = [TestSet3]
    wait_time = between(1, 2)
    host = "http://localhost:8081"