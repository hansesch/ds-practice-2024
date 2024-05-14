from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)
    host = "http://localhost:8081"


    @task
    def checkout(self):
        # Sample formData for testing
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

        # Sample book data for testing
        book = {
            "title": "Learning Python",
            "category": "Programming",
            "id": "1"
        }

        # Preparing the request payload
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
            "items": [
                {
                    "name": book["title"],
                    "quantity": 1,
                    "category": book["category"],
                    "id": book["id"]
                },
            ],
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

        # Making the POST request
        with self.client.post("/checkout", json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to complete checkout: {response.text}")
            else:
                response.success()